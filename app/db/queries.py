import csv
import logging
from typing import Generator, List, Tuple, Any

from app.db.client import client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def row_reader(path: str) -> Generator:
	"""Читаем csv файл и возвращаем генератор"""
	with open(path) as table:
		csv_reader = csv.reader(table)
		next(csv_reader)
		for line in csv_reader:
			yield line


def health_check() -> None:
	"""Поверяем что бд работает"""
	try:
		client.execute('DROP TABLE IF EXISTS lenta')
		client.execute(
			'CREATE TABLE lenta ('
			'url String, title String, '
			'text String, topic String, '
			'tags String, date String) '
			'ENGINE = Log()'
		)
		insert_query = "INSERT INTO lenta (url, title, text, topic, tags, date) VALUES"
		values = [
			('https://example.com/news/1', 'News 1', 'Text 1', 'Topic 1', 'Tag3', '1914/09/16'),
			('https://example.com/news/2', 'News 2', 'Text 2', 'Topic 2', 'Tag3', '1914/09/16')
		]

		client.execute(insert_query, values)
		logger.info(client.execute('SELECT * FROM lenta'))
	except Exception as e:
		logger.error(e)


def df_to_clickhouse(path: str) -> str:
	"""Создаем таблицу если ее еще нет и запиливаем в нее данные"""
	try:
		client.execute(
			'CREATE TABLE IF NOT EXISTS lenta ('
			'url String, title String, '
			'text String, topic String, '
			'tags String, date String) '
			'ENGINE = Log()'
		)
		client.execute(
			'INSERT INTO lenta (url, title, text, topic, tags, date) VALUES',
			(line for line in row_reader(path))
		)
		rows = client.execute(
			"SELECT count() as rows FROM lenta"
		)
		logger.info(f"{rows[0][0]} строк загружено в ClickHouse")
		return f"{rows[0][0]} строк загружено в ClickHouse"
	except Exception as e:
		logger.error(e)


def get_100() -> List[Tuple[Any]]:
	"""Запрос на топ 100 слов"""
	data = client.execute(
		"""
		SELECT word, count
		FROM (
			SELECT word, count(*) AS count
			FROM lenta
			ARRAY JOIN splitByChar(' ', CONCAT(url, ' ', title, ' ', text, ' ', topic, ' ', tags, ' ', date)) AS word
			WHERE word not in ('', ' ', '-', '_', '.', ',', '!', '?', '/', ':', ';', '—')
			GROUP BY word
			)
		ORDER BY count DESC
		LIMIT 100
		"""
	)
	return data
