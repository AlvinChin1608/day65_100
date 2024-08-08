# day65_100
# RESTful APIs and HTTP Methods

## Overview
**REST (REpresentational State Transfer)** is an architectural style used for designing networked applications. It operates over HTTP and defines a set of constraints and properties based on the principles of the client-server architecture.

### Note
RESTful services emphasize simplicity, statelessness, and using HTTP methods (GET, POST, PUT, DELETE) for CRUD operations.

While SOAP can be transported over HTTP, it doesn't inherently follow RESTful principles. GraphQL and FALCOR offer alternative approaches to data fetching and are not considered RESTful.   

In essence, while SOAP, GraphQL, and FALCOR can be used to build APIs, they represent different architectural styles and have distinct characteristics compared to RESTful services.

## Key Concepts

1. __Client-Server Architecture:__
Clients make requests to servers using HTTP methods.
Servers process these requests, perform necessary computations, or interact with databases, and then return responses.

2. __Building APIs:__
An API (Application Programming Interface) acts like a menu between the client and server, listing available operations and their expected inputs and outputs.

3. __RESTful Constraints:__
REST is not a protocol but an architectural style with specific constraints that APIs should follow to be considered RESTful.

## HTTP Methods
RESTful APIs use standard HTTP methods to perform CRUD (Create, Read, Update, Delete) operations:

- __GET:__ Retrieve information from the server.
- __POST:__ Submit data to be processed by the server.
- __PUT:__ Update an existing resource or create it if it does not exist.
- __PATCH:__ Apply partial modifications to a resource.
- __DELETE:__ Remove a resource from the server.

## Routing and Endpoints
Endpoints define the routes available in an API. Each route may correspond to different actions based on the HTTP method used:

## Example Routes and Methods
Here is a list of API endpoints available in this project:
```python
# API Endpoints
| HTTP Verb | Endpoint                       | Description                                    |
|-----------|--------------------------------|------------------------------------------------|
| GET       | `/random`                      | Fetches a random cafe                          |
| GET       | `/all`                         | Fetches all cafes                              |
| GET       | `/search?loc=location`         | Fetches cafes matching the specified location  |
| POST      | `/add`                         | Creates a new cafe                             |
| PATCH     | `/update-price/<int:cafe_id>`  | Updates the price of the specified cafe        |
| DELETE    | `/report-closed/<int:cafe_id>?api-key=YourAPIKey` | Deletes the specified cafe  |
```

## JSON Serialization
To convert Python objects into JSON format, use the jsonify() function in Flask:
```python
from flask import jsonify

@app.route("/example")
def example():
    data = {"key": "value"}
    return jsonify(data)
```
## Testing APIs with Postman
For testing RESTful APIs, tools like Postman are invaluable. They allow you to simulate HTTP requests to your endpoints, validate responses, and debug issues without manually typing URLs.

### Example Postman Setup:

1. **Method:** POST
2. **URL:** http://127.0.0.1:5000/add
3. **Body:**
Key: name, Value: Cafe XYZ
Key: map_url, Value: http://example.com/map
Key: img_url, Value: http://example.com/image.jpg
Key: location, Value: Downtown
Key: seats, Value: 20
Key: has_toilet, Value: true
Key: has_wifi, Value: true
Key: has_sockets, Value: true
Key: can_take_calls, Value: true
Key: coffee_price, Value: 5.00

## Code Example
Here’s a sample Flask code snippet demonstrating a RESTful endpoint for adding a cafe:
```python
@app.route("/add", methods=["POST"])
def add_cafe():
    name = request.form.get("name")
    map_url = request.form.get("map_url")
    img_url = request.form.get("img_url")
    location = request.form.get("location")
    seats = request.form.get("seats")
    has_toilet = bool(request.form.get("has_toilet"))
    has_wifi = bool(request.form.get("has_wifi"))
    has_sockets = bool(request.form.get("has_sockets"))
    can_take_calls = bool(request.form.get("can_take_calls"))
    coffee_price = request.form.get("coffee_price")

    new_cafe = Cafe(
        name=name,
        map_url=map_url,
        img_url=img_url,
        location=location,
        seats=seats,
        has_toilet=has_toilet,
        has_wifi=has_wifi,
        has_sockets=has_sockets,
        can_take_calls=can_take_calls,
        coffee_price=coffee_price
    )

    db.session.add(new_cafe)
    db.session.commit()
    return jsonify({"message": "Cafe added successfully!"}), 201
```

## DEMO
### SQLite DBMS
![](https://github.com/AlvinChin1608/day65_100/blob/main/screenshots_demo/SQL_DBMS.png)

### GET on POSTMAN
![](https://github.com/AlvinChin1608/day65_100/blob/main/screenshots_demo/GET-all_cafe.png)

### POST on POSTMAN
![](https://github.com/AlvinChin1608/day65_100/blob/main/screenshots_demo/POST_new_cafe.png)

### Add form 
![](https://github.com/AlvinChin1608/day65_100/blob/main/screenshots_demo/Screenshot%202024-08-07%20at%2023.26.19.png)

### PATCH 
![](https://github.com/AlvinChin1608/day65_100/blob/main/screenshots_demo/PATCH-Update_Coffee_Price_for_cafe.png)

### DELETE
1[](https://github.com/AlvinChin1608/day65_100/blob/main/screenshots_demo/DELETE-a_cafe_by_ID.png)

