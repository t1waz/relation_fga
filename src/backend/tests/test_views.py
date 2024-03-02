from backend.tests.utils import make_test_get, make_test_post


class TestHealthCheck:
    ENDPOINT = "/health"

    async def test_health_check_endpoint_is_working(self):
        response = await make_test_get("/health")

        assert response.status_code == 200

    async def test_health_check_endpoint_post_request(self):
        response = await make_test_post(self.ENDPOINT, data={})

        assert response.status_code == 404


class TestObtainTokenView:
    ENDPOINT = "/auth/obtain-token"

    async def test_obtain_token_data_get_request(self):
        response = await make_test_get(self.ENDPOINT)

        assert response.status_code == 404

    async def test_obtain_token_data_missing_password(self, f_user_1):
        response = await make_test_post(self.ENDPOINT, data={"email": f_user_1.email})

        assert response.status_code == 400
        assert "request data" in response.text

    async def test_obtain_token_data_missing_email(self, f_user_1):
        response = await make_test_post(
            self.ENDPOINT, data={"password": f_user_1.password}
        )

        assert response.status_code == 400
        assert "request data" in response.text

    async def test_obtain_token_data_empty_data(self):
        response = await make_test_post(self.ENDPOINT, data={})

        assert response.status_code == 400
        assert "request data" in response.text

    async def test_obtain_token_data_email_not_a_email(self, f_user_1):
        response = await make_test_post(
            self.ENDPOINT, data={"email": "not_a_email", "password": f_user_1.password}
        )

        assert response.status_code == 400
        assert "request data" in response.text

    async def test_obtain_token_data_not_existing_email(self, f_user_1):
        response = await make_test_post(
            self.ENDPOINT,
            data={"email": "aa@example.com", "password": f_user_1.password},
        )

        assert response.status_code == 400
        assert "credentials" in response.text

    async def test_obtain_token_data_invalid_password(self, f_user_1):
        response = await make_test_post(
            self.ENDPOINT, data={"email": f_user_1.email, "password": "invalid"}
        )

        assert response.status_code == 400
        assert "credentials" in response.text

    async def test_obtain_token_data_valid_request(self, f_user_1):
        response = await make_test_post(
            self.ENDPOINT, data={"email": f_user_1.email, "password": f_user_1.password}
        )

        assert response.status_code == 201

        data = response.json()

        assert "access" in data
        assert "refresh" in data
        assert len(data["access"]) > 10
        assert len(data["refresh"]) > 10
