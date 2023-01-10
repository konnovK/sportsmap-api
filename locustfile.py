import time
import uuid

from locust import HttpUser, task


class PingUser(HttpUser):
    @task
    def ping(self):
        self.client.get("/ping")


class LoginUser(HttpUser):
    @task
    def reg_log_del(self):
        now = time.time()
        email = f"user{now}{uuid.uuid4()}@example.com"
        password = "hackme"
        resp = self.client.post("/api/admin/users", json={
            "email": email,
            "password": password
        })
        assert resp.status_code == 201, resp.status_code

        resp = self.client.post("/api/admin/login", json={
            "email": email,
            "password": password
        })
        assert resp.status_code == 200, resp.status_code
        body = resp.json()
        access_token, refresh_token = body['access_token'], body['access_token']

        resp = self.client.delete(
            "/api/admin/users",
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        assert resp.status_code == 204, resp.status_code
