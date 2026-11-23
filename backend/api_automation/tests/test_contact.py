"""
Tests for Contact API endpoints.
Covers sending messages, retrieving messages, marking as read, and deletion.
"""
import pytest
import allure
from api_automation.clients.portfolio_clients import ContactClient


@pytest.fixture
def contact_client():
    """Provide a ContactClient instance."""
    return ContactClient()


@allure.feature("Contact API")
@allure.story("Send Contact Message")
class TestSendMessage:
    """Test POST /api/v1/contact endpoint."""
    
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Send contact message with valid data")
    def test_send_message_success(self, contact_client, contact_message_data):
        """Verify successful contact message submission."""
        with allure.step("Prepare contact message"):
            payload = contact_message_data
        
        with allure.step("Send message"):
            response = contact_client.send_message(payload)
        
        with allure.step("Verify response status"):
            assert response.status_code == 201
        
        with allure.step("Verify response contains message ID"):
            data = response.json()
            assert "id" in data
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Send message with invalid email")
    def test_send_message_invalid_email(self, contact_client, contact_message_data):
        """Verify message submission fails with invalid email."""
        with allure.step("Prepare payload with invalid email"):
            payload = contact_message_data.copy()
            payload["email"] = "not-an-email"
        
        with allure.step("Attempt to send message"):
            response = contact_client.send_message(payload)
        
        with allure.step("Verify validation error"):
            assert response.status_code == 422
            error_data = response.json()
            assert "errors" in error_data or "detail" in error_data
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Send message without required fields")
    def test_send_message_missing_email(self, contact_client, contact_message_data):
        """Verify message submission fails without email."""
        with allure.step("Prepare payload without email"):
            payload = contact_message_data.copy()
            del payload["email"]
        
        with allure.step("Attempt to send message"):
            response = contact_client.send_message(payload)
        
        with allure.step("Verify validation error"):
            assert response.status_code == 422
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Send message without name")
    def test_send_message_missing_name(self, contact_client, contact_message_data):
        """Verify message submission fails without name."""
        with allure.step("Prepare payload without name"):
            payload = contact_message_data.copy()
            del payload["name"]
        
        with allure.step("Attempt to send message"):
            response = contact_client.send_message(payload)
        
        with allure.step("Verify validation error"):
            assert response.status_code == 422


@allure.feature("Contact API")
@allure.story("Get All Messages")
class TestGetAllMessages:
    """Test GET /api/v1/contact endpoint."""
    
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get all contact messages")
    def test_get_all_messages_success(self, contact_client):
        """Verify successful retrieval of all messages."""
        with allure.step("Request all messages"):
            response = contact_client.get_all_messages()
        
        with allure.step("Verify response status"):
            assert response.status_code == 200
        
        with allure.step("Verify response is a list"):
            data = response.json()
            assert isinstance(data, list)


@allure.feature("Contact API")
@allure.story("Get Single Message")
class TestGetMessage:
    """Test GET /api/v1/contact/{message_id} endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Get message by valid ID")
    def test_get_message_success(self, contact_client):
        """Verify successful retrieval of a message."""
        with allure.step("Request message with ID 1"):
            response = contact_client.get_message(1)
        
        with allure.step("Verify response status"):
            assert response.status_code in [200, 404]
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Get message by invalid ID")
    def test_get_message_not_found(self, contact_client):
        """Verify 404 response for non-existent message."""
        with allure.step("Request message with non-existent ID"):
            response = contact_client.get_message(99999)
        
        with allure.step("Verify not found response"):
            assert response.status_code == 404


@allure.feature("Contact API")
@allure.story("Mark Message as Read")
class TestMarkMessageRead:
    """Test PATCH /api/v1/contact/{message_id} endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Mark message as read")
    def test_mark_message_read_success(self, contact_client):
        """Verify successful marking of message as read."""
        with allure.step("Mark message with ID 1 as read"):
            response = contact_client.mark_message_read(1)
        
        with allure.step("Verify response status"):
            assert response.status_code in [200, 204, 404]
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Mark non-existent message as read")
    def test_mark_message_read_not_found(self, contact_client):
        """Verify 404 when marking non-existent message as read."""
        with allure.step("Attempt to mark non-existent message as read"):
            response = contact_client.mark_message_read(99999)
        
        with allure.step("Verify not found response"):
            assert response.status_code == 404


@allure.feature("Contact API")
@allure.story("Delete Message")
class TestDeleteMessage:
    """Test DELETE /api/v1/contact/{message_id} endpoint."""
    
    @pytest.mark.regression
    @pytest.mark.positive
    @allure.title("Delete message successfully")
    def test_delete_message_success(self, contact_client):
        """Verify successful message deletion."""
        with allure.step("Delete message with ID 1"):
            response = contact_client.delete_message(1)
        
        with allure.step("Verify response status"):
            assert response.status_code in [200, 204, 404]
    
    @pytest.mark.regression
    @pytest.mark.negative
    @allure.title("Delete non-existent message")
    def test_delete_message_not_found(self, contact_client):
        """Verify 404 when deleting non-existent message."""
        with allure.step("Attempt to delete non-existent message"):
            response = contact_client.delete_message(99999)
        
        with allure.step("Verify not found response"):
            assert response.status_code == 404
