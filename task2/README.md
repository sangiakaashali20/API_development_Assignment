# Flask API Key Generation and Sharing

## Project Description
This project is a Flask API that accepts text and converts it into uppercase letters.

## API Endpoint
- Method: POST
- Endpoint: `/process`
- Input: JSON containing text
- Output: Uppercase text

## API Key Authentication
- Three unique API keys are generated for three consumers.
- The API key is sent using the `X-API-Key` header.
- Invalid or missing API keys are rejected.

## Technologies Used
- Python
- Flask
- JSON
- PowerShell

## Testing
All three consumers were tested with valid API keys. Invalid and missing API keys were also tested.