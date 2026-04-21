import pytest


class TestGetActivities:
    """Test GET /activities endpoint"""
    
    def test_get_all_activities(self, client):
        """Test that GET /activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        assert "Basketball Team" in data
        assert "Swimming Club" in data
    
    def test_activities_have_required_fields(self, client):
        """Test that each activity has required fields"""
        response = client.get("/activities")
        data = response.json()
        for activity_name, activity_details in data.items():
            assert "description" in activity_details
            assert "schedule" in activity_details
            assert "max_participants" in activity_details
            assert "participants" in activity_details
            assert isinstance(activity_details["participants"], list)
    
    def test_participant_count_accuracy(self, client):
        """Test that participant counts are accurate"""
        response = client.get("/activities")
        data = response.json()
        assert len(data["Chess Club"]["participants"]) == 2
        assert len(data["Programming Class"]["participants"]) == 2
        assert len(data["Gym Class"]["participants"]) == 2
        assert len(data["Basketball Team"]["participants"]) == 0
        assert len(data["Swimming Club"]["participants"]) == 0


class TestSignupForActivity:
    """Test POST /activities/{activity_name}/signup endpoint"""
    
    def test_successful_signup(self, client):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Basketball%20Team/signup?email=john@example.com"
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "john@example.com" in data["message"]
    
    def test_signup_adds_participant_to_activity(self, client):
        """Test that signup actually adds participant to the activity"""
        client.post("/activities/Swimming%20Club/signup?email=test@example.com")
        response = client.get("/activities")
        data = response.json()
        assert "test@example.com" in data["Swimming Club"]["participants"]
    
    def test_duplicate_signup_returns_400(self, client):
        """Test that signing up twice returns 400 error"""
        client.post("/activities/Chess%20Club/signup?email=newstudent@example.com")
        response = client.post(
            "/activities/Chess%20Club/signup?email=newstudent@example.com"
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]
    
    def test_signup_for_nonexistent_activity_returns_404(self, client):
        """Test that signing up for non-existent activity returns 404"""
        response = client.post(
            "/activities/Nonexistent%20Activity/signup?email=test@example.com"
        )
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]
    
    def test_participant_count_increases_after_signup(self, client):
        """Test that participant count increases after signup"""
        response_before = client.get("/activities")
        count_before = len(response_before.json()["Swimming Club"]["participants"])
        
        client.post("/activities/Swimming%20Club/signup?email=new@example.com")
        
        response_after = client.get("/activities")
        count_after = len(response_after.json()["Swimming Club"]["participants"])
        
        assert count_after == count_before + 1


class TestUnregisterFromActivity:
    """Test DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_successful_unregister(self, client):
        """Test successful unregister from an activity"""
        response = client.delete(
            "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]
    
    def test_unregister_removes_participant_from_activity(self, client):
        """Test that unregister actually removes participant"""
        client.delete(
            "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
        )
        response = client.get("/activities")
        data = response.json()
        assert "michael@mergington.edu" not in data["Chess Club"]["participants"]
    
    def test_unregister_nonexistent_participant_returns_404(self, client):
        """Test that unregistering non-existent participant returns 404"""
        response = client.delete(
            "/activities/Chess%20Club/unregister?email=nonexistent@example.com"
        )
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]
    
    def test_unregister_from_nonexistent_activity_returns_404(self, client):
        """Test that unregistering from non-existent activity returns 404"""
        response = client.delete(
            "/activities/Nonexistent%20Activity/unregister?email=test@example.com"
        )
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"]
    
    def test_participant_count_decreases_after_unregister(self, client):
        """Test that participant count decreases after unregister"""
        response_before = client.get("/activities")
        count_before = len(response_before.json()["Chess Club"]["participants"])
        
        client.delete(
            "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
        )
        
        response_after = client.get("/activities")
        count_after = len(response_after.json()["Chess Club"]["participants"])
        
        assert count_after == count_before - 1
