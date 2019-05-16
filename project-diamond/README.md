Project Diamond
===============
Project Diamond is the team project code name. Every week you will learn an area needed to complete the project.  It will run on the IST Linux server in your Team area. It will consist of five running python3 applications app1-app5.

**app1**: will use CURL to retrieve a JSON payload of data from the Internet, then it will use a network socket programming to send the payload securely using TLS security to the app2. It will also receive the AES encrypted payload from app4 via a message queue using RabbitMQ. It will also save the JSON payload to a text file on the Linux system.  All workflow actions pass or fail will be logged into the activity MongoDB NoSQL database with a timestamp. Unit tests will confirm all methods are functional.

**app2**: will receive the secure payload from app1 using TLS. It will then hash the JSON payload using HMAC and append it to the message and use secure SFTP to send the payload to app3. All workflow actions pass or fail will be logged into the activity MongoDB NoSQL database with an identifier and timestamp. Unit tests will confirm all methods are functional.

**app3**: will receive the secure SFTP payload from app2 using SFTP and verify the hash. It will email the payload using threading to an email address. It will then transform the JSON message into a python object and use Pyro ORB to send the python object to app4. It will also compress the JSON object. All workflow actions pass or fail will be logged into the activity MongoDB NoSQL database with a timestamp. Unit tests will confirm all methods are functional.

**app4**: will receive the Pyro python object and convert it back to JSON. Then it will use RabbitMQ message Queue to sent the message to app1. The calculated round trip time will be displayed on app1. All workflow actions pass or fail will be logged into the activity MongoDB NoSQL database with a timestamp. Unit tests will confirm all methods are functional.

**app5**: will receive all the log requests and put them into the MongoDB database. There should be method handlers for the pass and fail. Unit tests will confirm all methods are functional.

	- CURL: Allows you script web bots and robots to interact with the internet.
	- JSON: Javascript Object Notation used to package self-describing data payloads
	- Networking Sockets: Using the compter's network listening ports the client can connect to the server and perform a file transfer
	- SSL/TLS: Transport Layer Security 1.2 is the latest version which provides payload integrity and authentication
	- Hashing: Used to map data using a hashing algorithm into a smaller string used to validate the data 
	- Threading: the ability to execute multiple processes or threads concurrently
	- ORB: Object Request Broker passing objects between computer applications
	- Compression: the reduction of the payload size
	- Message Queue: Guaranteed delivery of the message payload to the destination 
	- AES Encryption: provides the protection of the message
	- MongoDB: BSON(similar to JSON) NoSQL type database
