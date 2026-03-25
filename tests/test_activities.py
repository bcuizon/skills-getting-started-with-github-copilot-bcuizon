"""
Unit tests for the Mergington High School API endpoints.

Each test follows the Arrange-Act-Assert (AAA) pattern:
- Arrange: Set up test data and fixtures
- Act: Execute the endpoint being tested
- Assert: Verify expected outcomes (status codes, response data, state changes)
"""

import pytest
from fastapi.testclient import TestClient


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all available activities.

        Arrange: Prepare the TestClient
        Act: Send GET request to /activities
        Assert: Verify response contains all expected activities
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Music Ensemble",
            "Debate Club",
            "Science Lab",
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        for activity in expected_activities:
            assert activity in data


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client):
        """
        Test that a student can successfully sign up for an activity.

        Arrange: Prepare test data for signup
        Act: Send POST request to signup endpoint
        Assert: Verify participant is added and success message is returned
        """
        # Arrange
        activity_name = "Chess Club"
        email = "new_student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_activity_not_found(self, client):
        """
        Test that signup fails with 404 when activity doesn't exist.

        Arrange: Prepare test data with non-existent activity
        Act: Send POST request to signup for non-existent activity
        Assert: Verify 404 error is returned
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_student_already_registered(self, client):
        """
        Test that signup fails with 400 when student is already registered.

        Arrange: Identify an activity and existing participant
        Act: Attempt to sign up the same student again
        Assert: Verify 400 error is returned
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered in initial data

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_success(self, client):
        """
        Test that a student can successfully unregister from an activity.

        Arrange: Identify an existing participant in an activity
        Act: Send DELETE request to unregister endpoint
        Assert: Verify participant is removed and success message is returned
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_activity_not_found(self, client):
        """
        Test that unregister fails with 404 when activity doesn't exist.

        Arrange: Prepare test data with non-existent activity
        Act: Send DELETE request to unregister from non-existent activity
        Assert: Verify 404 error is returned
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_student_not_registered(self, client):
        """
        Test that unregister fails with 400 when student is not registered.

        Arrange: Identify an activity and non-participant email
        Act: Attempt to unregister a student who isn't registered
        Assert: Verify 400 error is returned
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not registered" in data["detail"]
