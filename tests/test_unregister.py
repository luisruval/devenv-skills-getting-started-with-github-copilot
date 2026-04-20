def test_unregister_success(client):
    existing_email = "michael@mergington.edu"

    response = client.delete("/activities/Chess Club/unregister", params={"email": existing_email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {existing_email} from Chess Club"}

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert existing_email not in participants


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete(
        "/activities/Unknown Club/unregister",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_non_member_returns_400(client):
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "newstudent@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
