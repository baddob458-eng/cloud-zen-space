# N Cloud Backend - FastAPI

Complete backend API for N Cloud platform.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new account
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/logout` - Logout
- `POST /api/auth/google` - Google OAuth (placeholder)
- `POST /api/auth/apple` - Apple OAuth (placeholder)

### Profile
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update profile (username, email, password)
- `DELETE /api/profile` - Delete account

### Tools
- `GET /api/tools/list` - Get all available tools
- `GET /api/tools/connected` - Get user's connected tools
- `POST /api/tools/connect` - Connect a tool
- `DELETE /api/tools/{tool_id}` - Disconnect a tool

### History
- `GET /api/history` - Get user's session history
- `POST /api/history` - Save new session
- `DELETE /api/history/{history_id}` - Delete history item

## Authentication

All protected endpoints require Bearer token in Authorization header:
```
Authorization: Bearer <access_token>
```

Tokens are returned on signup/login and expire after 60 minutes.

## Database

Using SQLite (`ncloud.db`) with SQLAlchemy ORM.

Tables:
- `users` - User accounts
- `connected_tools` - User's connected tools
- `history` - User's AI session history

## CORS

Enabled for:
- http://localhost:3000
- http://localhost:8080

## OAuth Setup (Future)

To enable Google/Apple OAuth:
1. Get credentials from Google Cloud Console / Apple Developer
2. Add to `.env`:
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`
   - `APPLE_CLIENT_ID`
   - `APPLE_CLIENT_SECRET`
3. Install `authlib`: `pip install authlib`
