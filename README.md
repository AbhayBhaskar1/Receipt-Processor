# Receipt Processor API

## Overview
This project implements a receipt processor web service using FastAPI. The API calculates reward points for submitted receipts based on specific criteria including retailer name, purchase date, and items purchased. Users can submit receipts and retrieve points awarded using unique receipt IDs.

## Prerequisites
- Python 3.9
- FastAPI
- Uvicorn
- Docker

## Setup

### Local Setup with Python
1. Clone the repository:
   ```bash
   git clone 
   cd receipt-processor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker Setup
1. Build the image:
   ```bash
   docker build -t receipt-processor .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 receipt-processor
   ```

The API will be available at `http://localhost:8000` for both setup methods.


