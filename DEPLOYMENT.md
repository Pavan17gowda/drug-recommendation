# Deployment Guide for DrugGenius

## Vercel Deployment

### Prerequisites
- GitHub account
- Vercel account (sign up at vercel.com)
- Code pushed to GitHub repository

### Step 1: Connect to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repository: `Pavan17gowda/drug-recommendation`

### Step 2: Configure Project

1. **Framework Preset**: Select "Other"
2. **Root Directory**: Leave as `.` (root)
3. **Build Command**: Leave empty (Vercel auto-detects)
4. **Output Directory**: Leave empty
5. **Install Command**: `pip install -r requirements.txt`

### Step 3: Environment Variables (Optional)

Add these if needed:
- `FLASK_ENV`: `production`
- `SECRET_KEY`: Your secret key

### Step 4: Deploy

Click "Deploy" and wait for the build to complete.

## Important Notes for Vercel

### File Storage Limitation
Vercel's serverless functions are stateless, meaning:
- Files written during runtime are NOT persisted
- The `data/` folder will reset on each deployment
- User data and recommendations will be lost

### Solutions for Production

#### Option 1: Use a Cloud Database (Recommended)

**MongoDB Atlas (Free Tier Available)**
```python
# Install: pip install pymongo
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGODB_URI'))
db = client['druggenius']
users = db['users']
recommendations = db['recommendations']
```

**PostgreSQL on Railway/Supabase**
```python
# Install: pip install psycopg2-binary
import psycopg2

conn = psycopg2.connect(os.getenv('DATABASE_URL'))
```

#### Option 2: Use Vercel KV (Key-Value Store)
```python
# Install: pip install vercel-kv
from vercel_kv import kv

# Store data
kv.set('users', json.dumps(users_db))

# Retrieve data
users_db = json.loads(kv.get('users'))
```

#### Option 3: Use Vercel Postgres
```python
# Install: pip install vercel-postgres
from vercel_postgres import sql

# Query
result = sql('SELECT * FROM users WHERE email = $1', [email])
```

### Updated Code for MongoDB

Replace the file storage functions in `app.py`:

```python
from pymongo import MongoClient
import os

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'))
db = client['druggenius']

def load_users():
    users = {}
    for user in db.users.find():
        users[user['email']] = {
            'username': user['username'],
            'email': user['email'],
            'password': user['password']
        }
    return users

def save_users(users):
    for email, user_data in users.items():
        db.users.update_one(
            {'email': email},
            {'$set': user_data},
            upsert=True
        )

def load_recommendations():
    recs = {}
    for rec in db.recommendations.find():
        email = rec['user_email']
        if email not in recs:
            recs[email] = []
        recs[email].append(rec['data'])
    return recs

def save_recommendations(recommendations):
    for email, recs in recommendations.items():
        for rec in recs:
            db.recommendations.update_one(
                {'user_email': email, 'data.date': rec['date']},
                {'$set': {'user_email': email, 'data': rec}},
                upsert=True
            )
```

## Alternative Deployment Options

### 1. Railway (Recommended for Full-Stack)
- Supports persistent file storage
- Free tier available
- Easy deployment from GitHub
- Supports databases

**Deploy to Railway:**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### 2. Render
- Free tier available
- Persistent disk storage
- Auto-deploy from GitHub

**Deploy to Render:**
1. Go to render.com
2. New Web Service
3. Connect GitHub repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`

### 3. PythonAnywhere
- Free tier with persistent storage
- Good for Flask apps
- Manual deployment

### 4. Heroku
- Requires credit card (even for free tier)
- Good Flask support
- Easy deployment

## Recommended Setup for Production

1. **Use Railway or Render** for the backend (supports file storage)
2. **Use MongoDB Atlas** for database (free tier)
3. **Use Vercel** for frontend only (if separating frontend/backend)

## Quick Fix for Vercel (Temporary)

If you want to deploy on Vercel NOW without database:

1. Accept that data will be lost on each deployment
2. Use it for demo/testing purposes only
3. Add a warning message to users

Add this to your templates:
```html
<div class="warning">
    ⚠️ Demo Mode: Data is not persisted and will reset periodically.
</div>
```

## Environment Variables for Production

Create a `.env` file (don't commit this):
```
SECRET_KEY=your-secret-key-here
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/druggenius
DATABASE_URL=postgresql://user:pass@host:5432/dbname
FLASK_ENV=production
```

## Testing Deployment Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Test with production settings
FLASK_ENV=production python app.py
```

## Troubleshooting

### Build Fails
- Check `requirements.txt` for incompatible packages
- Ensure Python version is specified in `runtime.txt`
- Check Vercel build logs for specific errors

### App Runs but Data Not Saving
- Vercel serverless functions are stateless
- Implement database solution (see above)

### Import Errors
- Ensure all dependencies are in `requirements.txt`
- Remove unused imports from `app.py`

## Support

For deployment issues:
- Vercel Docs: https://vercel.com/docs
- Railway Docs: https://docs.railway.app
- MongoDB Atlas: https://www.mongodb.com/docs/atlas/

## Next Steps After Deployment

1. Set up a proper database (MongoDB Atlas recommended)
2. Configure environment variables
3. Set up custom domain (optional)
4. Enable HTTPS (automatic on Vercel)
5. Set up monitoring and logging
6. Implement backup strategy for data
