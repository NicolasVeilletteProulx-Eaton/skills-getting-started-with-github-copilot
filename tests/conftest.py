"""
Pytest configuration and fixtures for the activities API tests.
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset activities to initial state before each test.
    This ensures test isolation by resetting the in-memory database.
    """
    # Store original activities
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Team sport practice and interschool matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["charlie@mergington.edu", "avril@mergington.edu"]
        },
        "Swim Club": {
            "description": "Swim training and water safety sessions",
            "schedule": "Mondays and Wednesdays, 4:30 PM - 6:00 PM",
            "max_participants": 16,
            "participants": ["liam@mergington.edu", "nina@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media art",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["grace@mergington.edu", "henry@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting workshops and school play rehearsals",
            "schedule": "Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 20,
            "participants": ["zoe@mergington.edu", "mason@mergington.edu"]
        },
        "Debate Team": {
            "description": "Prepare for debate competitions and improve public speaking",
            "schedule": "Tuesdays, 5:00 PM - 6:30 PM",
            "max_participants": 10,
            "participants": ["mia@mergington.edu", "ethan@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Hands-on science challenges and STEM competition prep",
            "schedule": "Thursdays, 3:45 PM - 5:15 PM",
            "max_participants": 15,
            "participants": ["ava@mergington.edu", "noah@mergington.edu"]
        }
    }
    
    # Clear current activities
    activities.clear()
    
    # Restore original activities
    activities.update(original_activities)
    
    yield  # Run the test
    
    # Cleanup (reset again after test)
    activities.clear()
    activities.update(original_activities)