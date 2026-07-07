# Flask Inventory Management System

A robust, production-grade Python Flask REST API supplemented with a real-time command-line interface (CLI) administrative management console and an automated testing suite.

## Setup & Installations

1. Clone the repository and enter the directory:
   cd summative-lab

2. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies:
   pip install flask flask-cors requests pytest

---

## Running the Components

### 1. Launch the API Engine Server
python app.py

### 2. Launch Administrative Interface Panel (In a separate terminal window)
python cli.py

### 3. Run the Automated Test Suite
pytest -v test_app.py

---

## API Architecture & Schema Blueprint

### Data Exchange Contracts

#### Manual Creation Payload (POST /inventory)
* Request Body:
  {
    "product_name": "Organic Almond Milk",
    "price": 3.99,
    "stock": 45
  }
* Response (201 Created):
  {
    "id": 1,
    "product_name": "Organic Almond Milk",
    "brands": "Generic",
    "ingredients_text": "N/A",
    "price": 3.99,
    "stock": 45
  }

#### Barcode Automation Payload (POST /inventory)
If a barcode parameter is supplied in the JSON request payload, the backend intercepts manual creation and routes the workflow directly through the OpenFoodFacts External API:
  {
    "barcode": "737628011862",
    "price": 4.49,
    "stock": 15
  }
* Success Path: Dynamically extracts product_name, brands, and ingredients_text directly from live global food record metrics.
* Network Fallback Path: If the OpenFoodFacts API is unreachable, a structural fail-safe interceptor instantiates a "Fallback Product" record so your localized sales pipelines never freeze.

---

## Endpoint Matrix & Status Map

* GET /inventory
  - Description: Fetches complete stock list tracking arrays
  - Expected Status: 200 OK

* GET /inventory/<id>
  - Description: Grabs detail data schemas for an isolated item
  - Expected Status: 200 OK, 404 Not Found

* POST /inventory
  - Description: Creates item entries manually OR processes barcodes
  - Expected Status: 201 Created, 400 Bad Request

* PATCH /inventory/<id>
  - Description: Updates specified metrics dynamically
  - Expected Status: 200 OK, 400 Bad Request, 404 Not Found

* DELETE /inventory/<id>
  - Description: Purges an item permanently from inventory listings
  - Expected Status: 200 OK, 404 Not Found

### Global Application Resilience Map
* 400 BAD REQUEST — Triggered on missing vital payload properties or improperly formatted JSON bodies.
* 415 UNSUPPORTED MEDIA TYPE — Triggered if mutations are sent without explicit application/json Content-Type headers.
* License
MIT License — see LICENSE file.
