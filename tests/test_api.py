def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_team_crud_and_duplicate_validation(client):
    # 1. Yangi jamoa yaratish
    res = client.post("/api/v1/teams/", json={"name": "Samarqand United", "city": "Samarqand"})
    assert res.status_code == 201
    team_id = res.json()["id"]

    # 2. Bir xil nomli jamoa qo'shishga urinish -> 400
    dup = client.post("/api/v1/teams/", json={"name": "Samarqand United", "city": "Samarqand"})
    assert dup.status_code == 400

    # 3. ID bo'yicha olish -> 200
    get_res = client.get(f"/api/v1/teams/{team_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Samarqand United"

    # 4. O'chirish -> 204, so'ngra qayta so'rash -> 404
    del_res = client.delete(f"/api/v1/teams/{team_id}")
    assert del_res.status_code == 204
    assert client.get(f"/api/v1/teams/{team_id}").status_code == 404


def test_player_registration_and_duplicate_jersey(client):
    team_id = client.post("/api/v1/teams/", json={"name": "Registon FC", "city": "Samarqand"}).json()["id"]

    p1 = client.post(
        "/api/v1/players/",
        json={"full_name": "Azizbek Karimov", "team_id": team_id, "jersey_number": 10, "position": "Hujumchi"},
    )
    assert p1.status_code == 201

    # Bir xil raqam -> 400
    p_dup = client.post(
        "/api/v1/players/",
        json={"full_name": "Jasur Aliyev", "team_id": team_id, "jersey_number": 10, "position": "Yarim himoyachi"},
    )
    assert p_dup.status_code == 400

    # Jamoa o'yinchilari ro'yxati
    players = client.get(f"/api/v1/teams/{team_id}/players")
    assert players.status_code == 200
    assert len(players.json()) == 1


def test_full_tournament_flow_and_notifications(client):
    # Jamoalar yaratish
    t1 = client.post("/api/v1/teams/", json={"name": "Samarqand United", "city": "Samarqand"}).json()["id"]
    t2 = client.post("/api/v1/teams/", json={"name": "Registon FC", "city": "Samarqand"}).json()["id"]

    # Turnir yaratish
    tour = client.post(
        "/api/v1/tournaments/",
        json={"name": "Samarqand Havaskorlar Kubogi", "season": "2026"},
    )
    assert tour.status_code == 201
    tour_id = tour.json()["id"]

    # Uchrashuv belgilash va hisob kiritish
    match = client.post(
        "/api/v1/matches/",
        json={"tournament_id": tour_id, "home_team_id": t1, "away_team_id": t2},
    )
    assert match.status_code == 201
    match_id = match.json()["id"]

    result = client.patch(f"/api/v1/matches/{match_id}/result", json={"home_score": 3, "away_score": 1})
    assert result.status_code == 200
    assert result.json()["status"] == "finished"

    # Turnir jadvali (bonus qoidasi bilan)
    standings = client.get(f"/api/v1/tournaments/{tour_id}/standings?scoring=bonus")
    assert standings.status_code == 200
    table = standings.json()
    assert table[0]["team_name"] == "Samarqand United"
    assert table[0]["points"] == 4

    # EventBus orqali hosil bo'lgan bildirishnomalarni tekshirish
    notifs = client.get("/api/v1/notifications/")
    assert notifs.status_code == 200
    event_types = [n["event_type"] for n in notifs.json()]
    assert "TeamRegisteredEvent" in event_types
    assert "MatchFinishedEvent" in event_types