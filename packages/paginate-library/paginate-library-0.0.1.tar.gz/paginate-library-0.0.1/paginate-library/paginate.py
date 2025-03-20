from math import ceil
from typing import Type
from schemas import paginate_shema as ps

from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status


def paginate(
        dto: ps.PaginationRequestBodySchema,
        data: list = None,
        data_schema: Type[BaseModel] = None,
):
    """
    Производит пагинацию для страницы
    dto - тело запроса с пагинацией
    data - список элементов
    """
    total = len(data)
    total_page = ceil(total / dto.page_size)

    if data is None or dto.page > total_page:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if total > dto.page_size:
        start_item = (dto.page - 1) * dto.page_size
        final_item = dto.page * dto.page_size
        data = data[start_item:final_item]

    if data_schema:
        data = [data_schema.from_orm(single_data) for single_data in data]

    response = {
        "current_page": dto.page,
        "total_pages": total_page,
        "data": data,
    }
    return response
