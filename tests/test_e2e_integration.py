def test_ui_and_static_assets_served(client):
    ui = client.get("/ui")
    assert ui.status_code == 200
    assert "Havaskor Futbol Tizimi" in ui.text

    css = client.get("/static/styles.css")
    assert css.status_code == 200

    js = client.get("/static/app.js")
    assert js.status_code == 200


def test_complete_end_to_end_system_scenario(client, auth_headers):
    # 1. Turli rollardagi foydalanuvchilar (RBAC)
    admin_headers = auth_headers("e2e_admin", "admin")
    org_headers = auth_headers("e2e_org", "organizer")
    viewer_headers = auth_headers("e2e_viewer", "viewer")

    # 2. Viewer jamoa yarata olmaydi -> 403
    assert (
        client.post("/api/v1/teams/", json={"name": "Taqiqlangan FC", "city": "Samarqand"}, headers=viewer_headers)
        .status_code
        == 403
    )

    # 3. Organizer 2 ta jamoa, o'yinchi va turnir yaratadi
    t1 = client.post(
        "/api/v1/teams/", json={"name": "Samarqand United", "city": "Samarqand"}, headers=org_headers
    ).json()["id"]
    t2 = client.post(
        "/api/v1/teams/", json={"name": "Registon FC", "city": "Samarqand"}, headers=org_headers
    ).json()["id"]

    p1 = client.post(
        "/api/v1/players/",
        json={"full_name": "Azizjon Toirov", "team_id": t1, "jersey_number": 7, "position": "Hujumchi"},
        headers=org_headers,
    )
    assert p1.status_code == 201

    tour_id = client.post(
        "/api/v1/tournaments/",
        json={"name": "Samarqand Kuzgi Kubogi", "season": "2026"},
        headers=org_headers,
    ).json()["id"]

    # 4. Uchrashuv belgilash va 4:1 hisobini kiritish
    match_id = client.post(
        "/api/v1/matches/",
        json={"tournament_id": tour_id, "home_team_id": t1, "away_team_id": t2},
        headers=org_headers,
    ).json()["id"]

    res = client.patch(
        f"/api/v1/matches/{match_id}/result",
        json={"home_score": 4, "away_score": 1},
        headers=org_headers,
    )
    assert res.status_code == 200

    # 5. Standart (3 ochko) va Bonus (4 ochko) jadvalini taqqoslash
    std = client.get(f"/api/v1/tournaments/{tour_id}/standings?scoring=standard").json()
    bonus = client.get(f"/api/v1/tournaments/{tour_id}/standings?scoring=bonus").json()
    assert std[0]["points"] == 3
    assert bonus[0]["points"] == 4

    # 6. EventBus bildirishnomalari va Monitoring ko'rsatkichlari
    notifs = client.get("/api/v1/notifications/").json()
    assert len(notifs) >= 3

    health = client.get("/api/v1/monitoring/health/detailed").json()
    assert health["status"] == "healthy"
    assert health["database"] == "connected"

    # 7. Admin jurnallarni ko'ra oladi
    logs = client.get("/api/v1/monitoring/logs?limit=5", headers=admin_headers)
    assert logs.status_code == 200