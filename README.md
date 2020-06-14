# Programming Internte of Things - Assignment 3
## Car Share System

### Introduction
This software represents the culmination of mutliple assignements that have resulted in a platform that enables a company to install raspberry pi devices with cameras in vehicles, and use these to manage the vehicles as a fleet of rental-style cars. 
It achevieves this by presenting a website where different users can perform a number of functions including registering, booking, cancelling bookings, and other administrative tasks related to the operations of the company. 
A cloud database containing all information is accessed using an API that employes paramaterized SQL queries, the API of which is accessed by both the Master Pi in responding to Agent Pi requests, and the website itself. 

### Instructions
The implemenation of the specification has resulted in four primary programs all of which can be operated on independent hardware depending on the desired configuration. In consideration of the Master Pi, this means that the socket response functionality, the database API, and the website can be deployed on physically separate hardware, spreading processing loads and affording a level of redundancy in the platform.

There are few arguments that need to be parsed for deployment, rather the necessary parameters are stored in files. See the documentation for details on how to modify select parameters for deployment. As such deployment is achieved by executing the following files with appropriate dependencies installed using Python 3.5.3 or later.
Deploy Agent Pi: python3 agentpi.py
Deploy Master Pi Socket: python3 socketresponder.py
Execute the following commands in the appropriate directories.
Deploy Website: flask run --host IP_ADDRESS
Deploy API: flask run --host IP_ADDRESS --port PORT

### Default User Credentials
These credentials are only valid as long as the seed data is employed.
Beyond this there is no guarantee that these credentials remain valid,
as they can be changed by authorised users.

User Type | Username | Password
--------- | -------- | --------
Admin | admin | adminpass
Manager | manager | managerpass
Engineer | engineer | engineer


### Github Usage
![Image of Github Commit History](https://github.com/Waaaghtech/Iot-Carshare/github.png)

### Trello Usage
![Image of Trello Board](https://github.com/Waaaghtech/Iot-Carshare/trello.png)

### File Structure
This project is divided into three primary direcctories with subdirectories as appropriate.

AgentPi - contains the code for operating the Agent and the files associated with the socket connection.

MasterPi - contains two subfolders: carapi that contains the files associated with the API that affords access to the database; website that contains the files associated with 

docs - contains the sphinx files associated with generating the published documentation

The documentation contains full details of each directory, subdirectory, and file.