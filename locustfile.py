import random
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
        user = {
            "email": email,
            "password": password
        }
        if random.randint(1, 10) > 4:
            user['first_name'] = str(uuid.uuid4())
            user['last_name'] = str(uuid.uuid4())

        resp = self.client.post("/api/admin/users", json=user)
        assert resp.status_code == 201, resp.status_code

        resp = self.client.post("/api/admin/login", json={
            "email": user['email'],
            "password": user['password']
        })
        assert resp.status_code == 200, resp.status_code
        body = resp.json()
        access_token = body['access_token']

        resp = self.client.put(
            "/api/admin/users",
            headers={
                'Authorization': f'Bearer {access_token}'
            },
            json={
                "password": 'justanewpassword'
            }
        )
        resp = self.client.put(
            "/api/admin/users",
            headers={
                'Authorization': f'Bearer {access_token}'
            },
            json={
                "first_name": 'IVAN'
            }
        )
        resp = self.client.put(
            "/api/admin/users",
            headers={
                'Authorization': f'Bearer {access_token}'
            },
            json={
                "last_name": 'IVANOV'
            }
        )
        assert resp.status_code == 200, resp.status_code

        resp = self.client.delete(
            "/api/admin/users",
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        assert resp.status_code == 204, resp.status_code
