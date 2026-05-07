"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.
"""

import pytest


class TestUnregisterActivities:
    """Tests for activity unregistration functionality."""
    
    def test_unregister_successful(self, client):
        """Test successful unregistration from an activity."""
        email = "michael@mergington.edu"  # Already in Chess Club
        
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]
        assert email in data["message"]
    
    def test_unregister_removes_from_participants(self, client):
        """Test that unregister actually removes email from participants list."""
        email = "daniel@mergington.edu"  # Already in Chess Club
        
        # Unregister
        client.delete(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        
        # Check if removed
        response = client.get("/activities")
        data = response.json()
        assert email not in data["Chess Club"]["participants"]
    
    def test_unregister_nonexistent_activity(self, client):
        """Test unregister fails for non-existent activity."""
        response = client.delete(
            "/activities/Nonexistent Activity/unregister",
            params={"email": "test@mergington.edu"}
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]
    
    def test_unregister_not_signed_up(self, client):
        """Test unregister fails if email is not in participants."""
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "notsignedup@mergington.edu"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"]
    
    def test_unregister_after_signup(self, client):
        """Test full signup -> unregister cycle."""
        email = "cycletest@mergington.edu"
        
        # Signup
        signup_response = client.post(
            "/activities/Art Studio/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Verify added
        activities_response = client.get("/activities")
        data = activities_response.json()
        assert email in data["Art Studio"]["participants"]
        
        # Unregister
        unregister_response = client.delete(
            "/activities/Art Studio/unregister",
            params={"email": email}
        )
        assert unregister_response.status_code == 200
        
        # Verify removed
        activities_response2 = client.get("/activities")
        data2 = activities_response2.json()
        assert email not in data2["Art Studio"]["participants"]