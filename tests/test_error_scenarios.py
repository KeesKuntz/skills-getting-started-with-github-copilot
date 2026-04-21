import pytest


class TestErrorScenarios:
    """Test error handling and edge cases"""
    
    def test_signup_with_special_characters_in_email(self, client):
        """Test signup with special characters in email (URL encoded)"""
        response = client.post(
            "/activities/Basketball%20Team/signup?email=test%2Bactive@example.com"
        )
        assert response.status_code == 200
        assert "test+active@example.com" in response.json()["message"]
    
    def test_activity_with_spaces_in_name(self, client):
        """Test activities with spaces in names are handled correctly"""
        response = client.get("/activities")
        data = response.json()
        assert "Basketball Team" in data
        assert "Swimming Club" in data
    
    def test_empty_activity_has_empty_participants_list(self, client):
        """Test that empty activities have empty participants list"""
        response = client.get("/activities")
        data = response.json()
        assert data["Basketball Team"]["participants"] == []
    
    def test_response_contains_correct_status_codes(self, client):
        """Test that various error conditions return correct status codes"""
        # 404 for non-existent activity
        response = client.post(
            "/activities/Invalid/signup?email=test@example.com"
        )
        assert response.status_code == 404
        
        # 400 for duplicate signup
        client.post("/activities/Chess%20Club/signup?email=dup@example.com")
        response = client.post(
            "/activities/Chess%20Club/signup?email=dup@example.com"
        )
        assert response.status_code == 400
        
        # 200 for successful operations
        response = client.get("/activities")
        assert response.status_code == 200
    
    def test_unregister_existing_then_duplicate_attempt_fails(self, client):
        """Test that unregistering the same participant twice fails on second attempt"""
        email = "michael@mergington.edu"
        client.delete(f"/activities/Chess%20Club/unregister?email={email}")
        response = client.delete(f"/activities/Chess%20Club/unregister?email={email}")
        assert response.status_code == 404
