import os
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.db.queries import get_100, df_to_clickhouse

router = APIRouter()


@router.get("/getWords", response_model=Dict[str, int], status_code=status.HTTP_200_OK)
def get_words() -> Any:
	try:
		data = get_100()
		data = dict(data)
		return JSONResponse(data)
	except Exception as e:
		raise HTTPException(
			detail=str(e),
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
		)


@router.get("/upload-data", response_model=Dict[str, str], status_code=status.HTTP_200_OK)
def get_data() -> Any:
	current_dir = os.path.dirname(os.path.realpath(__file__))
	file_path = os.path.abspath(os.path.join(current_dir, "../../../../data"))

	try:
		for file in os.listdir(file_path):
			file_name = os.path.join(file_path, file)
			data = df_to_clickhouse(file_name)

		return {"status": data}
	except Exception as e:
		raise HTTPException(detail=str(e), status_code=500)
