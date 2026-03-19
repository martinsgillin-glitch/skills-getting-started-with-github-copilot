"""API tests for the Mergington High School activities backend."""


class TestGetActivities:
    """Tests for GET /activities."""

    def test_get_activities_returns_200(self, client):
        # Arrange (client fixture)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_get_activities_contains_known_activity(self, client):
        # Arrange
        expected = "Chess Club"

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert expected in data


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup."""

    def test_signup_success(self, client):
        # Arrange
        activity = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity}"

    def test_signup_duplicate_returns_400(self, client):
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_missing_activity_returns_404(self, client):
        # Arrange
        activity = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestDeleteParticipant:
    """Tests for DELETE /activities/{activity_name}/participants."""

    def test_delete_participant_success(self, client):
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity}"

    def test_delete_nonexistent_participant_returns_404(self, client):
        # Arrange
        activity = "Chess Club"
        email = "not@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]
