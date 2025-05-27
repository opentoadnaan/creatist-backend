from __future__ import annotations

import os
from typing import Optional, Union
from uuid import UUID

from click import Option
from dotenv import load_dotenv
from supabase import AsyncClient, create_async_client

from src.models import UserModel

load_dotenv()


class UserHandler:
    supabase: AsyncClient

    async def init(self):
        self.supabase = await create_async_client(
            os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY")
        )

    async def fetch_user(
        self,
        *,
        user_id: Union[UUID, str, None] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Optional[UserModel]:
        if user_id:
            return await self._fetch_user_by_id(user_id)

        if email and password:
            return await self._fetch_user_by_email(email, password)

    async def create_user(self, *, user: UserModel):
        payload = user.model_dump(mode="json")

        response = await self.supabase.table("users").insert(payload).execute()

    async def update_user(
        self, *, user_id: Union[UUID, str], update_payload: UserModel
    ) -> Optional[UserModel]:
        payload = update_payload.model_dump(mode="json")
        _id = payload.pop("id", user_id)

        assert _id == user_id

        response = await (
            self.supabase.table("users").update(payload).eq("id", _id).execute()
        )

        return self._parse(response.data)

    async def _fetch_user_by_email(
        self, email: str, password: str
    ) -> Optional[UserModel]:
        response = await (
            self.supabase.table("users")
            .select("*")
            .eq("email", email)
            .eq("password", password)
            .execute()
        )

        return self._parse(response.data)

    async def _fetch_user_by_id(self, user_id):
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        response = await (
            self.supabase.table("users").select("*").eq("id", user_id).execute()
        )

        return self._parse(response.data)

    def _parse(self, response: list, count: int = 1):
        if len(response) == 0:
            return

        assert len(response) == count

        return UserModel(**response[0])
