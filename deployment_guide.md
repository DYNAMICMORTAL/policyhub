# Vercel Deployment Guide for PolicyIntelliHub

## Prerequisites
1. Vercel account (https://vercel.com)
2. Google Gemini API key
3. Git repository

## Deployment Steps

### 1. Install Vercel CLI
```bash
npm i -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Set Environment Variables
```bash
vercel env add GEMINI_API_KEY
# Enter your Google Gemini API key when prompted

vercel env add SECRET_KEY
# Enter a secure secret key when prompted
```

### 4. Deploy
```bash
vercel --prod
```

## Important Notes

### Environment Variables Required:
- `GEMINI_API_KEY`: Your Google Gemini API key
- `SECRET_KEY`: Flask session secret key

### Limitations on Vercel:
- Serverless functions have execution time limits (60s max)
- File storage is temporary (use `/tmp/` directory)
- No persistent storage between requests
- PDF processing may timeout for large files

### Recommended for Production:
- Use external database (PostgreSQL, MongoDB)
- Implement file storage service (AWS S3, Cloudinary)
- Add error handling for timeout scenarios
- Consider using Vercel Pro for longer execution times

## Testing Your Deployment

1. Visit your Vercel URL
2. Test the health endpoint: `https://your-app.vercel.app/health`
3. Try analyzing a simple policy clause
4. Check the analytics page

## Troubleshooting

### Common Issues:
1. **Build fails**: Check requirements.txt for compatibility
2. **API timeouts**: Reduce complexity or increase timeout limits
3. **File upload issues**: Ensure `/tmp/` directory usage
4. **Environment variables**: Verify they're set correctly in Vercel dashboard

### Logs:
- View function logs in Vercel dashboard
- Use `vercel logs` command for real-time monitoring
