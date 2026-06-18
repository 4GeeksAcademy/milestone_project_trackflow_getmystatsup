def _register(client, email: str, password: str = "strongpass"):
    return client.post("/auth/register", json={"email": email, "password": password})


def _token_for(client, email: str, password: str = "strongpass") -> str:
    response = client.post("/auth/login", json={"email": email, "password": password})
    return response.json()["access_token"]


def test_users_list_requires_auth(client):
    response = client.get("/users")
    assert response.status_code == 401


def test_public_users_create_returns_user(client, tinydb):
    response = client.post("/users", json={"email": "public@example.com", "password": "strongpass"})
    assert response.status_code == 201
    assert response.json()["email"] == "public@example.com"
    stored = tinydb.table("users").get(doc_id=1)
    assert stored["hashed_password"] != "strongpass"


def test_user_cannot_update_another_user(client):
    _register(client, "owner1@example.com")
    _register(client, "owner2@example.com")

    token = _token_for(client, "owner1@example.com")
    response = client.put(
        "/users/2",
        json={"is_active": False},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_user_can_update_self(client):
    _register(client, "self@example.com")
    token = _token_for(client, "self@example.com")
    response = client.put(
        "/users/1",
        json={"is_active": False},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["is_active"] is False


def test_duplicate_email_conflict(client):
    _register(client, "dup@example.com")
    response = client.post("/users", json={"email": "dup@example.com", "password": "strongpass"})
    assert response.status_code == 409