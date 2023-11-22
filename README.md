# Dormitory Reservation System

## Overview

The Dormitory Reservation System is a web application built using Django for managing reservations of dormitory rooms. It allows users to browse available rooms, make reservations, and view their reservation history.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/astelmachfilipczak/dormitory.git

2. Navigate to the project directory:

    ```bash
    cd dormitory
   
3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
   
4. Apply database migrations:

    ```bash
   python manage.py migrate
   

5. Create a superuser to access the Django admin site:

    ```bash
   python manage.py createsuperuser
   

6. Start the development server:

    ```bash
   python manage.py runserver

7. Access the application at http://localhost:8000


   
### Database Setup (PostgreSQL)
1. Install PostgreSQL:

Follow the official documentation to install PostgreSQL on your PC.

2. Configure the Database:

    ```bash
    psql -U postgres

    CREATE DATABASE dorm_db;
    CREATE USER postgres WITH PASSWORD 'password';
    ALTER ROLE postgres SET client_encoding TO 'utf8';
    ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
    ALTER ROLE postgres SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE dorm_db TO dorm_user;

    \q
   
3. Continue with the remaining steps for Django setup.
   
## Usage
Visit the homepage to explore the rooms of a fictional dormitory network.
Navigate to the 'All Rooms' page or append '/rooms' to the end of URL to see all available rooms.
Hover over a room to view details and click 'Click here to book' to make a reservation.
Log in or register to browse your reservations on the 'Reservation' page.
Use the search feature to find rooms based on various criteria.

## Features
Random selection of rooms on the home page.
Room search functionality.
User registration and authentication.
Reservation management (create, view open/closed reservations).
Availability checking for room reservations.
Detailed room information, including number of beds, bathroom type, etc.

## Contributing
Contributions to the Dormitory Reservation System are welcome! Whether you're fixing a bug, implementing a new feature, or improving documentation, I really appreciate your help.

To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m 'Description of your changes'`.
4. Push to your branch: `git push origin feature-name`.
5. Open a pull request with a clear title and description.

Please adhere to coding standards and make sure your code is well-documented. 

Thank you for contributing to the Dormitory Reservation System!

## License
This project is open-source and is distributed under the terms of the MIT License.

## Credits

This project utilizes a frontend template named "EstateAgency" provided by BootstrapMade.com. The template was last updated on Jul 27, 2023, using Bootstrap v5.3.1. You can find the original template [here](https://bootstrapmade.com/real-estate-agency-bootstrap-template/).

- **Template Name:** EstateAgency
- **Updated:** Jul 27, 2023, with Bootstrap v5.3.1
- **Template URL:** [EstateAgency Template](https://bootstrapmade.com/real-estate-agency-bootstrap-template/)
- **Author:** BootstrapMade.com
- **License:** [Template License](https://bootstrapmade.com/license/)

I would like to express my gratitude to BootstrapMade.com for providing this template, which served as a foundation for the frontend design of this Dormitory Reservation System.
