from httpx import AsyncClient

from schemas.user import UserCreate


ROOT_ENDPOINT = "/kode/v1/user/"


class TestUserApi:
    async def test_create_user(
        self,
        http_client: AsyncClient,
    ):
        new_user_data = UserCreate(
            username="Test_username",
            first_name="Test_first_name",
            second_name="Test_second_name",
            email="test_email@gmail.com",
            password="password",
        )
        response = await http_client.post(
            ROOT_ENDPOINT, json=new_user_data.model_dump()
        )
        assert response.status_code == 201

        response_data = response.json()
        assert new_user_data.email == response_data["email"]
