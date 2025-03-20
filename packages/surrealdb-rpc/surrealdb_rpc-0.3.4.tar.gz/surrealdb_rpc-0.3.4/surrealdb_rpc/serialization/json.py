import datetime
import decimal
import json

from surrealdb_rpc.data_model.types import UUID, DateTime, Decimal, Duration
from surrealdb_rpc.serialization.abc import JSONSerializable


class SurrealJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        match obj:
            case uuid if isinstance(uuid, UUID):
                return str(uuid)
            case i if isinstance(i, (decimal.Decimal, Decimal)):
                return str(i)
            case td if isinstance(td, (datetime.timedelta, Duration)):
                return Duration.__str__(td)
            case dt if isinstance(dt, (datetime.datetime, DateTime)):
                return DateTime.__str__(dt)
            case thing if isinstance(thing, JSONSerializable):
                return thing.__json__()
            case _:
                return super().default(obj)
