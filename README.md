# Clothing Store Database Application

## Overview

This project is a simple database application for managing clothing store data. It uses a MySQL databaseand a Flask backend written in Python to retrieve and insert records. A basic frontend interface is included to display and interact with the data.

## Technologies

* Python (Flask)
* MySQL
* HTML / CSS / JavaScript

## Project Structure

Database-Project
│
├── backend
│   └── app.py
│
├── frontend
│   ├── index.html
│   ├── products.html
│   ├── customers.html
│   ├── orders.html
│   ├── style.css
│   └── app.js
│
├── schema.sql
├── data.sql
└── README.md

## Setup Instructions

### 1. Create the database

Run the following SQL files in MySQL:
schema.sql
data.sql

This will create the tables and insert sample data.

### 2. Install dependencies

Install the required Python packages:
pip install flask mysql-connector-python

### 3. Run the backend server

Navigate to the backend folder and start the Flask application: python app.py
The server will run at:
### http://127.0.0.1:5000/

## API Endpoints

Get all products
GET /products

Add a customer
POST /customers
