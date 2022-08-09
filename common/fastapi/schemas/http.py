from typing import Dict, Union

from common.fastapi.schemas import BaseSchema

HTTP_404_DETAIL = dict(detail='Detail')
HTTP_200_UPDATED = dict(detail='Updated')
HTTP_200_REMOVED = dict(detail='Removed')
HTTP_200_ACCEPTED = dict(detail='Accepted')
HTTP_404_CREATED = dict(detail='Created')


# HTTP_404_


class DetailModel(BaseSchema):
    detail: Union[str, Dict]


class HTTPResponseModel(BaseSchema):
    status_code: int
    detail: Dict
