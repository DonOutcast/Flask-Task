import logging


logging.basicConfig(
    format="%(asctime)s, %(msecs)d %(name)s %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("flask")
