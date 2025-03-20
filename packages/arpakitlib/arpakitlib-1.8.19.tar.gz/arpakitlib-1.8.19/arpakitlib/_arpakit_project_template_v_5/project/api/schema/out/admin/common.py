import datetime as dt

from project.api.schema.common import BaseSO


class SimpleDBMAdminSO(BaseSO):
    id: int
    long_id: str
    slug: str | None
    creation_dt: dt.datetime
