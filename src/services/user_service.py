from typing import Optional, Any, List

from src.data.dal import UserDAL
from src.schema import User


class UserService:
    def __init__(self, user_dal: UserDAL) -> None:
        self.__user_dal = user_dal

    async def get_users(self, **params: Optional[Any]) -> Optional[List[User]]:
        return await self.__user_dal.get_all(**params)
    
    async def get_one_user(self, **params: Optional[Any]) -> Optional[User]:
        return await self.__user_dal.get_one(**params)
    
    async def update_user(self, user_id: int, **values) -> None:
        await self.__user_dal.update(user_id=user_id, **values)
