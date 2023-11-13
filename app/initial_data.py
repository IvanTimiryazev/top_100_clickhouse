import logging
from app.db.queries import health_check, df_to_clickhouse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
	health_check()


def main() -> None:
	logger.info("Загружаем данные")
	init()
	logger.info("Данные загружены")


if __name__ == "__main__":
	main()
