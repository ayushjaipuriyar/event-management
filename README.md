# Event Management System - Backend API Documentation

This repository contains the backend API documentation for a fictional event management system developed using Django and Django Rest Framework.

## Description
The event management system allows users to manage events, registrations, venues, and user profiles. The system supports two types of user roles: Admin and Participants.

## Tech Stack
- Django (using Django Rest Framework for designing APIs)
- SQLite
- 
## Models
### Users
```json

"username": "CharField (max_length=150, unique=True)"
"email": "EmailField"
"fullname": "CharField (max_length=255)"
"role": "CharField (max_length=20, choices=[('admin', 'Admin'), ('participant', 'Participant')])"
```
### Events
```json
    "title" : "models.CharField(max_length=100)"
    "description" : "models.TextField()"
    "start_time" : "models.DateTimeField(default=None)"
    "end_time" : "models.DateTimeField(default=None)"
    "capacity" : "models.PositiveIntegerField(default=0)"
    "categories" : "models.ManyToManyField('Category', related_name='events')"
    "tags" : "models.CharField(max_length=100)"
    "creator" : "models.CharField(max_length=150, default=None)"
    "venue" : "models.ForeignKey(Venue, on_delete=models.CASCADE, to_field='name', default=None)"
```
### Category
```json
    "name" : "models.CharField(max_length=100)"
```
### Venues
```json
    "name" : "models.CharField(max_length=100, unique=True)"
    "capacity" : "models.PositiveIntegerField()"
    "amenities" : "models.TextField()"
```
### Registrations
```json
    "event" : "models.ForeignKey(Event, on_delete=models.CASCADE)"
    "user" : "models.ForeignKey(User, on_delete=models.CASCADE)"
    "status" : "models.CharField(max_length=20, choices=[('Pending', 'Pending'),('Accepted', 'Accepted'), ('Rejected', 'Rejected')])"
```

## Endpoints
### User Endpoints
#### User Registration
- URL: /api/users/signup/
- Method: POST
- Description: Register a new user
- Request Body:
```json
{
    "username": "john_doe",
    "email": "john.doe@example.com",
    "password": "password123",
    "fullname": "John Doe",
    "role": "participant"
}
```
- Response: None
#### User Login
- URL: /api/users/signin/
- Method: POST
- Description: Authenticate a user and retrieve an access token
- Request Body:
```json
{
    "email": "john.doe@example.com",
    "password": "password123"
}
```
- Response: None
#### User Registrations
- URL: /api/users/registrations/
- Method: GET
- Description: Get registrations for the authenticated user
- Authorization Header: Authorization: Bearer {{access_token}}
- Response: List of registrations for the user
#### Admin User List
- URL: /api/users/admin/users/
- Method: GET
- Description: Get the list of all participants
- Authorization Header: Authorization: Bearer {{access_token}}
- Response: List of user profiles for all participants
- Admin User Detail
- URL: /api/users/admin/users/5/
- Method: GET
- Description: Get the details of a specific user
- Authorization Header: Authorization: Bearer {{access_token}}
- Response: User profile details

### Event Endpoints
#### Event List
- URL: /api/events/
- Method: GET
- Description: Get the list of all events
- Response: List of all events

####Event Detail
- URL: /api/events/1/
- Method: GET
- Description: Get the details of a specific event
- Response: Event details

####Create Event
- URL: /api/events/create/
- Method: POST
- Description: Create a new event
- Authorization Header: Authorization: Bearer {{access_token}}
- Request Body:
```json
{
    "title": "Sample Event",
    "description": "This is a sample event",
    "date": "2023-07-05",
    "venue": 1
}
```
- Response: None

#### Event Registrations
- URL: /api/events/1/registrations/
- Method: GET
- Description: Get registrations for a specific event
- Authorization Header: Authorization: Bearer {{access_token}}
- Response: List of registrations for the event

####Create Registration
- URL: /api/events/1/register/
- Method: POST
- Description: Register for an event
- Authorization Header: Authorization: Bearer {{access_token}}
- Request Body:
```json
{
    "event": 1,
    "user": 5,
    "status": "pending"
}
```

#### Update Registration Status
- URL: /api/events/1/registrations/5/update_status/
- Method: PUT
- Description: Update the status of a registration for a specific event
- Authorization Header: Authorization: Bearer {{access_token}}
- Request Body:
```json
{
    "status": "approved"
}
```
- Response: None

#### Venue List
- URL: /api/venues/
- Method: GET
- Description: Get the list of all venues
- Response: List of all venues

#### Venue Detail
- URL: /api/venues/1/
- Method: GET
- Description: Get the details of a specific venue
- Response: Venue details

#### Create Venue
- URL: /api/venues/create/
- Method: POST
- Description: Create a new venue
- Authorization Header: Authorization: Bearer {{access_token}}
- Request Body:
```json
{
    "name": "Sample Venue",
    "address": "123 Main Street",
    "capacity": 100
}
```
- Response: None

#### Update Venue
- URL: /api/venues/1/update/
- Method: PUT
- Description: Update the details of a specific venue
- Authorization Header: Authorization: Bearer {{access_token}}
- Request Body:
```json
{
    "name": "Updated Venue Name",
    "address": "456 Elm Street",
    "capacity": 150
}
```
- Response: None

#### Delete Venue
- URL: /api/venues/1/delete/
- Method: DELETE
- Description: Delete a specific venue
- Authorization Header: Authorization: Bearer {{access_token}}
- Response: None
