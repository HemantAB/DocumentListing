# Document Management System - Frontend

A React-based frontend application for managing text documents with TypeScript and Tailwind CSS.

## Setup Instructions

1. Install dependencies:
```bash
# Install all dependencies
npm install
```

2. Set up environment variables:
```bash
# Create .env file
cp .env.example .env

# Update API URL if needed
VITE_API_URL=http://localhost:8000/api
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at http://localhost:5173

4. Build for production:
```bash
npm run build
```

## Implemented Features

1. **Document Management**
   - View list of documents
   - Create new documents
   - View document details
   - Delete documents
   - Document size display
   - Creation date display

2. **Search & Filter**
   - Search by document name
   - Search by document ID
   - Sort by name or date
   - Pagination support

3. **User Interface**
   - Clean, modern design
   - Responsive layout
   - Loading states
   - Error handling
   - Confirmation dialogs
   - Modal windows

4. **Data Display**
   - Formatted dates
   - File sizes in KB
   - Sortable columns
   - Empty state handling
   - Loading indicators

## Technical Decisions

1. **React + TypeScript**
   - Type safety
   - Better developer experience
   - Improved maintainability
   - Modern component patterns

2. **Vite Build Tool**
   - Fast development server
   - Quick build times
   - Modern module system
   - Hot module replacement

3. **Tailwind CSS**
   - Utility-first approach
   - Consistent styling
   - Easy customization
   - Reduced bundle size

4. **Component Architecture**
   - Reusable UI components
   - Clear component hierarchy
   - Separation of concerns
   - Custom hooks for logic

## Assumptions

1. **Backend API**
   - RESTful API available
   - JSON response format
   - Basic error handling
   - CORS enabled

2. **User Environment**
   - Modern browsers
   - Desktop-first design
   - Reasonable network speed
   - No offline support needed

3. **Usage Patterns**
   - Single user operation
   - No real-time updates needed
   - Sequential operations
   - Standard latency acceptable

4. **Data Volume**
   - Moderate list sizes
   - Text-only content
   - Standard document sizes
   - Regular refresh rate

## Project Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── modal.tsx
│   │   │   └── table.tsx
│   │   └── documents/
│   │       └── DocumentList.tsx
│   ├── types/
│   │   └── document.ts
│   ├── services/
│   │   └── api.ts
│   ├── lib/
│   │   └── utils.ts
│   ├── App.tsx
│   └── main.tsx
├── public/
├── index.html
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── README.md
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run preview` - Preview production build

## Future Improvements

1. **Features**
   - Document editing
   - Rich text support
   - File upload
   - Document sharing
   - Categories/tags
   - Batch operations

2. **Technical**
   - State management (Redux/Zustand)
   - Unit tests
   - E2E tests
   - Error boundary
   - Performance optimization

3. **UX/UI**
   - Dark mode
   - Keyboard shortcuts
   - Drag and drop
   - Mobile optimization
   - Accessibility improvements

4. **Infrastructure**
   - Docker setup
   - CI/CD pipeline
   - Analytics
   - Error tracking

## Requirements

- Node.js 16+
- npm 7+
- Modern browser support

## Browser Support

- Chrome (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Edge (last 2 versions)