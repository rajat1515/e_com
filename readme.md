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
    docker-compose run -it hr-automation-backend python manage.py create_tenant
    ```

Schema name: public 
Domian name: public (rest can be any values )


The public vendor is only used to create tenants.

Now, using Postman or Swagger UI, you can create a specific tenant

http://localhost:8000/api/schema/swagger-ui

Endpoint / vendor 


now all the apis can be tested on (schema_name).localhost:8000


