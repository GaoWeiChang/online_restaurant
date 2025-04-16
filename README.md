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
### Home Page
![image](https://github.com/user-attachments/assets/7c22462d-a001-406e-a44b-fa8a419d1a18)
![image](https://github.com/user-attachments/assets/07bbd325-0aaf-4c7b-9a6e-1831e04da138)
### Account Page
![image](https://github.com/user-attachments/assets/88d9ed08-7ed8-4f6a-a297-72204ac8ee6a)
![image](https://github.com/user-attachments/assets/d1b166cf-def6-4286-bea9-d3ed231bc8bf)
![image](https://github.com/user-attachments/assets/579c0150-c9b8-40e2-afce-2d128047ac2d)
![image](https://github.com/user-attachments/assets/cf1f3a7d-5a6b-4d95-b3a9-49d8f4e5dfa0)
### Vendor Page
![image](https://github.com/user-attachments/assets/09ce4573-6341-48e2-a03c-0658c1cd9333)
### Marketplace Page
![image](https://github.com/user-attachments/assets/1b151bf2-51f2-4c2a-be34-c2e7b6fe38b1)
### Cart Page
![image](https://github.com/user-attachments/assets/a7b8e900-ef1a-47d6-b2e8-80999a010b90)
![image](https://github.com/user-attachments/assets/1fc03079-25c3-4457-a103-27753ec4901d)
### Payment Page
<img width="927" alt="image" src="https://github.com/user-attachments/assets/f6405f10-005b-45a7-98fd-8fabebcb8a7a" />

### Location Search Functionality
![image](https://github.com/user-attachments/assets/f27804cd-d2cc-4666-abf8-7a12d51f2872)
![image](https://github.com/user-attachments/assets/7ab5a3b8-cce3-44b1-8c37-e91e059fb64e)

