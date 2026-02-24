# MongoDB Atlas Setup Guide

## Step 1: Create MongoDB Atlas Account

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up for a free account
3. Verify your email address

## Step 2: Create a Cluster

1. Click "Build a Database"
2. Choose **FREE** tier (M0 Sandbox)
3. Select a cloud provider and region (choose closest to you)
4. Cluster Name: `DrugGenius` (or keep default)
5. Click "Create"

Wait 3-5 minutes for cluster creation.

## Step 3: Create Database User

1. Click "Database Access" in left sidebar
2. Click "Add New Database User"
3. Authentication Method: **Password**
4. Username: `druggenius_user` (or your choice)
5. Password: Click "Autogenerate Secure Password" and **SAVE IT**
6. Database User Privileges: **Read and write to any database**
7. Click "Add User"

## Step 4: Configure Network Access

1. Click "Network Access" in left sidebar
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (for development)
   - IP Address: `0.0.0.0/0`
   - Comment: "Allow all IPs"
4. Click "Confirm"

⚠️ **For production**, restrict to specific IPs or use Vercel's IP ranges.

## Step 5: Get Connection String

1. Click "Database" in left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Driver: **Python**, Version: **3.12 or later**
5. Copy the connection string:

```
mongodb+srv://druggenius_user:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

6. Replace `<password>` with your actual password
7. Add database name: `/druggenius` before the `?`

Final format:
```
mongodb+srv://druggenius_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/druggenius?retryWrites=true&w=majority
```

## Step 6: Configure Environment Variables

### For Local Development

Create a `.env` file in your project root:

```env
MONGODB_URI=mongodb+srv://druggenius_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/druggenius?retryWrites=true&w=majority
SECRET_KEY=717730305d8ed3cdc3f37eedaf000abe29f377cdc7800607
FLASK_ENV=development
```

### For Vercel Deployment

1. Go to your Vercel project dashboard
2. Click "Settings"
3. Click "Environment Variables"
4. Add new variable:
   - **Name**: `MONGODB_URI`
   - **Value**: Your connection string
   - **Environment**: Production, Preview, Development (select all)
5. Click "Save"
6. Add another variable:
   - **Name**: `SECRET_KEY`
   - **Value**: Your secret key
7. Click "Save"

## Step 7: Test Connection Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

You should see:
```
✅ Connected to MongoDB Atlas successfully
✅ Using MongoDB for data storage
```

## Step 8: Deploy to Vercel

```bash
# Commit changes
git add .
git commit -m "Add MongoDB Atlas integration"
git push origin main
```

Vercel will automatically redeploy with MongoDB support!

## Verify MongoDB is Working

1. Register a new user on your deployed app
2. Go to MongoDB Atlas dashboard
3. Click "Browse Collections"
4. You should see:
   - Database: `druggenius`
   - Collections: `users`, `recommendations`
   - Your registered user data

## Database Structure

### Users Collection
```json
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "username": "John Doe",
  "password": "hashed_password",
  "created_at": "2026-02-23T12:00:00Z"
}
```

### Recommendations Collection
```json
{
  "_id": ObjectId("..."),
  "user_email": "user@example.com",
  "recommendation_id": 1,
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

## Troubleshooting

### Connection Error: "Authentication failed"
- Check your username and password
- Make sure you replaced `<password>` in connection string
- Password should not contain special characters like `@`, `#`, `%`

### Connection Error: "IP not whitelisted"
- Go to Network Access
- Add `0.0.0.0/0` to allow all IPs
- Wait 2-3 minutes for changes to propagate

### "Module not found: pymongo"
```bash
pip install pymongo dnspython
```

### Data not persisting
- Check Vercel logs for MongoDB connection errors
- Verify MONGODB_URI environment variable is set
- Check MongoDB Atlas dashboard for connection attempts

## MongoDB Atlas Free Tier Limits

- **Storage**: 512 MB
- **RAM**: Shared
- **Connections**: 500 concurrent
- **Backup**: Not included (manual export only)

This is sufficient for:
- ~10,000 users
- ~100,000 recommendations
- Development and small production apps

## Monitoring

1. Go to MongoDB Atlas dashboard
2. Click "Metrics" to see:
   - Connections
   - Operations per second
   - Network traffic
   - Storage usage

## Backup (Manual)

1. Click "Browse Collections"
2. Select collection
3. Click "Export Collection"
4. Choose JSON or CSV format

## Security Best Practices

1. **Use strong passwords**
2. **Restrict IP access** in production
3. **Rotate credentials** regularly
4. **Enable audit logs** (paid feature)
5. **Use environment variables** (never commit credentials)

## Upgrading to Paid Tier

If you need more:
- M10 tier: $0.08/hour (~$57/month)
- Includes backups, more storage, dedicated resources

## Alternative: MongoDB Compass (GUI)

Download [MongoDB Compass](https://www.mongodb.com/products/compass) to:
- View data visually
- Run queries
- Manage indexes
- Export/import data

Connection string: Same as your app's MONGODB_URI

## Support

- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [MongoDB University](https://university.mongodb.com/) - Free courses
- [Community Forums](https://www.mongodb.com/community/forums/)

## Next Steps

After setup:
1. ✅ Test registration and login
2. ✅ Create some recommendations
3. ✅ Verify data persists after redeployment
4. ✅ Check MongoDB Atlas dashboard
5. ✅ Set up monitoring alerts (optional)

Your app now has persistent, scalable data storage! 🎉
