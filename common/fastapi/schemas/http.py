from typing import Dict, Union

from common.fastapi.schemas import BaseSchema


# HTTP_404_


class DetailModel(BaseSchema):
    detail: Union[str, Dict]


class HTTPResponseModel(BaseSchema):
    status_code: int
    detail: Dict


HTTP_404_DETAIL = HTTPResponseModel(status_code=404, detail=dict(detail='HTTP 404 Detail Not Found'))
HTTP_200_UPDATED = HTTPResponseModel(status_code=200, detail=dict(detail='Updated'))
HTTP_200_REMOVED = HTTPResponseModel(status_code=200, detail=dict(detail='Removed'))
HTTP_200_ACCEPTED = HTTPResponseModel(status_code=200, detail=dict(detail='Accepted'))
HTTP_201_CREATED = HTTPResponseModel(status_code=200, detail=dict(detail='Created'))
