### Vendor Management Project

The Vendor Management System is a web application developed using Django, designed to streamline and automate the process of managing vendors within an organization. This system provides a centralized platform for businesses to effectively handle vendor information, track performance, and facilitate communication. Key features include vendor onboarding, performance evaluation, document management, and a user-friendly dashboard for real-time insights. The Vendor Management System aims to enhance efficiency, transparency, and collaboration in the vendor management lifecycle, ultimately contributing to improved vendor relationships and organizational effectiveness.

### Prerequisites

- Django(version == 5.0.4)
- Django Restfreamework (version == 3.15.1)

## Getting Started

These instructions will help you set up and run the project on your local machine:
- Clone : git clone https://github.com/mehakaijaz/fatmug_design_assignment.git
- Activate virtual environment(new\scripts\activate)
- Install all the packages(pip install -r requirements.txt)
- Navigate inside the project(cd vms-master)
- Make migrations(python manage.py makemigrations)
- Migrate(python manage.py migrate)
- Create a superuser(python manage.py createsuperuser)
      Fill in the details on the terminal to create the superuser.
- Run the backend server (python manage.py runserver)
  
##APIs Endpoints
- /api/vendors/ : create and list vendors
- api/ vendors/<int:pk>/ : retrieve,update and delete vendors
- api/ purchase_orders/  : create and list purchaseorders
- api/ purchase_orders/<int:pk>/ : retrieve,update and delete purchaseorders
- api/ historical_performance/ : create and list historical performance
- api/ historical_performance/<int:pk>/ : retrieve,update and delete historical performance
- api/ purchase_orders/<int:pk>/acknowledge/ : purchase order acknowledgement

