# 🚀 Deploying IST Vulnerable Web App to Vercel

## Quick Deploy

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Go to Vercel**: https://vercel.com
2. **Sign in** with your GitHub account
3. **Import Project**:
   - Click "Add New..." → "Project"
   - Select your `raidscanner` repository
   - Choose the `lab` branch
4. **Configure Project**:
   - Framework Preset: **Other**
   - Root Directory: **vulnerable-webapp**
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
   - Install Command: `npm install`
5. **Deploy**: Click "Deploy"

### Option 2: Deploy via Vercel CLI

```bash
cd vulnerable-webapp

# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Deploy to production
vercel --prod
```

## 🔧 Configuration

The project includes `vercel.json` with the following configuration:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "server.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "server.js"
    }
  ]
}
```

## 🎯 After Deployment

Your app will be available at:
```
https://your-project-name.vercel.app
```

## 🧪 Testing with RaidScanner

Once deployed, test it with your scanner:

### SQL Injection Tests
```bash
# Replace with your Vercel URL
export TARGET="https://your-app.vercel.app"

# Test login
echo "$TARGET/portal/login" > targets.txt

# Test search
echo "$TARGET/search?q=test" >> targets.txt

# Test API
echo "$TARGET/api/students?department=Computer" >> targets.txt

# Run RaidScanner
docker compose run --rm raidscanner-cli
# Select SQLi scanner and provide targets.txt
```

### LFI Tests
```bash
echo "$TARGET/files?file=syllabus.txt" > lfi-targets.txt
echo "$TARGET/files?file=schedule.txt" >> lfi-targets.txt
```

### Open Redirect Tests
```bash
echo "$TARGET/redirect?url=https://google.com" > or-targets.txt
```

## ⚙️ Environment Variables (Optional)

If you need to add environment variables:

1. Go to Project Settings → Environment Variables
2. Add variables like:
   - `NODE_ENV=production`
   - `PORT=3000` (Vercel handles this automatically)

## 🔄 Automatic Deployments

Vercel automatically deploys when you push to the `lab` branch:

```bash
# Make changes
git add .
git commit -m "Update vulnerable webapp"
git push origin lab

# Vercel will automatically deploy!
```

## 📊 Monitoring

- **Deployment Logs**: Check Vercel dashboard
- **Function Logs**: View runtime logs in Vercel
- **Analytics**: Enable Web Analytics in project settings

## 🐛 Troubleshooting

### Issue: Build fails
**Solution**: Ensure `package.json` is correct and all dependencies are listed

### Issue: Routes not working
**Solution**: Check `vercel.json` configuration matches the project structure

### Issue: Database not persisting
**Note**: SQLite uses in-memory database, which resets on each deployment. This is intentional for the vulnerable app.

### Issue: Module not found
**Solution**: Run `npm install` locally first to test dependencies

## 🔗 Custom Domain (Optional)

1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. SSL certificate is automatically provisioned

## 📝 Important Notes

- ⚠️ This is an **intentionally vulnerable** application
- 🔒 Do NOT use real user data
- 🎓 For educational purposes only
- 🧪 Perfect for testing RaidScanner
- 🚫 Never use in production environments

## 🎬 Demo URLs Structure

After deployment, your app will have:

- Homepage: `https://your-app.vercel.app/`
- Student Portal: `https://your-app.vercel.app/portal`
- Course Search: `https://your-app.vercel.app/search`
- File Viewer: `https://your-app.vercel.app/files`
- API: `https://your-app.vercel.app/api/students`

## 🧪 Integration with RaidScanner

Update RaidScanner documentation with your live URL:

```bash
# In RaidScanner Web GUI
Target URL: https://your-app.vercel.app/portal/login
Threads: 5
Scanner: SQLi
```

Perfect for demonstrating your final year project! 🎓
