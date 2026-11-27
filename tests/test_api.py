def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_team_crud_and_duplicate_validation(client, auth_headers):
    headers = auth_headers("admin_crud", "admin")

    res = client.post("/api/v1/teams/", json={"name": "Samarqand United", "city": "Samarqand"}, headers=headers)
    assert res.status_code == 201
    team_id = res.json()["id"]

    dup = client.post("/api/v1/teams/", json={"name": "Samarqand United", "city": "Samarqand"}, headers=headers)
    assert dup.status_code == 400

    get_res = client.get(f"/api/v1/teams/{team_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Samarqand United"

    del_res = client.delete(f"/api/v1/teams/{team_id}", headers=headers)
    assert del_res.status_code == 204
    assert client.get(f"/api/v1/teams/{team_id}").status_code == 404


def test_player_registration_and_duplicate_jersey(client, auth_headers):
    headers = auth_headers("org_players", "organizer")
    team_id = client.post(
        "/api/v1/teams/", json={"name": "Registon FC", "city": "Samarqand"}, headers=headers
    ).json()["id"]

    p1 = client.post(
        "/api/v1/players/",
        json={"full_name": "Azizbek Karimov", "team_id": team_id, "jersey_number": 10, "position": "Hujumchi"},
        headers=headers,
    )
    assert p1.status_code == 201

    p_dup = client.post(
        "/api/v1/players/",
        json={"full_name": "Jasur Aliyev", "team_id": team_id, "jersey_number": 10, "position": "Yarim himoyachi"},
        headers=headers,
    )
    assert p_dup.status_code == 400

    players = client.get(f"/api/v1/teams/{team_id}/players")
    assert players.status_code == 200
    assert len(players.json()) == 1


def test_full_tournament_flow_and_notifications(client, auth_headers):
    headers = auth_headers("org_tour", "organizer")
    t1 = client.post(
        "/api/v1/teams/", json={"name": "Samarqand United", "city": "Samarqand"}, headers=headers
    ).json()["id"]
    t2 = client.post(
        "/api/v1/teams/", json={"name": "Registon FC", "city": "Samarqand"}, headers=headers
    ).json()["id"]

    tour = client.post(
        "/api/v1/tournaments/",
        json={"name": "Samarqand Havaskorlar Kubogi", "season": "2026"},
        headers=headers,
    )
    assert tour.status_code == 201
    tour_id = tour.json()["id"]

    match = client.post(
        "/api/v1/matches/",
        json={"tournament_id": tour_id, "home_team_id": t1, "away_team_id": t2},
        headers=headers,
    )
    assert match.status_code == 201
    match_id = match.json()["id"]

    result = client.patch(
        f"/api/v1/matches/{match_id}/result",
        json={"home_score": 3, "away_score": 1},
        headers=headers,
    )
    assert result.status_code == 200
    assert result.json()["status"] == "finished"

    standings = client.get(f"/api/v1/tournaments/{tour_id}/standings?scoring=bonus")
    assert standings.status_code == 200
    table = standings.json()
    assert table[0]["team_name"] == "Samarqand United"
    assert table[0]["points"] == 4

    notifs = client.get("/api/v1/notifications/")
    assert notifs.status_code == 200
    event_types = [n["event_type"] for n in notifs.json()]
    assert "TeamRegisteredEvent" in event_types
    assert "MatchFinishedEvent" in event_types