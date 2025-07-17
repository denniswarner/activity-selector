# Activity Selector

A modern web application that helps you discover and choose activities based on your preferences. The app pulls activity data from Google Sheets and provides an intuitive interface for filtering and selecting activities by category, price level, and location.

## Features

- **Category-based filtering**: Browse activities by Food, Fun, Outdoor, and Culture categories
- **Price level filtering**: Filter by budget ($, $$, $$$, $$$$)
- **Location-based suggestions**: Find activities in specific areas
- **Smart suggestions**: Get personalized activity recommendations
- **Real-time data**: Connected to Google Sheets for easy data management
- **Modern UI**: Built with React, Tailwind CSS, and Vite
- **RESTful API**: FastAPI backend with automatic documentation

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation and serialization
- **Google Sheets API**: Data source integration
- **Uvicorn**: ASGI server

### Frontend
- **React**: UI framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Fast build tool and dev server

## Project Structure

```
activity-selector/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # Pydantic models
│   │   ├── services/
│   │   │   └── sheets_service.py # Google Sheets integration
│   │   └── api/
│   │       └── routes.py        # API endpoints
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── types/               # TypeScript type definitions
│   │   └── main.tsx             # App entry point
│   ├── package.json             # Node.js dependencies
│   └── vite.config.ts           # Vite configuration
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- Google Cloud Platform account (for Sheets API)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Sheets API:**
   - Create a Google Cloud Project
   - Enable Google Sheets API
   - Create a service account
   - Download credentials JSON file
   - Share your Google Sheet with the service account email

5. **Configure environment variables:**
   Create a `.env` file in the backend directory:
   ```env
   GOOGLE_SHEETS_CREDENTIALS_FILE=path/to/your/credentials.json
   SPREADSHEET_ID=your_spreadsheet_id_here
   ```

6. **Start the backend server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5176`

## API Endpoints

### Categories
- `GET /api/categories` - Get all available categories

### Activities
- `GET /api/activities?category={category}` - Get activities by category
- `POST /api/suggest` - Get activity suggestions based on criteria

### Request/Response Examples

**Get Categories:**
```bash
curl http://localhost:8001/api/categories
```

**Get Activities by Category:**
```bash
curl "http://localhost:8001/api/activities?category=Food"
```

**Get Suggestions:**
```bash
curl -X POST "http://localhost:8001/api/suggest" \
  -H "Content-Type: application/json" \
  -d '{"category": "Food", "price_level": "$$", "location": "Downtown"}'
```

## Google Sheets Data Format

Your Google Sheet should have the following columns:
- Name
- Description
- Price Level
- Location
- Category
- Address
- Phone
- URL
- Notes
- Last Visit Date
- Past Orders
- Last Bill Price

## Development

### Backend Development
- The backend uses FastAPI with automatic reload
- API documentation available at `http://localhost:8001/docs`
- CORS is configured for frontend development

### Frontend Development
- Hot module replacement enabled
- TypeScript for type safety
- Tailwind CSS for styling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on GitHub. 