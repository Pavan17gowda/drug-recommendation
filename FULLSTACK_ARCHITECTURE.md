# DrugGenius - Full Stack Architecture

## Overview
DrugGenius is a full-stack web application for drug recommendations based on symptoms. The application follows a modern architecture with clear separation between frontend and backend.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   HTML/CSS   │  │  JavaScript  │  │   Services   │     │
│  │   Templates  │  │   UI Logic   │  │   (API/Auth) │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/REST API
                            │
┌─────────────────────────────────────────────────────────────┐
│                        BACKEND API                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Flask App  │  │  Auth Logic  │  │  Business    │     │
│  │   (Routes)   │  │   (bcrypt)   │  │   Logic      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ File I/O
                            │
┌─────────────────────────────────────────────────────────────┐
│                      DATA STORAGE                            │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │  users.json  │  │recommendations│                        │
│  │              │  │    .json      │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Backend
- **Framework**: Flask 3.0.3
- **Authentication**: bcrypt for password hashing
- **CORS**: flask-cors for cross-origin requests
- **Session Management**: Flask sessions with filesystem storage
- **Data Storage**: JSON files (can be replaced with database)

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript (ES6+)**: Vanilla JS with modern features
- **Architecture Pattern**: Service-oriented architecture

## Project Structure

```
DrugGenius/
├── api/                          # Backend API
│   ├── app.py                    # Main Flask application
│   ├── config.py                 # Configuration settings
│   └── requirements.txt          # Python dependencies
│
├── static/                       # Frontend assets
│   ├── css/
│   │   └── style.css            # Styles
│   ├── js/
│   │   ├── api.js               # API service layer
│   │   ├── store.js             # State management
│   │   ├── auth.js              # Authentication service
│   │   ├── recommendations.js   # Recommendations service
│   │   └── script2.js           # UI logic
│   └── images/                  # Image assets
│
├── templates/                    # HTML templates
│   ├── index.html               # Main page
│   ├── dashboard.html           # Dashboard
│   └── history.html             # History page
│
├── data/                         # Data storage
│   ├── users.json               # User data
│   └── recommendations.json     # Recommendations data
│
└── app.py                        # Original monolithic app (legacy)
```

## API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user
- `POST /api/logout` - Logout user
- `GET /api/user` - Get current user info

### Recommendations
- `POST /api/recommendations` - Save new recommendation
- `GET /api/recommendations` - Get all user recommendations
- `GET /api/recommendations/<id>` - Get specific recommendation
- `DELETE /api/recommendations/<id>` - Delete recommendation

### Statistics
- `GET /api/statistics` - Get user statistics

### Health
- `GET /api/health` - API health check

## Frontend Services

### 1. API Service (`api.js`)
Handles all HTTP requests to the backend API.

**Methods:**
- `register(username, email, password)`
- `login(email, password)`
- `logout()`
- `getCurrentUser()`
- `saveRecommendation(data)`
- `getRecommendations()`
- `deleteRecommendation(id)`
- `getStatistics()`

### 2. Store Service (`store.js`)
Manages application state and provides reactive updates.

**State:**
```javascript
{
  user: null,
  isAuthenticated: false,
  recommendations: [],
  statistics: null,
  loading: false,
  error: null
}
```

**Methods:**
- `getState()` - Get current state
- `setState(updates)` - Update state
- `subscribe(listener)` - Subscribe to changes
- `setUser(user)` - Set user data
- `setRecommendations(recommendations)` - Set recommendations

### 3. Auth Service (`auth.js`)
Handles authentication logic and user management.

**Methods:**
- `register(username, email, password, confirmPassword)`
- `login(email, password)`
- `logout()`
- `isAuthenticated()`
- `getCurrentUser()`
- `verifySession()`

### 4. Recommendations Service (`recommendations.js`)
Manages drug recommendations and disease identification.

**Methods:**
- `identifyDiseases(symptoms)`
- `generateRecommendations(symptoms, patientInfo)`
- `processSymptoms(symptoms, patientInfo)`
- `loadRecommendations()`
- `deleteRecommendation(id)`
- `loadStatistics()`

