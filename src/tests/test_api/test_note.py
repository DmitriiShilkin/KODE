from typing import Callable

from httpx import AsyncClient

from models import User, Note
from schemas.note import NoteCreate

ROOT_ENDPOINT = "/kode/v1/note/"


class TestNoteApi:
    async def test_get_multi(
        self,
        http_client: AsyncClient,
        user_fixture: User,
        user_fixture_2: User,
        note_fixture: Note,
        note_fixture_2: Note,
        get_auth_headers: Callable,
    ) -> None:
        user_auth_headers = await get_auth_headers(user_fixture)
        user_2_auth_headers = await get_auth_headers(user_fixture_2)
        response = await http_client.get(
            ROOT_ENDPOINT,
            headers=user_auth_headers,
        )
        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data) == 2

        response = await http_client.get(
            ROOT_ENDPOINT,
            headers=user_2_auth_headers,
        )
        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data) == 0

        response = await http_client.get(
            ROOT_ENDPOINT,
        )
        assert response.status_code == 401

    async def test_create(
        self,
        http_client: AsyncClient,
        user_fixture: User,
        get_auth_headers: Callable,
    ) -> None:
        user_auth_headers = await get_auth_headers(user_fixture)
        create_data = NoteCreate(text="Test note text")
        response = await http_client.post(
            ROOT_ENDPOINT,
            json=create_data.model_dump(),
            headers=user_auth_headers,
        )
        assert response.status_code == 201
        response_data = response.json()
        assert create_data.text == response_data["text"]

        response = await http_client.post(
            ROOT_ENDPOINT,
            json=create_data.model_dump(),
        )
        assert response.status_code == 401
