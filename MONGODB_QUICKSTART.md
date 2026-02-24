# MongoDB Atlas Quick Start (5 Minutes)

## Step 1: Create Account (1 minute)

1. Open: https://www.mongodb.com/cloud/atlas/register
2. Sign up with:
   - Email: `pavancg61@gmail.com` (or your email)
   - Or use Google/GitHub sign-in
3. Verify your email

## Step 2: Create FREE Cluster (2 minutes)

1. After login, click **"Build a Database"**
2. Choose **"M0 FREE"** tier (should be selected by default)
3. Cloud Provider: **AWS** (recommended)
4. Region: Choose closest to you:
   - **Mumbai (ap-south-1)** - if in India
   - **Singapore (ap-southeast-1)** - if in Asia
   - **N. Virginia (us-east-1)** - if in US
5. Cluster Name: Keep default or name it `DrugGenius`
6. Click **"Create"** button
7. Wait 3-5 minutes (cluster is being created)

## Step 3: Create Database User (1 minute)

While cluster is creating:

1. You'll see "Security Quickstart" popup
2. **Username**: `druggenius_admin`
3. **Password**: Click "Autogenerate Secure Password"
4. **COPY AND SAVE THIS PASSWORD!** (You'll need it)
5. Click **"Create User"**

## Step 4: Add Your IP Address (30 seconds)

1. Still in Security Quickstart popup
2. Click **"Add My Current IP Address"**
3. Then click **"Add Entry"**
4. For development, also add:
   - Click "Add IP Address"
   - Enter: `0.0.0.0/0` (allows all IPs)
   - Description: "Allow all"
   - Click "Add Entry"
5. Click **"Finish and Close"**

## Step 5: Get Connection String (1 minute)

1. Click **"Connect"** button on your cluster
2. Choose **"Drivers"**
3. Driver: **Python**
4. Version: **3.6 or later**
5. Copy the connection string (looks like this):

```
mongodb+srv://druggenius_admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

6. **IMPORTANT**: Replace `<password>` with your actual password
7. Add database name `/druggenius` before the `?`:

**BEFORE:**
```
mongodb+srv://druggenius_admin:MyPass123@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

**AFTER:**
```
mongodb+srv://druggenius_admin:MyPass123@cluster0.xxxxx.mongodb.net/druggenius?retryWrites=true&w=majority
```

## Step 6: Add to Vercel (1 minute)

1. Go to: https://vercel.com/pavancg61-7323s-projects/drug-recommendation/settings/environment-variables

2. Click **"Add New"** button

3. Fill in:
   - **Key**: `MONGODB_URI`
   - **Value**: Paste your connection string (with password and /druggenius)
   - **Environments**: Check all three boxes (Production, Preview, Development)

4. Click **"Save"**

5. Go to: https://vercel.com/pavancg61-7323s-projects/drug-recommendation

6. Click **"Redeploy"** button (or wait for auto-deploy)

## Step 7: Test It! (1 minute)

1. Visit your app: https://drug-recommendation-ten.vercel.app

2. Register a new user

3. Create some recommendations

4. Go back to MongoDB Atlas:
   - Click "Browse Collections"
   - You should see:
     - Database: `druggenius`
     - Collections: `users`, `recommendations`
     - Your data inside!

## ✅ Success Indicators

You'll know it's working when:
- ✅ You can register and login
- ✅ Recommendations are saved
- ✅ Data persists after page refresh
- ✅ Data shows in MongoDB Atlas dashboard
- ✅ Vercel logs show: "✅ Connected to MongoDB Atlas successfully"

## 🔍 Check Vercel Logs

To verify MongoDB connection:

1. Go to: https://vercel.com/pavancg61-7323s-projects/drug-recommendation
2. Click on latest deployment
3. Click "Functions" tab
4. Look for: "✅ Connected to MongoDB Atlas successfully"

## ⚠️ Troubleshooting

### "Authentication failed"
- Check password in connection string
- Make sure you replaced `<password>` with actual password
- Password shouldn't have special characters like `@`, `#`, `%`

### "IP not whitelisted"
- Go to Network Access in MongoDB Atlas
- Add `0.0.0.0/0` to allow all IPs
- Wait 2-3 minutes

### "Module not found: pymongo"
- Already fixed in requirements.txt
- Vercel will install automatically

### Still using JSON files?
- Check Vercel environment variables are set
- Redeploy after adding MONGODB_URI
- Check Vercel logs for errors

## 📊 Monitor Your Database

MongoDB Atlas Dashboard:
- **Metrics**: See connections, operations
- **Browse Collections**: View your data
- **Charts**: Visualize data (optional)

## 🎉 You're Done!

Your app now has:
- ✅ Persistent data storage
- ✅ Scalable database (up to 512MB free)
- ✅ Automatic backups
- ✅ Professional infrastructure

## Next Steps (Optional)

1. **Set up monitoring alerts** in MongoDB Atlas
2. **Create indexes** for better performance (already done automatically)
3. **Export data** regularly for backup
4. **Upgrade to paid tier** if you need more storage

## Need Help?

- MongoDB Atlas Docs: https://docs.atlas.mongodb.com/
- MongoDB University: https://university.mongodb.com/ (free courses)
- Support: https://www.mongodb.com/support

---

**Estimated Total Time**: 5-10 minutes
**Cost**: $0 (Free tier)
**Storage**: 512 MB (enough for ~10,000 users)
