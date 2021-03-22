from loguru import logger
import sys

config = {
	'base_url' : 'http://localhost:5000',
}
APP_IS_SUCCESS = "isSuccess"

logger.add(sys.stdout, level="DEBUG")
logger.add(
    "./logs/log_file.log",
    rotation="1 day",
    level="DEBUG",
    retention="30 days",
    backtrace=True,
    diagnose=True,  
)