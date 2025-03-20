
from .bll import BaseBll
from co6co_permissions.model.pos.other import sysConfigPO
from sqlalchemy import Select
from co6co_db_ext.db_utils import QueryOneCallable
import json as sysJson


class config_bll(BaseBll):
    async def query_config_value(self,  key: str, parseDict: bool = False) -> str | dict:
        select = (
            Select(sysConfigPO.value)
            .filter(sysConfigPO.code.__eq__(key))
        )
        call = QueryOneCallable(self.session)
        result = await call(select, isPO=False)
        result: str = result.get("value")
        if parseDict:
            result = sysJson.loads(result)
        return result
