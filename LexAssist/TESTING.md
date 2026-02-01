# StartupLex Backend - Testing Guide

## Quick Start with Test Mode

The backend is configured to run in **TEST MODE** by default, which uses mock responses instead of requiring a RAG API.

### 1. Start the Flask Backend

```powershell
.\.venv\Scripts\python.exe app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
```

### 2. Test the Backend (Option A - Python Script)

Run the automated test script:

```powershell
.\.venv\Scripts\python.exe test_backend_quick.py
```

This will test all 10 sample queries and display the responses.

### 3. Test via Browser (Option B - Manual Testing)

1. Open `query.html` in your browser
2. Try asking one of these questions:
   - "What documents do I need to incorporate my startup?"
   - "How should I structure equity for my first employees?"
   - "What is a SAFE and when should we use it?"
   - "What GDPR compliance do we need for our SaaS?"
   - "How do we protect our intellectual property?"

The response should appear after a brief loading animation.

### 4. Test via PowerShell (Option C - API Testing)

Run the PowerShell test examples:

```powershell
# Health check
Invoke-WebRequest -Uri "http://localhost:5000/" -Method GET

# Test a query
$body = @{
    question = "What documents do I need to incorporate my startup?"
    context = ""
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/query" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

## Configuration

### Test Mode (Current)
- **Status**: Enabled by default
- **File**: `.env` (create from `.env.example`)
- **Setting**: `TEST_MODE=True`
- **Behavior**: Returns mock responses from `test_queries.py`

### Production Mode (When RAG API is Ready)
To switch to your RAG API:

1. Update `.env`:
   ```
   TEST_MODE=False
   RAG_API_URL=http://your-rag-api-url:port
   RAG_API_ENDPOINT=/your-endpoint
   RAG_API_KEY=your-api-key-if-needed
   ```

2. Restart the Flask backend

## Test Files

### `test_queries.py`
Contains 10 sample questions and responses:
1. Incorporation documents
2. Employee equity structure
3. SAFE agreements
4. GDPR compliance
5. IP protection
6. Founder vesting
7. Operating agreements
8. Employment agreements
9. Business licenses
10. C-Corp vs S-Corp

### `test_backend_quick.py`
Automated test script that:
- Checks server health
- Sends all 10 test queries
- Displays formatted responses
- Verifies API is working

### `test_backend.py`
Unit tests using Python unittest framework:
```powershell
python test_backend.py              # Run all tests
python test_backend.py mock         # Show mock responses
```

## Testing the Frontend Display

The responses should display in the browser with:
- ✓ Proper formatting (paragraphs and lists)
- ✓ Loading animation while waiting
- ✓ Response visible in the response section
- ✓ Ability to ask another question
- ✓ Save/share response buttons working

## Expected Response Format

Test responses are plain text that get formatted into HTML by the `formatResponse()` function in the JavaScript.

Example test response:
```
To incorporate your startup, you'll need Articles of Incorporation, Corporate Bylaws, Board Resolutions, Founder Stock Agreements, and 83(b) Election Forms filed with your state and the IRS.
```

## Troubleshooting

### Backend not responding
- Make sure Flask is running: `.\.venv\Scripts\python.exe app.py`
- Check that port 5000 is available
- Verify no firewall blocking localhost:5000

### Frontend not showing responses
- Check browser console (F12) for JavaScript errors
- Verify `API_BASE_URL` in `query.html` is correct
- Make sure CORS is enabled (it is in the Flask app)

### Getting wrong responses
- In TEST_MODE, responses are matched by keywords
- If a question doesn't match test queries well, a generic response is returned
- This is expected behavior - the RAG API will improve this

## Next Steps

1. ✓ Test the frontend with test mode (this document)
2. ✓ Verify responses display correctly
3. → Connect to your actual RAG API
4. → Fine-tune response formatting
5. → Deploy to production

## API Endpoints Summary

| Endpoint | Method | Mode | Description |
|----------|--------|------|-------------|
| `/` | GET | All | Health check |
| `/api/query` | POST | All | Submit legal question |
| `/api/documents` | GET | All | List compliance docs |
| `/api/chat` | POST | All | Multi-turn conversation |

## Notes

- Test mode returns consistent responses for testing
- No external API calls are made in test mode
- Responses are based on simple keyword matching
- Perfect for UI/UX testing and frontend development
- Switch to production mode once RAG API is ready
