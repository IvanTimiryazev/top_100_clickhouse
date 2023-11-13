from clickhouse_driver import Client

from app.core.config import settings

client = Client(
	host=settings.CLICKHOUSE_URI
)