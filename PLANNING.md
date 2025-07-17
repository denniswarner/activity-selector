# Activity Selector - Project Planning

## 🎯 Project Overview
A responsive web application that helps users decide what to do on their free time by suggesting activities based on category, price level, and data from Google Sheets.

## 🏗️ Architecture

### Frontend
- **Framework**: React with TypeScript
- **Styling**: Tailwind CSS for responsive design
- **State Management**: React hooks (useState, useEffect)
- **Build Tool**: Vite for fast development

### Backend
- **Framework**: FastAPI (Python)
- **Data Source**: Google Sheets API
- **Authentication**: Google OAuth2 for Sheets access
- **Caching**: In-memory cache for sheet data to reduce API calls

### Data Structure
- **Google Sheets**: Each worksheet represents an activity category
- **Categories**: Fun, Food, Entertainment, etc.
- **Price Levels**: Free ($), Low ($$), Medium ($$$), High ($$$$)
- **Activity Data**: Name, description, price level, location (optional)

## 📁 File Structure
```
activity-selector/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ActivitySelector.tsx
│   │   │   ├── CategoryDropdown.tsx
│   │   │   ├── PriceSelector.tsx
│   │   │   ├── ActivityList.tsx
│   │   │   └── Header.tsx
│   │   ├── types/
│   │   │   └── types.ts
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── index.html
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── services/
│   │   │   ├── sheets_service.py
│   │   │   └── cache_service.py
│   │   └── api/
│   │       └── routes.py
│   ├── requirements.txt
│   └── .env.example
├── tests/
│   ├── test_sheets_service.py
│   ├── test_api.py
│   └── test_models.py
├── README.md
├── TASK.md
└── PLANNING.md
```

## 🎨 UI/UX Design
- **Landing Page**: Clean, modern design with "What do you want to do today?" as the main heading
- **Category Dropdown**: Large, easy-to-use dropdown with clear category names
- **Price Selector**: Visual price level selector (Free, $, $$, $$$, $$$$)
- **Suggest Button**: Prominent call-to-action button
- **Results**: Card-based layout showing suggested activities
- **Responsive**: Mobile-first design that works on all devices

## 🔧 Technical Implementation

### Google Sheets Integration
- Use Google Sheets API v4
- Service account authentication for backend access
- Cache sheet data to minimize API calls
- Error handling for API rate limits

### API Endpoints
- `GET /api/categories` - Get available categories
- `GET /api/activities` - Get activities by category and price
- `GET /api/suggest` - Get random suggestions

### Data Flow
1. User selects category and price level
2. Frontend calls backend API
3. Backend fetches data from Google Sheets (or cache)
4. Backend filters and randomizes activities
5. Frontend displays results

## 🧪 Testing Strategy
- Unit tests for all backend services
- API endpoint testing
- Frontend component testing
- Integration tests for Google Sheets API

## 📋 Development Phases
1. **Phase 1**: Basic backend with Google Sheets integration
2. **Phase 2**: Frontend UI components
3. **Phase 3**: API integration and data flow
4. **Phase 4**: Testing and optimization
5. **Phase 5**: Deployment and documentation

## 🔐 Security Considerations
- Environment variables for API keys
- CORS configuration for frontend-backend communication
- Input validation and sanitization
- Rate limiting for API endpoints

## 🚀 Deployment
- Frontend: Vercel or Netlify
- Backend: Railway or Heroku
- Environment variables for production configuration 