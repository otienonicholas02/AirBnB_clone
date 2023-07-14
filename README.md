0x00. AirBnB clone - The console

Project Description
This marks the initial phase in constructing your inaugural web application, the AirBnB clone. The project's objective is to deploy a replica of the Airbnb website utilizing your own server. The ultimate version of this project will encompass the following features:

A command-line interpreter designed to manipulate data without a graphical interface, similar to a shell, serving the purpose of development and debugging.
A web-based interface that combines both static and dynamic functionalities, forming the front-end of the website.
An extensive database system responsible for overseeing the backend operations and functionalities.
An Application Programming Interface (API) that establishes a communication interface bridging the front-end and back-end components of the system.

The project's goals and objectives are as follows:
Generating a fresh instance of an object, such as creating a new "User" or a new "Place".
Fetching an object from a file storage, database, or any other relevant data source
Executing operations on objects, such as counting, computing statistics, and other related actions.
Modifying the attributes of an object by updating their values.
Destroy an object


The objects that have been created.
BaseModel
User
City
Amenity
State
Review
Place

How to start it
Clone this repository:https://github.com/otienonicholas02/AirBnB_clone.git
Access AirBnb directory: cd AirBnB_clone
Run hbnb(interactively): ./console and then press enter command
Run hbnb(non-interactively): echo "<command>" | ./console.py

$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
(hbnb) 
(hbnb) quit
$
But also in non-interactive mode: (like the Shell project in C)

$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb)
$


Testing
Unittests for the project are defined in the tests folder. To run the entire test suite simultaneously, execute the following command:
$ python3 unittest -m discover tests


AUTHORS
Nicholas Otieno<otienonicholas02@gmail.com>
Jezereal Gilbert<jezerealgilbert@gmail.com>

