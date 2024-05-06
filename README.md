# VendorManagementSystem
Vendor Management System


# Steps to run project.

1. Clone the repository and move to project folder. Make sure python is installed in your system. by running command ```*python --version*```

2. Install the requirements by running command ```*pip install -r requirements.txt*```

3. Make migrations and migrate the changes by running command ```*python manage.py makemigrations*``` & ```*python manage.py migrate*```

4. Create a admin user by running command ```*python manage.py createsuperuser*``` . Provide requested details.

5. Now run the project by running command ```*python manage.py runserver*```


# Steps to run/test the apis

1. Install '__Thunder Client__' extension in VS Code.
   
   <img width="820" alt="Screenshot 2024-05-06 at 3 10 16 PM" src="https://github.com/Kolwankar-Siddhiraj/VendorManagementSystem/assets/88200767/3b686f6d-f202-4598-87d1-229c9d3452ca">


2. Import the provided api collection in repository.

   <img width="295" alt="Screenshot 2024-05-06 at 3 12 00 PM" src="https://github.com/Kolwankar-Siddhiraj/VendorManagementSystem/assets/88200767/c7432520-da67-4125-be60-3b287924d943">


3. Setup environment for the project.

   <img width="1375" alt="Screenshot 2024-05-06 at 3 16 34 PM" src="https://github.com/Kolwankar-Siddhiraj/VendorManagementSystem/assets/88200767/33ba6c1f-7e96-4a1f-80e3-fe01888ab4f8">


4. Run any request from the collection.

Note : To run any api except Admin Login api we need auth token. To obtain auth token run Admin Login api and pass your admin credentials. Next copy the access token from the response and paste it in 'auth' key of Thunder client environment as shown in 3rd step. 

   <img width="1440" alt="Screenshot 2024-05-06 at 3 18 46 PM" src="https://github.com/Kolwankar-Siddhiraj/VendorManagementSystem/assets/88200767/26a1e60b-c1f9-4e46-a2e2-cb6f390d531e">



5. Pass necessary information in the request body (json) where needed.





# API documentation.

0. **Admin Login => POST:** */api/admin/login/*
   - **Description:** This endpoint is for admin to login.
   - **Data:** JSON object with the following fields:
     - username (string): Admin's username.
     - password (string): Admin's password.


1. **Create New Vendor => POST:** */api/vendors/*
   - **Description:** This endpoint creates a new vendor profile.
   - **Data:** JSON object with the following fields:
     - vendor_code (string): A unique identifier for the vendor.
     - name (string): Vendor's name.
     - contact_details (string): Contact information of the vendor.
     - address (string): Physical address of the vendor.


2. **List All Vendors => GET:** */api/vendors/*
   - **Description:** Retrieves a list of all vendors.


3. **Get Specific Vendor => GET:** */api/vendor/{vendor_id}/*
   - **Description:** Retrieves details of a specific vendor.
   - **Data:** Path parameter {vendor_id} specifying the ID of the vendor.


4. **Update Specific Vendor => PUT:** */api/vendor/{vendor_id}/*
   - **Description:** Updates details of a specific vendor.
   - **Data:** Path parameter {vendor_id} specifying the ID of the vendor.
     JSON object with the fields to be updated:
     - name (string): Vendor's name.
     - contact_details (string): Contact information of the vendor.
     - address (string): Physical address of the vendor.


5. **Delete Specific Vendor => DELETE:** */api/vendor/{vendor_id}/*
   - **Description:** Deletes a specific vendor.
   - **Data:** Path parameter {vendor_id} specifying the ID of the vendor.


6. **Create Purchase Order => POST:** */api/purchase_orders/*
   - **Description:** Creates a new purchase order.
   - **Data:** JSON object with the following fields:
     - vendor (integer): ID of the vendor associated with the PO.
     - delivery_date (string, format: YYYY-MM-DDTHH:MM:SS): Expected or actual delivery date of the order.
     - items (array of objects): Details of items ordered.
     - quantity (integer): Total quantity of items in the PO.


7. **List All Purchase Orders of Vendor => GET:** */api/purchase_orders/?vendor_id={vendor_id}*
   - **Description:** Retrieves a list of all purchase orders with an option to filter by vendor.
   - **Data:** Required query parameter:
     - vendor_id (integer): ID of the vendor to filter purchase orders.


8. **Get Specific Purchase Order => GET:** */api/purchase_orders/{po_id}/*
   - **Description:** Retrieves details of a specific purchase order.
   - **Data:** Path parameter {po_id} specifying the ID of the purchase order.


9. **Update Specific Purchase Order => PUT:** */api/purchase_orders/{po_id}/*
   - **Description:** Updates details of a specific purchase order.
   - **Data:** Path parameter {po_id} specifying the ID of the purchase order.
     JSON object with the fields to be updated:
     - status (string): Current status of the PO (completed, canceled).
     - quality_rating (float, optional): Rating given to the vendor for this PO.


10. **Delete Specific Purchase Order => DELETE:** */api/purchase_orders/{po_id}/*
    - **Description:** Deletes a specific purchase order.
    - **Data:** Path parameter {po_id} specifying the ID of the purchase order.


11. **Get Performance Metrics of Vendor => GET:** */api/vendors/{vendor_id}/performance/*
    - **Description:** Retrieves the calculated performance metrics for a specific vendor.
    - **Data:** Path parameter {vendor_id} specifying the ID of the vendor.


12. **Acknowledge Purchase Order => POST:** */api/purchase_orders/{po_id}/acknowledge/*
    - **Description:** Updates acknowledgment_date for a specific purchase order and triggers recalculation of average_response_time.
    - **Data:** Path parameter {po_id} specifying the ID of the purchase order.







