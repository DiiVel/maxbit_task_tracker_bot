from loguru import logger

logger.add(
    "logs.log",
    format="{time} | {level: <8} | {name: ^15} | {function: ^15} | {line: >3} | {message}",
    rotation="9:00",
    compression="zip",
    level="INFO",
)