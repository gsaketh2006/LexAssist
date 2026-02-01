"""
Example cURL commands for testing the StartupLex Backend
Run these commands in PowerShell or terminal to test the API
"""

# Health Check
curl -X GET http://localhost:5000/

# Test Query 1 - Incorporation
$body = @{
    question = "What documents do I need to incorporate my startup?"
    context = ""
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/query" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body


# Test Query 2 - Equity
$body = @{
    question = "How should I structure equity for my first employees?"
    context = ""
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/query" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body


# Test Query 3 - SAFE Agreement
$body = @{
    question = "What is a SAFE and when should we use it?"
    context = ""
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/query" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body


# Test Query 4 - GDPR
$body = @{
    question = "What GDPR compliance do we need for our SaaS?"
    context = ""
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/query" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body


# Test Query 5 - IP Protection
$body = @{
    question = "How do we protect our intellectual property?"
    context = ""
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/query" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body


# Get Documents List
Invoke-WebRequest -Uri "http://localhost:5000/api/documents" `
    -Method GET


# Get Specific Document
Invoke-WebRequest -Uri "http://localhost:5000/api/documents/1" `
    -Method GET


# Test Chat Endpoint
$body = @{
    messages = @(
        @{
            role = "user"
            content = "What should be in our operating agreement?"
        }
    )
    session_id = "test-session-123"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/chat" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
