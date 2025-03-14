import logging
import sys
from logging.handlers import RotatingFileHandler
from .config import get_settings

settings = get_settings()

def setup_logger(name: str = None) -> logging.Logger:
    log_dir = settings.PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name or __name__)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logger("app")