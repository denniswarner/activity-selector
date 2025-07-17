"""
Google Sheets service for fetching activity data.
"""
import os
import random
from typing import List, Dict, Optional, Any
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ..models import Activity, PriceLevel, Category
from .cache_service import cache_service


class GoogleSheetsService:
    """Service for interacting with Google Sheets API."""
    
    def __init__(self):
        """Initialize the Google Sheets service."""
        self.credentials_file = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE')
        self.spreadsheet_id = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
        self.service = None
        self._initialized = False
        
        if not self.credentials_file or not self.spreadsheet_id:
            print("⚠️  Google Sheets credentials not configured. Using mock data for development.")
            return
        
        try:
            self._initialize_service()
            self._initialized = True
        except Exception as e:
            print(f"⚠️  Failed to initialize Google Sheets service: {e}")
            print("   Using mock data for development.")
    
    def _initialize_service(self) -> None:
        """Initialize the Google Sheets API service."""
        try:
            # Define the scope for Google Sheets API
            scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
            
            # Load credentials from service account file
            credentials = Credentials.from_service_account_file(
                self.credentials_file, 
                scopes=scope
            )
            
            # Build the service
            self.service = build('sheets', 'v4', credentials=credentials)
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Google Sheets service: {str(e)}")
    
    def get_categories(self) -> List[Category]:
        """
        Get available categories from the spreadsheet.
        
        Returns:
            List[Category]: List of available categories
        """
        if not self._initialized:
            return self._get_mock_categories()
        
        cache_key = "categories"
        cached_categories = cache_service.get(cache_key)
        
        if cached_categories:
            return cached_categories
        
        try:
            # Get all worksheet names (categories)
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            categories = []
            for sheet in spreadsheet['sheets']:
                sheet_name = sheet['properties']['title']
                # Skip system sheets that start with underscore
                if not sheet_name.startswith('_'):
                    category = Category(
                        name=sheet_name,
                        description=f"Activities in the {sheet_name} category",
                        sheet_name=sheet_name
                    )
                    categories.append(category)
            
            # Cache the categories for 1 hour
            cache_service.set(cache_key, categories, ttl=3600)
            return categories
            
        except HttpError as e:
            raise RuntimeError(f"Failed to fetch categories from Google Sheets: {str(e)}")
    
    def get_activities_by_category(
        self, 
        category: str, 
        price_level: Optional[PriceLevel] = None
    ) -> List[Activity]:
        """
        Get activities from a specific category and optionally filter by price level.
        
        Args:
            category (str): Category name (worksheet name)
            price_level (Optional[PriceLevel]): Price level filter
            
        Returns:
            List[Activity]: List of activities matching the criteria
        """
        if not self._initialized:
            activities = self._get_mock_activities(category)
            if price_level:
                activities = [a for a in activities if a.price_level == price_level]
            return activities
        
        cache_key = f"activities_{category}_{price_level or 'all'}"
        cached_activities = cache_service.get(cache_key)
        
        if cached_activities:
            return cached_activities
        
        try:
            # Get all data from the worksheet
            range_name = f"{category}!A:K"  # Columns A-K: Name, Price, Description, Location, Address, Phone, Past Orders, Last Bill, URL, Notes, Last Visit Date
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return []
            
            # Skip header row if it exists
            data_rows = values[1:] if len(values) > 1 and self._is_header_row(values[0]) else values
            
            activities = []
            for row in data_rows:
                if len(row) >= 3:  # At minimum: name, price, category
                    try:
                        activity = self._parse_activity_row(row, category)
                        
                        # Filter by price level if specified
                        if price_level is None or activity.price_level == price_level:
                            activities.append(activity)
                            
                    except ValueError as e:
                        # Skip invalid rows
                        print(f"Warning: Skipping invalid activity row: {row}, Error: {e}")
                        continue
            
            # Cache the activities for 30 minutes
            cache_service.set(cache_key, activities, ttl=1800)
            return activities
            
        except HttpError as e:
            raise RuntimeError(f"Failed to fetch activities from Google Sheets: {str(e)}")
    
    def get_random_activities(
        self, 
        category: str, 
        price_level: Optional[PriceLevel] = None,
        limit: int = 5
    ) -> List[Activity]:
        """
        Get random activities from a category.
        
        Args:
            category (str): Category name
            price_level (Optional[PriceLevel]): Price level filter
            limit (int): Number of activities to return
            
        Returns:
            List[Activity]: Random list of activities
        """
        activities = self.get_activities_by_category(category, price_level)
        
        if not activities:
            return []
        
        # Return random selection
        return random.sample(activities, min(limit, len(activities)))
    
    def _parse_activity_row(self, row: List[str], category: str) -> Activity:
        """
        Parse a row from Google Sheets into an Activity object.
        
        Args:
            row (List[str]): Row data from Google Sheets
            category (str): Category name
            
        Returns:
            Activity: Parsed activity object
            
        Raises:
            ValueError: If required fields are missing or invalid
        """
        if len(row) < 2:
            raise ValueError("Row must have at least name and price level")
        
        name = row[0].strip()
        if not name:
            raise ValueError("Activity name cannot be empty")
        
        # Parse price level
        price_str = row[1].strip() if len(row) > 1 else "Free"
        try:
            price_level = PriceLevel(price_str)
        except ValueError:
            # Try to map common price indicators
            price_mapping = {
                "free": PriceLevel.FREE,
                "$": PriceLevel.LOW,
                "$$": PriceLevel.MEDIUM,
                "$$$": PriceLevel.HIGH,
                "$$$$": PriceLevel.LUXURY,
                "low": PriceLevel.LOW,
                "medium": PriceLevel.MEDIUM,
                "high": PriceLevel.HIGH,
                "luxury": PriceLevel.LUXURY
            }
            price_level = price_mapping.get(price_str.lower(), PriceLevel.FREE)
        
        # Parse optional fields
        description = row[2].strip() if len(row) > 2 and row[2] else None
        location = row[3].strip() if len(row) > 3 and row[3] else None
        address = row[4].strip() if len(row) > 4 and row[4] else None
        phone = row[5].strip() if len(row) > 5 and row[5] else None
        # Parse past orders (comma-separated list)
        past_orders = None
        if len(row) > 6 and row[6]:
            past_orders = [order.strip() for order in row[6].split(',') if order.strip()]
        # Parse last bill price
        last_bill_price = None
        if len(row) > 7 and row[7]:
            try:
                price_str = row[7].replace('$', '').replace(',', '').strip()
                last_bill_price = float(price_str)
            except ValueError:
                pass
        # Parse URL
        url = row[8].strip() if len(row) > 8 and row[8] else None
        # Parse Notes
        notes = row[9].strip() if len(row) > 9 and row[9] else None
        # Parse Last Visit Date
        last_visit_date = row[10].strip() if len(row) > 10 and row[10] else None
        return Activity(
            name=name,
            description=description,
            price_level=price_level,
            location=location,
            category=category,
            address=address,
            phone=phone,
            past_orders=past_orders,
            last_bill_price=last_bill_price,
            url=url,
            notes=notes,
            last_visit_date=last_visit_date
        )
    
    def _is_header_row(self, row: List[str]) -> bool:
        """
        Check if a row is a header row.
        
        Args:
            row (List[str]): Row to check
            
        Returns:
            bool: True if it's a header row
        """
        if not row:
            return False
        
        # Common header indicators
        header_indicators = ['name', 'activity', 'title', 'description', 'price', 'cost', 'location']
        first_cell = row[0].lower().strip()
        
        return any(indicator in first_cell for indicator in header_indicators)


    def _get_mock_categories(self) -> List[Category]:
        """Get mock categories for development."""
        return [
            Category(
                name="Food",
                description="Restaurants and dining options",
                sheet_name="Food"
            ),
            Category(
                name="Fun",
                description="Entertainment and recreational activities",
                sheet_name="Fun"
            ),
            Category(
                name="Outdoor",
                description="Outdoor activities and adventures",
                sheet_name="Outdoor"
            ),
            Category(
                name="Culture",
                description="Museums, theaters, and cultural experiences",
                sheet_name="Culture"
            ),
        ]
    
    def _get_mock_activities(self, category: str) -> List[Activity]:
        """Get mock activities for development."""
        mock_data = {
            "Food": [
                Activity(name="Pizza Place", description="Great local pizza joint", price_level=PriceLevel.MEDIUM, location="Downtown", category="Food"),
                Activity(name="Sushi Restaurant", description="Authentic Japanese sushi", price_level=PriceLevel.HIGH, location="West Side", category="Food"),
                Activity(name="Food Truck", description="Delicious street food", price_level=PriceLevel.LOW, location="Various locations", category="Food"),
                Activity(name="Fine Dining", description="Upscale dining experience", price_level=PriceLevel.LUXURY, location="City Center", category="Food"),
            ],
            "Fun": [
                Activity(name="Movie Theater", description="Latest blockbusters", price_level=PriceLevel.MEDIUM, location="Mall", category="Fun"),
                Activity(name="Bowling Alley", description="Fun for the whole family", price_level=PriceLevel.MEDIUM, location="Entertainment District", category="Fun"),
                Activity(name="Escape Room", description="Solve puzzles together", price_level=PriceLevel.HIGH, location="Downtown", category="Fun"),
                Activity(name="Arcade", description="Classic and modern games", price_level=PriceLevel.LOW, location="Shopping Center", category="Fun"),
            ],
            "Outdoor": [
                Activity(name="Hiking Trail", description="Scenic mountain trails", price_level=PriceLevel.FREE, location="State Park", category="Outdoor"),
                Activity(name="Bike Rental", description="Explore the city on wheels", price_level=PriceLevel.LOW, location="Downtown", category="Outdoor"),
                Activity(name="Rock Climbing", description="Indoor climbing gym", price_level=PriceLevel.MEDIUM, location="Sports Complex", category="Outdoor"),
                Activity(name="Kayaking", description="Paddle on the river", price_level=PriceLevel.MEDIUM, location="River Park", category="Outdoor"),
            ],
            "Culture": [
                Activity(name="Art Museum", description="Contemporary art exhibits", price_level=PriceLevel.MEDIUM, location="Cultural District", category="Culture"),
                Activity(name="Theater Show", description="Live performances", price_level=PriceLevel.HIGH, location="Theater District", category="Culture"),
                Activity(name="Library Visit", description="Quiet reading and study", price_level=PriceLevel.FREE, location="Public Library", category="Culture"),
                Activity(name="Concert Hall", description="Classical music performances", price_level=PriceLevel.HIGH, location="Music Center", category="Culture"),
            ],
        }
        return mock_data.get(category, [])


# Global sheets service instance
sheets_service = GoogleSheetsService() 