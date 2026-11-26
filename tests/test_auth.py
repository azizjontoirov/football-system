def test_register_login_and_me(client):
    reg = client.post(
        "/api/v1/auth/register",
        json={
            "username": "azizjon",
            "email": "azizjon@football.uz",
            "password": "mysecretpassword",
            "role": "viewer",
        },
    )
    assert reg.status_code == 201
    assert reg.json()["role"] == "viewer"

    login = client.post(
        "/api/v1/auth/login",
        data={"username": "azizjon", "password": "mysecretpassword"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["username"] == "azizjon"


def test_unauthenticated_write_returns_401(client):
    res = client.post("/api/v1/teams/", json={"name": "Ruxsatsiz FC", "city": "Samarqand"})
    assert res.status_code == 401


def test_rbac_viewer_cannot_create_team(client, auth_headers):
    viewer_headers = auth_headers("muxlis1", "viewer")
    res = client.post(
        "/api/v1/teams/",
        json={"name": "Muxlis FC", "city": "Samarqand"},
        headers=viewer_headers,
    )
    assert res.status_code == 403


def test_rbac_organizer_cannot_delete_team_but_admin_can(client, auth_headers):
    org_headers = auth_headers("tashkilotchi1", "organizer")
    admin_headers = auth_headers("superadmin1", "admin")

    # Organizer jamoa yarata oladi -> 201
    created = client.post(
        "/api/v1/teams/",
        json={"name": "Zarafshon FC", "city": "Samarqand"},
        headers=org_headers,
    )
    assert created.status_code == 201
    team_id = created.json()["id"]

    # Organizer jamoani o'chira olmaydi -> 403
    forbidden_del = client.delete(f"/api/v1/teams/{team_id}", headers=org_headers)
    assert forbidden_del.status_code == 403

    # Admin o'chira oladi -> 204
    allowed_del = client.delete(f"/api/v1/teams/{team_id}", headers=admin_headers)
    assert allowed_del.status_code == 204