"""
Unit tests for Contact API endpoints.
Tests: POST contact message, GET all messages, GET by ID, PATCH mark as read, DELETE.
"""
import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock


@pytest.mark.unit
@pytest.mark.asyncio
class TestContactAPI:
    """Test suite for /api/v1/contact endpoints."""
    
    @patch('app.routers.contact.email_service.send_contact_email')
    async def test_send_contact_message_success(self, mock_email, client: AsyncClient, sample_contact_message_data):
        """Test successful contact message submission."""
        mock_email.return_value = True
        
        response = await client.post("/api/v1/contact/", json=sample_contact_message_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_contact_message_data["name"]
        assert data["email"] == sample_contact_message_data["email"]
        assert data["message"] == sample_contact_message_data["message"]
        assert data["is_read"] is False
        assert "id" in data
        assert "created_at" in data
        
        # Verify email was called
        mock_email.assert_called_once()
    
    async def test_send_contact_message_missing_required_fields(self, client: AsyncClient):
        """Test sending contact message with missing required fields."""
        incomplete_data = {"name": "John"}
        response = await client.post("/api/v1/contact/", json=incomplete_data)
        assert response.status_code == 422
    
    async def test_send_contact_message_invalid_email(self, client: AsyncClient, sample_contact_message_data):
        """Test sending contact message with invalid email."""
        sample_contact_message_data["email"] = "invalid-email"
        response = await client.post("/api/v1/contact/", json=sample_contact_message_data)
        assert response.status_code == 422
    
    @patch('app.routers.contact.email_service.send_contact_email')
    async def test_send_contact_message_email_failure_still_saves(self, mock_email, client: AsyncClient, sample_contact_message_data):
        """Test that message is saved even if email fails."""
        mock_email.side_effect = Exception("Email server down")
        
        response = await client.post("/api/v1/contact/", json=sample_contact_message_data)
        # Message should still be saved
        assert response.status_code == 201
        assert response.json()["name"] == sample_contact_message_data["name"]
    
    @patch('app.routers.contact.email_service.send_contact_email')
    async def test_get_all_messages_empty(self, mock_email, client: AsyncClient):
        """Test getting all contact messages when none exist."""
        response = await client.get("/api/v1/contact/messages")
        assert response.status_code == 200
        assert response.json() == []
    
    @patch('app.routers.contact.email_service.send_contact_email')
    async def test_get_all_messages_with_records(self, mock_email, client: AsyncClient, sample_contact_message_data):
        """Test getting all contact messages."""
        mock_email.return_value = True
        
        # Create multiple messages
        await client.post("/api/v1/contact/", json=sample_contact_message_data)
        
        second_message = sample_contact_message_data.copy()
        second_message["name"] = "Jane Doe"
        second_message["email"] = "jane@example.com"
        await client.post("/api/v1/contact/", json=second_message)
        
        # Get all
        response = await client.get("/api/v1/contact/messages")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    @patch('app.routers.contact.email_service.send_contact_email')
    async def test_filter_messages_by_read_status(self, mock_email, client: AsyncClient, sample_contact_message_data):
        """Test filtering messages by read status."""
        mock_email.return_value = True
        
        # Create message
        create_response = await client.post("/api/v1/contact/", json=sample_contact_message_data)
        message_id = create_response.json()["id"]
        
        # Mark as read
        await client.patch(f"/api/v1/contact/messages/{message_id}/read")
        
        # Create another unread message
        second_message = sample_contact_message_data.copy()
        second_message["email"] = "another@example.com"
        await client.post("/api/v1/contact/", json=second_message)
        
        # Filter unread
        response = await client.get("/api/v1/contact/messages?is_read=false")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["is_read"] is False
        
        # Filter read
        response = await client.get("/api/v1/contact/messages?is_read=true")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["is_read"] is True
    
    @patch('app.routers.contact.email_service.send_contact_email')
    async def test_get_message_by_id_success(self, mock_email, client: AsyncClient, sample_contact_message_data):
        """Test getting contact message by ID."""
        mock_email.return_value = True
        
        # Create message
        create_response = await client.post("/api/v1/contact/", json=sample_contact_message_data)
        created_id = create_response.json()["id"]
        
        # Get by ID
        response = await client.get(f"/api/v1/contact/messages/{created_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_id
        assert data["name"] == sample_contact_message_data["name"]
    
    async def test_get_message_by_id_not_found(self, client: AsyncClient):
        """Test getting message with non-existent ID."""
        response = await client.get("/api/v1/contact/messages/9999")
        assert response.status_code == 404
    
    @patch('app.routers.contact.email_service.send_contact_email')
    async def test_mark_message_as_read_success(self, mock_email, client: AsyncClient, sample_contact_message_data):
        """Test marking message as read."""
        mock_email.return_value = True
        
        # Create message
        create_response = await client.post("/api/v1/contact/", json=sample_contact_message_data)
        created_id = create_response.json()["id"]
        assert create_response.json()["is_read"] is False
        
        # Mark as read
        response = await client.patch(f"/api/v1/contact/messages/{created_id}/read")
        assert response.status_code == 200
        data = response.json()
        assert data["is_read"] is True
    
    async def test_mark_message_as_read_not_found(self, client: AsyncClient):
        """Test marking non-existent message as read."""
        response = await client.patch("/api/v1/contact/messages/9999/read")
        assert response.status_code == 404
    
    @patch('app.routers.contact.email_service.send_contact_email')
    async def test_delete_message_success(self, mock_email, client: AsyncClient, sample_contact_message_data):
        """Test successful message deletion."""
        mock_email.return_value = True
        
        # Create message
        create_response = await client.post("/api/v1/contact/", json=sample_contact_message_data)
        created_id = create_response.json()["id"]
        
        # Delete message
        response = await client.delete(f"/api/v1/contact/messages/{created_id}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"].lower()
        
        # Verify deletion
        get_response = await client.get(f"/api/v1/contact/messages/{created_id}")
        assert get_response.status_code == 404
    
    async def test_delete_message_not_found(self, client: AsyncClient):
        """Test deleting message that doesn't exist."""
        response = await client.delete("/api/v1/contact/messages/9999")
        assert response.status_code == 404
    
    @patch('app.routers.contact.email_service.send_contact_email')
    async def test_messages_ordered_by_created_at_desc(self, mock_email, client: AsyncClient, sample_contact_message_data):
        """Test that messages are returned newest first."""
        mock_email.return_value = True
        
        # Create multiple messages
        messages = ["First", "Second", "Third"]
        for name in messages:
            data = sample_contact_message_data.copy()
            data["name"] = name
            data["email"] = f"{name.lower()}@example.com"
            await client.post("/api/v1/contact/", json=data)
        
        # Get all messages
        response = await client.get("/api/v1/contact/messages")
        data = response.json()
        assert len(data) == 3
        # Should be reversed (newest first)
        assert data[0]["name"] == "Third"
        assert data[1]["name"] == "Second"
        assert data[2]["name"] == "First"
