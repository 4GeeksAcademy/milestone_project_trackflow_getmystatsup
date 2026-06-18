from datetime import timedelta

from app.core.security import create_access_token


def test_register_returns_token(client):
    response = client.post(
        "/auth/register",
        json={"email": "user1@example.com", "password": "strongpass"},
    )
    assert response.status_code == 201
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_returns_token(client):
    client.post(
        "/auth/register",
        json={"email": "user2@example.com", "password": "strongpass"},
    )
    response = client.post(
        "/auth/login",
        json={"email": "user2@example.com", "password": "strongpass"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_protected_route_without_token_returns_401(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_protected_route_with_malformed_token_returns_401(client):
    response = client.get("/auth/me", headers={"Authorization": "Bearer not-a-token"})
    assert response.status_code == 401


def test_protected_route_with_expired_token_returns_401(client):
    client.post(
        "/auth/register",
        json={"email": "user3@example.com", "password": "strongpass"},
    )
    expired_token = create_access_token("user3@example.com", expires_delta=timedelta(minutes=-1))
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401


def test_auth_me_returns_current_user(client):
    client.post(
        "/auth/register",
        json={"email": "user4@example.com", "password": "strongpass"},
    )
    login = client.post(
        "/auth/login",
        json={"email": "user4@example.com", "password": "strongpass"},
    )
    token = login.json()["access_token"]
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "user4@example.com"
