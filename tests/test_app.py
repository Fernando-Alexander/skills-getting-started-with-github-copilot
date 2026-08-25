from src.app import activities


def test_get_activities_returns_available_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json()["Chess Club"]["description"] == (
        "Learn strategies and compete in chess tournaments"
    )


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_static_index_is_available(client):
    response = client.get("/static/index.html")

    assert response.status_code == 200
    assert "<html" in response.text.lower()


def test_signup_adds_participant(client):
    response = client.post(
        "/activities/Soccer Team/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up student@mergington.edu for Soccer Team"
    }
    assert "student@mergington.edu" in activities["Soccer Team"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    email = "student@mergington.edu"
    activities["Soccer Team"]["participants"].append(email)

    response = client.post("/activities/Soccer Team/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert activities["Soccer Team"]["participants"].count(email) == 1


def test_signup_rejects_unknown_activity(client):
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_requires_email(client):
    response = client.post("/activities/Soccer Team/signup")

    assert response.status_code == 422


def test_unregister_removes_participant(client):
    email = "student@mergington.edu"
    activities["Soccer Team"]["participants"].append(email)

    response = client.delete("/activities/Soccer Team/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered student@mergington.edu from Soccer Team"
    }
    assert email not in activities["Soccer Team"]["participants"]


def test_unregister_rejects_unknown_participant(client):
    response = client.delete(
        "/activities/Soccer Team/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_rejects_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"