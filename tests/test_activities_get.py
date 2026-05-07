"""
Tests for the GET /activities endpoint.
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""
    
    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns HTTP 200."""
        response = client.get("/activities")
        assert response.status_code == 200
    
    def test_get_activities_returns_dict(self, client):
        """Test that response is a dictionary."""
        response = client.get("/activities")
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_activities_contains_chess_club(self, client):
        """Test that Chess Club is in the activities."""
        response = client.get("/activities")
        data = response.json()
        assert "Chess Club" in data
    
    def test_get_activities_has_correct_count(self, client):
        """Test that we have 9 activities."""
        response = client.get("/activities")
        data = response.json()
        assert len(data) == 9
    
    def test_get_activities_chess_club_structure(self, client):
        """Test that Chess Club has correct structure."""
        response = client.get("/activities")
        data = response.json()
        chess_club = data["Chess Club"]
        
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)
        assert chess_club["max_participants"] == 12
    
    def test_get_activities_participants_are_lists(self, client):
        """Test that all activities have participants as lists."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list), \
                f"Activity '{activity_name}' participants is not a list"