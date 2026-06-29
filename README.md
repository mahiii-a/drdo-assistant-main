# DRDO Intelligent Document Assistant

## Overview

DRDO Intelligent Document Assistant is a full-stack web application that enables document management and query handling through a role-based system.

The application supports:

* User Registration and Login
* Role-Based Access Control (Admin/User)
* Document Upload and Management
* Query Submission and History Tracking
* Dashboard Analytics
* Recent Activity Monitoring

## Tech Stack

### Frontend

* React.js
* Vite
* Tailwind CSS
* Axios

### Backend

* Node.js
* Express.js
* PostgreSQL
* JWT Authentication
* Multer

## Database Setup

Create a PostgreSQL database and run:

database.sql

to create the required tables.

## Environment Variables

Create a file:

backend/.env

using the values from:

backend/.env.example

## Backend Setup

```bash
cd backend
npm install
npm start
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Features

### Admin

* Upload Documents
* View Documents
* Delete Documents
* Dashboard Statistics

### User

* Register Account
* Login
* Ask Queries
* View Query History
* Dashboard Analytics

