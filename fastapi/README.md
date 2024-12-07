# FastAPI Client Database Service

RESTful API service for accessing and querying the client database using FastAPI.

## API Endpoints

### Get Client by ID

---
GET /client/{client_id}
GET /client/{client_id}?field=Employer
---

### Search Clients

---
GET /clients/search?city=Seattle&gender=F
---

## Running the Server

---
uvicorn fastapi.main:app --reload
---

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Response Examples

### Single Client Response

---
{
    "Person_id": 230126,
    "FirstName": "John",
    "LastName": "Smith",
    "Gender": "M",
    "City": "Seattle",
    "State": "WA"
}
---

### Search Response

---
[
    {
        "Person_id": 230126,
        "FirstName": "Jane",
        "LastName": "Doe",
        "Gender": "F",
        "City": "Seattle",
        "State": "WA"
    }
]
---

## Dependencies

- fastapi: Web framework
- uvicorn: ASGI server
- pydantic: Data validation
- mysql-connector-python: Database connectivity

## Future Enhancements

- [ ] Authentication/Authorization
- [ ] Rate limiting
- [ ] Response caching
- [ ] Bulk operations endpoints
- [ ] Advanced filtering options
- [ ] OpenAPI specification enhancements