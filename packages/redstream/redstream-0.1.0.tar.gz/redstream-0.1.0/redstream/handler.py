import logging
import json
import importlib
import pkgutil
import redis.asyncio as redis  # Асинхронный клиент Redis
from functools import wraps

logger = logging.getLogger("redis_handler")


class RedisHandlerRegistry:
    """Глобальный реестр обработчиков Redis Stream."""

    def __init__(self, auto_register_package=None, redis_url="redis://localhost:6379/0"):
        self.handlers = {}  # Словарь поток -> обработчик
        self.consumer_groups = {}  # Словарь поток -> consumer_group
        self.redis = redis.Redis.from_url(redis_url, decode_responses=True)  # Асинхронный клиент Redis

        if auto_register_package:
            self.auto_register_handlers(auto_register_package)

    def message(self, stream_name, consumer_group=None, filter_func=None):
        def decorator(func):
            @wraps(func)
            async def wrapper(message_data, message_id, source_stream):
                try:
                    logger.info(f"📩 Сообщение из {source_stream}: {message_data}")
                    if filter_func and not filter_func(message_data):
                        logger.info(f"⏩ Фильтр отклонил сообщение: {message_data}")
                        return None
                    return await func(message_data, message_id, source_stream)
                except Exception as e:
                    logger.error(f"❌ Ошибка в обработчике {func.__name__}: {e}")
                    return None

            self.handlers[stream_name] = wrapper
            if consumer_group:
                self.consumer_groups[stream_name] = consumer_group  # 🔥 Сохраняем consumer_group

            logger.info(f"🔍 Зарегистрирован хендлер: {stream_name} -> {func.__name__} (consumer_group={consumer_group})")
            return wrapper

        return decorator

    def get_handlers(self):
        """Возвращает все зарегистрированные обработчики."""
        return self.handlers

    def get_consumer_groups(self):
        """Возвращает все consumer_groups."""
        return self.consumer_groups

    def auto_register_handlers(self, package_name):
        """Автоматически ищет файлы обработчиков в указанном пакете и импортирует их."""
        logger.info(f"🔍 Поиск обработчиков в {package_name}...")
        try:
            package = importlib.import_module(package_name)
            for _, module_name, _ in pkgutil.iter_modules(package.__path__):
                if module_name == "__main__":
                    continue
                full_module_name = f"{package_name}.{module_name}"
                logger.info(f"📥 Импорт обработчика: {full_module_name}")
                importlib.import_module(full_module_name)
        except ModuleNotFoundError as e:
            logger.error(f"❌ Ошибка при загрузке обработчиков: {e}")
        logger.info(f"✅ Все обработчики загружены автоматически. Итоговый список: {self.handlers.keys()}")


# Создаем глобальный экземпляр
redis_handler = RedisHandlerRegistry()


#Мне надо иметь возможность маркировать некоторые конфигурации как "только для чтения". Вносить изменения может только специальный сервис.
#Попытка внести запись в неизменяемые данные другими сервисами должна игнорироваться и отображаться варнингом в логах 
#Не должно быть привязки к именам сервисов внутри классов