"""
Unit tests for the Pydantic models.
"""
import pytest
from backend.app.models import (
    PriceLevel, 
    Activity, 
    Category, 
    ActivityRequest, 
    ActivityResponse,
    ErrorResponse
)


class TestPriceLevel:
    """Test cases for PriceLevel enum."""
    
    def test_price_level_values(self):
        """Test that all price level values are correct."""
        assert PriceLevel.FREE == "Free"
        assert PriceLevel.LOW == "$"
        assert PriceLevel.MEDIUM == "$$"
        assert PriceLevel.HIGH == "$$$"
        assert PriceLevel.LUXURY == "$$$$"
    
    def test_price_level_enumeration(self):
        """Test that all expected price levels exist."""
        expected_levels = ["Free", "$", "$$", "$$$", "$$$$"]
        actual_levels = [level.value for level in PriceLevel]
        assert actual_levels == expected_levels


class TestActivity:
    """Test cases for Activity model."""
    
    def test_valid_activity(self):
        """Test creating a valid activity."""
        activity = Activity(
            name="Hiking",
            description="Go for a hike in the mountains",
            price_level=PriceLevel.FREE,
            location="Local trails",
            category="Outdoor"
        )
        
        assert activity.name == "Hiking"
        assert activity.description == "Go for a hike in the mountains"
        assert activity.price_level == PriceLevel.FREE
        assert activity.location == "Local trails"
        assert activity.category == "Outdoor"
    
    def test_activity_without_optional_fields(self):
        """Test creating an activity without optional fields."""
        activity = Activity(
            name="Reading",
            price_level=PriceLevel.FREE,
            category="Indoor"
        )
        
        assert activity.name == "Reading"
        assert activity.description is None
        assert activity.location is None
        assert activity.price_level == PriceLevel.FREE
        assert activity.category == "Indoor"
    
    def test_activity_validation(self):
        """Test that required fields are enforced."""
        # Pydantic will raise ValidationError, not ValueError
        from pydantic import ValidationError
        
        # Test that empty name is allowed (Pydantic doesn't validate empty strings by default)
        # Instead, test with missing required fields
        with pytest.raises(ValidationError):
            Activity(
                # Missing name should fail
                price_level=PriceLevel.FREE,
                category="Test"
            )
        
        with pytest.raises(ValidationError):
            Activity(
                name="Test Activity",
                # Missing price_level should fail
                category="Test"
            )
        
        with pytest.raises(ValidationError):
            Activity(
                name="Test Activity",
                price_level=PriceLevel.FREE,
                # Missing category should fail
            )


class TestCategory:
    """Test cases for Category model."""
    
    def test_valid_category(self):
        """Test creating a valid category."""
        category = Category(
            name="Food",
            description="Restaurants and dining options",
            sheet_name="Food"
        )
        
        assert category.name == "Food"
        assert category.description == "Restaurants and dining options"
        assert category.sheet_name == "Food"
    
    def test_category_without_description(self):
        """Test creating a category without description."""
        category = Category(
            name="Fun",
            sheet_name="Fun"
        )
        
        assert category.name == "Fun"
        assert category.description is None
        assert category.sheet_name == "Fun"


class TestActivityRequest:
    """Test cases for ActivityRequest model."""
    
    def test_valid_request(self):
        """Test creating a valid activity request."""
        request = ActivityRequest(
            category="Food",
            price_level=PriceLevel.MEDIUM,
            limit=10
        )
        
        assert request.category == "Food"
        assert request.price_level == PriceLevel.MEDIUM
        assert request.limit == 10
    
    def test_request_without_price_level(self):
        """Test creating a request without price level."""
        request = ActivityRequest(
            category="Fun"
        )
        
        assert request.category == "Fun"
        assert request.price_level is None
        assert request.limit == 5  # Default value
    
    def test_request_validation(self):
        """Test request validation rules."""
        # Test limit constraints
        with pytest.raises(ValueError):
            ActivityRequest(
                category="Test",
                limit=0  # Should be >= 1
            )
        
        with pytest.raises(ValueError):
            ActivityRequest(
                category="Test",
                limit=25  # Should be <= 20
            )


class TestActivityResponse:
    """Test cases for ActivityResponse model."""
    
    def test_valid_response(self):
        """Test creating a valid activity response."""
        activities = [
            Activity(
                name="Activity 1",
                price_level=PriceLevel.FREE,
                category="Test"
            ),
            Activity(
                name="Activity 2",
                price_level=PriceLevel.FREE,
                category="Test"
            )
        ]
        
        response = ActivityResponse(
            activities=activities,
            total_found=2,
            category="Test",
            price_level=PriceLevel.FREE
        )
        
        assert len(response.activities) == 2
        assert response.total_found == 2
        assert response.category == "Test"
        assert response.price_level == PriceLevel.FREE
    
    def test_response_without_price_level(self):
        """Test creating a response without price level filter."""
        activities = [
            Activity(
                name="Activity 1",
                price_level=PriceLevel.FREE,
                category="Test"
            )
        ]
        
        response = ActivityResponse(
            activities=activities,
            total_found=1,
            category="Test"
        )
        
        assert response.price_level is None


class TestErrorResponse:
    """Test cases for ErrorResponse model."""
    
    def test_valid_error_response(self):
        """Test creating a valid error response."""
        error = ErrorResponse(
            error="Not found",
            detail="The requested resource was not found"
        )
        
        assert error.error == "Not found"
        assert error.detail == "The requested resource was not found"
    
    def test_error_response_without_detail(self):
        """Test creating an error response without detail."""
        error = ErrorResponse(
            error="Internal server error"
        )
        
        assert error.error == "Internal server error"
        assert error.detail is None 