## Data Models

### User
```json
{
  "email": "user@example.com",
  "username": "John Doe",
  "password": "hashed_password",
  "created_at": "2026-02-23T12:00:00Z"
}
```

### Recommendation
```json
{
  "id": 1,
  "date": "2026-02-23T12:00:00Z",
  "symptoms": ["fever", "headache"],
  "diseases": ["cold"],
  "medications": ["Acetaminophen", "Ibuprofen"],
  "patientInfo": {
    "age": "25",
    "sex": "male",
    "bp": "120/80",
    "temperature": "38.5"
  }
}
```

## Setup Instructions

### Backend Setup

1. **Install Python dependencies:**
```bash
cd api
pip install -r requirements.txt
```

2. **Run the API server:**
```bash
python app.py
```

The API will run on `http://localhost:5000`

### Frontend Setup

1. **Serve the frontend:**
   - Use the original Flask app to serve templates
   - Or use any static file server

2. **Update API URL:**
   - Edit `static/js/api.js`
   - Change `API_BASE_URL` if needed

## Features

### 1. User Authentication
- Secure registration with password hashing
- Session-based authentication
- Password validation
- Persistent sessions

### 2. Symptom Analysis
- 40+ symptoms supported
- Disease identification algorithm
- Age-based medication filtering
- Patient information tracking

### 3. Drug Recommendations
- Comprehensive drug database
- Symptom-to-medication mapping
- Multiple medications per symptom
- Safety disclaimers

### 4. Dashboard
- User statistics
- Recent recommendations
- Quick actions
- Health tips

### 5. History Management
- Complete recommendation history
- Advanced filtering (symptoms, diseases, dates)
- Detailed view modal
- Download reports
- Delete records

## Security Features

1. **Password Security**
   - bcrypt hashing with salt
   - Configurable rounds (default: 4 for development)

2. **Session Management**
   - Secure session cookies
   - 7-day session lifetime
   - Server-side session storage

3. **CORS Protection**
   - Configured for specific origins
   - Credentials support

4. **Input Validation**
   - Server-side validation
   - Client-side validation
   - Error handling

## Deployment

### Development
```bash
# Backend
cd api
python app.py

# Frontend (if separate)
# Use any static file server
```

### Production Considerations

1. **Backend:**
   - Use production WSGI server (Gunicorn, uWSGI)
   - Enable HTTPS
   - Use environment variables for secrets
   - Replace JSON storage with database (PostgreSQL, MongoDB)

2. **Frontend:**
   - Minify JavaScript and CSS
   - Enable caching
   - Use CDN for static assets
   - Implement service workers for offline support

3. **Security:**
   - Increase bcrypt rounds to 12+
   - Implement rate limiting
   - Add CSRF protection
   - Use secure session cookies
   - Implement input sanitization

## Future Enhancements

1. **Database Integration**
   - Replace JSON files with PostgreSQL/MongoDB
   - Add database migrations
   - Implement connection pooling

2. **Advanced Features**
   - Drug interaction checking
   - Allergy tracking
   - Prescription history
   - Doctor recommendations
   - Appointment scheduling

3. **API Improvements**
   - JWT authentication
   - API versioning
   - Rate limiting
   - Pagination
   - Caching

4. **Frontend Enhancements**
   - Progressive Web App (PWA)
   - Offline support
   - Push notifications
   - Real-time updates (WebSockets)
   - Mobile app (React Native)

5. **Analytics**
   - User behavior tracking
   - Recommendation accuracy metrics
   - Popular symptoms/medications
   - Usage statistics

## Testing

### Backend Tests
```bash
cd api
pytest tests/
```

### Frontend Tests
```bash
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [repository-url]/issues
- Email: support@druggenius.com

## Changelog

### Version 1.0.0 (2026-02-23)
- Initial full-stack implementation
- User authentication
- Symptom analysis
- Drug recommendations
- Dashboard and history
- RESTful API
- Service-oriented frontend architecture
