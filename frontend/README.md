# Activity Selector Frontend

A modern React + TypeScript frontend for the Activity Selector application.

## Features

- 🎨 Modern, responsive UI with Tailwind CSS
- 📱 Mobile-first design
- ⚡ Fast development with Vite
- 🔒 Type-safe with TypeScript
- 🎯 Component-based architecture
- 🌊 Smooth animations and transitions

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **React Hooks** - State management

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file (optional):
```bash
cp .env.example .env
```

3. Start development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## Project Structure

```
src/
├── components/          # React components
│   ├── ActivitySelector.tsx    # Main app component
│   ├── ActivityList.tsx        # Activity results display
│   ├── CategoryDropdown.tsx    # Category selection
│   ├── Header.tsx             # App header
│   └── PriceSelector.tsx      # Price level selection
├── services/           # API services
│   └── api.ts         # Backend API client
├── types/             # TypeScript type definitions
│   └── types.ts       # Shared types
├── App.tsx            # Root component
├── main.tsx           # App entry point
└── index.css          # Global styles
```

## Component Architecture

The app follows a component-based architecture:

- **ActivitySelector** - Main orchestrator component
- **Header** - App title and description
- **CategoryDropdown** - Category selection dropdown
- **PriceSelector** - Visual price level selector
- **ActivityList** - Results display with loading/error states

## API Integration

The frontend communicates with the backend via the `apiService`:

- `getCategories()` - Fetch available categories
- `getActivities()` - Fetch activities by category/price
- `getSuggestions()` - Get random activity suggestions
- `healthCheck()` - Backend health check

## Styling

The app uses Tailwind CSS with custom components:

- `.btn-primary` - Primary action buttons
- `.btn-secondary` - Secondary action buttons
- `.card` - Card containers
- `.input-field` - Form inputs

## Development

### Adding New Components

1. Create component file in `src/components/`
2. Export as named export
3. Import and use in parent components
4. Add TypeScript interfaces for props

### Styling Guidelines

- Use Tailwind utility classes
- Create custom components for repeated patterns
- Follow mobile-first responsive design
- Use semantic color names from the design system

### TypeScript

- All components should have proper TypeScript interfaces
- Use type imports for better tree-shaking
- Avoid `any` types, use proper interfaces

## Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Deployment

The frontend can be deployed to any static hosting service:

- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

Make sure to set the `VITE_API_URL` environment variable to point to your deployed backend.
