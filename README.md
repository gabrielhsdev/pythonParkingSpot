# About the Project

## The Problem

Managing parking spots in a busy shopping mall can be challenging. With hundreds of cars coming and going daily, issues like inefficient space usage, long waiting times for parking, and difficulties in tracking parked vehicles arise. Additionally, manual systems are prone to errors and delays, leading to customer dissatisfaction and operational inefficiencies.

## The Solution

This system is designed to streamline parking spot management in shopping malls. It provides an automated way to track parked cars, manage available spots, and record vehicle entry and exit times. By simplifying these processes, the system aims to reduce congestion, enhance user experience, and improve operational efficiency.

## Our Approach

We have built a Python-based application structured on the MVC (Model-View-Controller) design pattern to ensure clean separation of concerns and scalability. The system includes the following features:

- Dynamic Parking Spot Tracking: Real-time updates on available parking spots and occupied spaces.

- Vehicle History Management: Track entry and exit times for every car, providing a comprehensive log of parking activity.

- Docker Integration: The application is containerized for seamless deployment and consistent performance across environments.

- Extensible Architecture: Services and models are designed to be modular, making the system easy to maintain and expand.

By leveraging Python, Flask, and Docker, this project demonstrates an efficient and modern solution to parking management challenges in high-traffic shopping malls.

# Setup Instructions

### Clone the Repository First, clone the repository to your local machine:
```
git clone https://github.com/gabrielhsdev/pythonParkingSpot
````

### Build and Start the Containers In the project directory 
```
docker-compose up --build
```

This will build the Docker images for both the app and MySQL. Also, it creates the MySQL tables needed to run the project


Start the containers for both services.

Access the Application Once the containers are up and running, you can access the Flask application using postman files on the repo.
```
V1.postman_collection.json
```
This URL exposes an example endpoint from the application.

### Connect to MySQL To connect to MySQL from MySQL Workbench or any MySQL client
```
Host: 127.0.0.1
Port: 3306
Username: root
Password: root
Database: main
````