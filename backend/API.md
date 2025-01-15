# Backend API Specifications

## Base URL
```
http://localhost:8000/api
```

## Authentication
Most endpoints require authentication using JWT (JSON Web Token) in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### Authentication

#### Register User
```
POST /auth/register
```
Request Body:
```json
{
  "email": "string",
  "password": "string"
}
```
Response (200):
```json
{
  "id": "integer",
  "email": "string"
}
```
Error Responses:
- 400: Email already registered
- 422: Validation Error

#### Login
```
POST /auth/login
```
Request Body:
```json
{
  "email": "string",
  "password": "string"
}
```
Response (200):
```json
{
  "token": "string",
  "token_type": "bearer"
}
```
Error Responses:
- 401: Invalid credentials
- 422: Validation Error

### Items

#### Get All Items
```
GET /items/
```
Query Parameters:
- skip (optional): integer (default: 0)
- limit (optional): integer (default: 100)

Response (200):
```json
[
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "quantity": "integer",
    "category_id": "integer"
  }
]
```

#### Get Item by ID
```
GET /items/{item_id}
```
Response (200):
```json
{
  "id": "integer",
  "name": "string",
  "description": "string",
  "quantity": "integer",
  "category_id": "integer"
}
```
Error Responses:
- 404: Item not found

#### Create Item
```
POST /items/
```
Request Body:
```json
{
  "name": "string",
  "description": "string",
  "quantity": "integer",
  "category_id": "integer"
}
```
Response (200): Created item object

#### Update Item
```
PUT /items/{item_id}
```
Request Body: Same as Create Item
Response (200): Updated item object
Error Responses:
- 404: Item not found

#### Delete Item
```
DELETE /items/{item_id}
```
Response (200): boolean
Error Responses:
- 404: Item not found

#### Adjust Item Quantity
```
PATCH /items/{item_id}/quantity
```
Request Body:
```json
{
  "quantity_change": "integer"
}
```
Response (200): Updated item object
Error Responses:
- 404: Item not found

### Categories

#### Get All Categories
```
GET /categories/
```
Query Parameters:
- skip (optional): integer (default: 0)
- limit (optional): integer (default: 100)

Response (200):
```json
[
  {
    "id": "integer",
    "name": "string",
    "description": "string"
  }
]
```

#### Get Category by ID
```
GET /categories/{category_id}
```
Response (200):
```json
{
  "id": "integer",
  "name": "string",
  "description": "string"
}
```
Error Responses:
- 404: Category not found

#### Create Category
```
POST /categories/
```
Request Body:
```json
{
  "name": "string",
  "description": "string"
}
```
Response (200): Created category object

#### Update Category
```
PUT /categories/{category_id}
```
Request Body: Same as Create Category
Response (200): Updated category object
Error Responses:
- 404: Category not found

#### Delete Category
```
DELETE /categories/{category_id}
```
Response (200): boolean
Error Responses:
- 404: Category not found

### Transactions

#### Get All Transactions
```
GET /transactions/
```
Query Parameters:
- skip (optional): integer (default: 0)
- limit (optional): integer (default: 100)

Response (200):
```json
[
  {
    "id": "integer",
    "item_id": "integer",
    "quantity_change": "integer",
    "transaction_date": "string (datetime)",
    "transaction_type": "string",
    "user_id": "integer"
  }
]
```

#### Get Transaction by ID
```
GET /transactions/{transaction_id}
```
Response (200):
```json
{
  "id": "integer",
  "item_id": "integer",
  "quantity_change": "integer",
  "transaction_date": "string (datetime)",
  "transaction_type": "string",
  "user_id": "integer"
}
```
Error Responses:
- 404: Transaction not found

#### Create Transaction
```
POST /transactions/
```
Request Body:
```json
{
  "item_id": "integer",
  "quantity_change": "integer",
  "transaction_type": "string"
}
```
Response (200): Created transaction object
Error Responses:
- 404: Item not found

#### Delete Transaction
```
DELETE /transactions/{transaction_id}
```
Response (200): boolean
Error Responses:
- 404: Transaction not found

## Error Responses
All error responses follow this format:
```json
{
  "detail": "string"
}
```

Common HTTP Status Codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 422: Validation Error
- 500: Internal Server Error 