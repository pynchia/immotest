import logging

from app.core.config import settings

logging.basicConfig(format="%(asctime)s %(levelname)s:%(name)s: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(settings.LOGGING_LEVEL)
