# Deployment Instructions

## Vercel Deployment

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Add environment variable:
```bash
vercel env add GEMINI_API_KEY
```

4. Deploy:
```bash
vercel --prod
```

## Heroku Deployment

1. Install Heroku CLI and login:
```bash
heroku login
```

2. Create Heroku app:
```bash
heroku create your-app-name
```

3. Set environment variables:
```bash
heroku config:set GEMINI_API_KEY=your_api_key
heroku config:set SECRET_KEY=your_secret_key
```

4. Deploy:
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## Environment Variables Required

- `GEMINI_API_KEY`: Your Google Gemini API key
- `SECRET_KEY`: Flask secret key for sessions
- `FLASK_ENV`: Set to 'production' for production

## Notes

- File uploads are limited in serverless environments
- PDF processing uses temporary storage
- Analytics data uses sample data in cloud environments
- For persistent storage, consider adding a database like PostgreSQL
