## Overview
This project provides APIs for managing tenants, users, stores, products, and sales.

## Installation
To get started, follow these steps:


1. Clone the repository:
    ```
    git clone  https://github.com/rajat1515/e_com.git
    ```

2. Build the Docker containers:
    ```
    docker-compose build
    ```


### Tenant Setup
1. Create a public tenant/vendor:
    ```bash
    # Run the Django management command to create the public tenant
    docker-compose run -it e-commerce-backend python manage.py create_tenant
    ```

Schema name: public 
Domian name: public (rest can be any values )


The public vendor is only used to create tenants.

### Create super user
    ```bash
    # Run the Django management command to create the public tenant
    docker-compose run -it e-commerce-backend python manage.py create_superuser
    ```


### Start django server
    ```bash
    # Run the Django management command to start server
    docker-compose compose up 
    ```

Now, using tools like Postman or Swagger UI, you can create a specific tenant.

Access Swagger UI via:
http://localhost:8000/api/schema/swagger-ui

Endpoint for vendor creation:
/vendor

### Create Tenant-Specific Admin User (for initial Admin only)

```
    http://(schema).localhost:8000/admin/store/vendoruser/add/

    # Select user and the role 
```

Now all the APIs can be tested on (schema_name).localhost:8000.

To access APIs:

1) Obtain an access token from the /api/token/ endpoint for the user.
2) Copy the access token into the Authorization input box.

Note Admin user will be able to access only administrator APIs

