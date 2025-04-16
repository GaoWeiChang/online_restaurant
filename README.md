# Complex Food Online System

A complex online food ordering system built with Django (Python), PostgreSQL 14, and HTML/CSS/JavaScript. This platform are customers with restaurants, allowing for ordering and payment processing, while vendor collecting and processing orders for the customers.

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Django (Python web framework)
- Database: PostgreSQL 14
- APIs: [Paypal Payment API](https://developer.paypal.com/dashboard), [Google Map API](https://console.cloud.google.com/) 

## Core Features
### 1. Multi-vendor Marketplace Platform
- Vendor registration and authentication
- Vendor approval system with admin dashboards
### 2. Location-based Services
- Get user's current location to show nearby restaurants
- Utilize Google Map API to build Location-based search functionality
### 3. Menu Management and Order System
- Restaurant profile form with custom validators
- Menu Builder with food items and category
- Cart functionalities with AJAX requests
- Dynamic business hours module with AJAX
### 4. AJAX Functionality
- Dynamic cart management without page reload
- Real-time business hours updates
- Google Maps Autocomplete integration
- Dynamic menu item management
### 5. Payment System
- [PayPal Payment](https://developer.paypal.com/demo/checkout/#/pattern/server) Gateway by using Paypal payment API

## Project Structure
```
online_restaurant/
│
├── accounts/                 # User authentication, custom user model & profiles
├── customers/                # Customer-specific functionality
├── main_app/                 # Core application functionality
├── marketplace/              # Multi-vendor marketplace implementation
├── media/                    # User-uploaded files
├── menu/                     # Menu builder & food item management
├── orders/                   # Order processing and tracking
├── static/                   # Static files (CSS, JS)
├── templates/                # HTML templates
├── vendor/                   # Vendor registration, authentication & dashboard
├── .env-sample               # Environment variables template
└── manage.py                 # Django management script
```

## Results
