import functools
import time
import asyncio
from typing import Any, Callable
from app.core.logger import logger

def monitor_news_ingestor(step_name: str):
    """
    # AOP decorator: used for monitoring key nodes of the business pipeline
    #
    # Functionality:
    # 1. Automatically logs start and finish events to pipeline.log
    # 2. Automatically catches exceptions and logs them to error.log (with stack trace)
    # 3. Measures and records execution time
    #
    # :param step_name: The name of the pipeline step, e.g. "Fetch-HN", "Extract-Jina"
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            news_ingestor_logger = logger.bind(type="news_ingestor", step=step_name)

            start_time = time.time()
            news_ingestor_logger.info(f"Starting {step_name}...")

            try:
                result = await func(*args, **kwargs)

                duration = time.time() - start_time

                count_info = ""
                if isinstance(result, (list, dict)) and result:
                    count_info = f"Processed {len(result)} items"
                
                news_ingestor_logger.info(f"COMPLETED in {step_name} in {duration:.2f}s. {count_info}")
                return result
            
            except Exception as e:
                duration = time.time() - start_time
                news_ingestor_logger.error(f"FAILED in {step_name} after {duration:.2f}s. Error: {str(e)}")

                logger.error(f"Exception in ingestion step [{step_name}]: {str(e)}")

                raise e
            
        return wrapper
    return decorator

