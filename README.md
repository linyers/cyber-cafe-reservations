# Cyber Café Reservations

## Description

This project is a device reservation system for a cyber café. It allows customers to book computers and videogame consoles. The system facilitates managing the availability of devices and enhances the customer experience.

## Features

- **User Registration and Authentication:** Users can register and authenticate to make reservations.
- **Device Reservation:** Users can view the availability of devices and make reservations.
- **Reservation History:** Users can view their reservation history and cancel reservations if needed.
- **Availability Management:** Administrators can manage the availability and maintenance of devices.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/linyers/cyber-cafe-reservations.git
   ```
2. Navigate to the project directory:
   ```bash
   cd cyber-cafe-reservations
   ```
3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser to access the admin interface:
   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Open your browser and navigate to `http://localhost:8000` to use the application.
2. Access the admin interface at `http://localhost:8000/admin` to manage the application.

## Future Features

- **Email Notifications for Reservations:** Enhance the notification system to send detailed email notifications for new reservations, cancellations, and reminders.
- **Integration with MercadoPago:** Add payment integration with MercadoPago to allow users to pay for their reservations online.
