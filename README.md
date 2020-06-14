# Programming Internte of Things - Assignment 3
## Car Share System


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