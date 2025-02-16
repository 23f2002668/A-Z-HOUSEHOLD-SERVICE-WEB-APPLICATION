# **A-Z-HOUSEHOLD-SERVICE-WEB-APPLICATION**


# Overview / Vision :-
In a fast-paced world where time is precious and convenience is key, A-Z Household Service App
aspires to be the go-to platform for all your home service needs, delivering an unparalleled experience
that blends quality, reliability, and ease of use. A-Z Household Service App is the idea of simplicity and
accessibility through which anyone, regardless of their technical skills or busy schedules, can access top-
tier household services without the hassle of searching for multiple providers or dealing with unreliable
contractors. With just one app, users will be able to book vetted, highly skilled professionals for a wide
range of home services—from plumbing and electrical work to deep cleaning and pest control—at
competitive prices and with a high level of transparency.

---

# Functionality Of A-Z Household Application :-

**1. Admin login and user login**

* A login/register form with fields like username, password etc. for customer, service professional
and admin login
* Separate forms for each type of user
* Use a proper login framework with a simple HTML form with username and password (we are not concerned with how secure the login or the app is)
* The app have a suitable model to store and differentiate all the types of user of the app.

**2. Admin Dashboard - for the Admin**

* Admin login redirects to admin dashboard
* Admin will manage all the users (customers/service professional)
* Admin will approve a service professional after verification of profile docs
* Admin will block customer/service professional based on fraudulent activity/poor reviews

**3. Service Management - for the Admin**

* Create a new service with a base price.
* Update an existing service - e.g. name, price, time_required and/or other fields
* Delete an existing service

**5. Service Request - for the customers**
* Create a new service request based on the services available
* Edit an existing service request - e.g. date_of_request, completion status, remarks etc
* Close an existing service request.
  
**6. Search for available services**
* The customers should be able to search for available services based on their location, name, pin
code etc.
* The admin should be able to search for a professional to block/unblock/review them.

**7. Take action on a particular service request - for the service professional**
* Ability to view all the service requests from all the customers
* Ability to accept/reject a particular service request
* Ability to close the service request once completed

---

# Challenges Faced:-
* Designing role-based access to functionalities.
* Implementing effective database relationships for seamless operations.

---

# Frameworks and Libraries :-
* Flask for application code
* Jinja2 templates + Bootstrap for HTML generation and styling
* SQLite for data storage

---

# Database Structure:-

**Payments :**
* CustomerName
* CustomerEmail
* ProfessionalName
* ProfessionalEmail
* Service
* Amount
* Date
  
**ProfessionalServices :**
* UserEmail
* UserName
* CustomerName
* CustomerEmail
* CustomerAddress
* BasePrice
* Date
* Status
* Ratings
  
**ServiceProviders :**
* Email
* UserName
* Dob
* Category
* Experience
* Address
* Pincode
* Date
* Status

**ServiceUsers :**
* Email
* UserName
* Dob
* Address
* Pincode
* Date
  
**Services :**
* ServiceId
* Category
* Service
* BasePrice
* Date
* Description

**UserDetails :**
* Email
* UserName
* UserType
* Date
* Password

**UserServices :**
* Email
* CustomerName
* Service
* Category
* ProfessionalName
* ProfessionalEmail
* BAsePrice
* Status
* Date
