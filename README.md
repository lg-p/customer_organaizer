# Handbook

*It is a console application that stores, views, and edits customer data.*  

### Possible commands:
-  **insert** - insert a new customer into the store\
        *arguments*: customer_id, full_name, position, name of the organization, email, phone  
        
-  **find** - searches for a customer in the store by the given argument name and argument value\
        *arguments*: one of the customer arguments, argument value  
        
-  **update** - update a customer in the store\
        *arguments*: customer_id, full_name, position, name of the organization, email, phone  
        
-  **delete** - remove customer from the storage\
        *arguments*: customer_id
        
-  **list** - displays a list of customers sorted by the listed argument\
        *arguments*: any number of customer arguments separated by a space
        
### Storage options: 
*You can store data in an XML file, or in a database, or in internal memory.*
- To save data to an XML file when starting the application, you must specify the optional **--path** argument and the path to the file, separated by a space.
- To save data in the database when starting the application, you must specify the optional arguments **--db**, **--user**, **--password**, **--host**,
**--port** and their values separated by a space.
- No arguments are required to store data in internal memory.

## Using with Docker

*To run your application in a docker container, use a bash-script.*
- Specify the first parameter **DB** to store data in a database, or **XML** to store data in an XML file, 
or **InMemory** to store data in internal memory. 
- Specify the second parameter **clear** to remove docker containers after use or nothing to stop docker containers.

*example: `./startup.sh DB clear`*
