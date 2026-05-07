"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


class TestSignupActivities:
    """Tests for activity signup functionality."""
    
    def test_signup_successful(self, client):
        """Test successful signup for an activity."""
        email = "newstudent@mergington.edu"
        response = client.post(
            "/activities/Programming Class/signup",
            params={"email": email}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
        assert email in data["message"]
    
    def test_signup_adds_to_participants(self, client):
        """Test that signup actually adds email to participants list."""
        email = "signuptest@mergington.edu"
        
        # Signup
        client.post(
            "/activities/Gym Class/signup",
            params={"email": email}
        )
        
        # Check if added
        response = client.get("/activities")
        data = response.json()
        assert email in data["Gym Class"]["participants"]
    
    def test_signup_nonexistent_activity(self, client):
        """Test signup fails for non-existent activity."""
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": "test@mergington.edu"}
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]
    
    def test_signup_duplicate_email(self, client):
        """Test that duplicate signup is rejected."""
        email = "michael@mergington.edu"  # Already in Chess Club
        
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]
    
    def test_signup_multiple_activities(self, client):
        """Test that student can signup for multiple activities."""
        email = "multiactivity@mergington.edu"
        
        # Signup for two activities
        response1 = client.post(
            "/activities/Soccer Team/signup",
            params={"email": email}
        )
        response2 = client.post(
            "/activities/Swim Club/signup",
            params={"email": email}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify in both activities
        activities_response = client.get("/activities")
        data = activities_response.json()
        assert email in data["Soccer Team"]["participants"]
        assert email in data["Swim Club"]["participants"]