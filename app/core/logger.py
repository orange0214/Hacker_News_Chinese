import sys
from pathlib import Path
from loguru import logger
from app.core.config import settings

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

PIPELINE_LOG_FILE = LOG_DIR / "news_ingestor.log"
ERROR_LOG_FILE = LOG_DIR / "error.log"

def setup_logging():
    """
    Configure Loguru logging system
    - Remove the default handler
    - Add console output (INFO and above)
    - Add pipeline.log (only records where extra['type'] == 'pipeline')
    - Add error.log (only records with level >= ERROR)
    """
    logger.remove()

    # 1. Console output
    logger.add(
        sys.stderr,
        level=settings.log_level if hasattr(settings, 'log_level') else 'INFO',
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
    )
    
    # 2. Pipeline (news ingestor) log
    logger.add(
        PIPELINE_LOG_FILE,
        filter=lambda record: record['extra'].get('type') == 'news_ingestor',
        rotation="10 MB",
        retention="10 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <7} | {extra[step]: <20} | {message}",
        level="INFO"
    )

    # 3. Error log
    logger.add(
        ERROR_LOG_FILE,
        level="ERROR",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        backtrace=True, # include stack trace in the log
        diagnose=True, # include diagnostic information in the log
    )

    logger.info("Logging system initialized")

setup_logging()

__all__ = ['logger']