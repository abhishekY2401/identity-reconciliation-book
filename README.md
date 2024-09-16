# identity-reconciliation-book
Identities and mutuals redefined

## Bitespeed Backend Task: Identity Reconciliation

### Project Description

This project implements an Identity Reconciliation service that unifies user contact data (email and phone numbers) based on provided input. It manages contacts with both primary and secondary precedence, ensuring that any new or existing data linked to the same person is appropriately consolidated. It follows these key steps:

1. If no contact exists, a new primary contact is created.
2. If a match is found for either the phone number or email, the matching contacts are linked together under a single primary contact.
3. It merges contacts by demoting newer primary contacts into secondary contacts when required, ensuring a unified representation of a user across different contact details.

Prerequisites
Before you begin, ensure you have the following installed:

- Python 3.9+
- PostgreSQL
- Git
- SQLAlchemy
- Alembic (not necessary to install, it is already installed in virtual environment)

### Installation

1. Clone the Repository

```
git clone https://github.com/your-repo/identity-reconciliation.git
cd identity-reconciliation
```

2. Set up a Virtual Environment

```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Dependencies

```
pip install -r requirements.txt
```

4. Set up PostgreSQL Database

- Make sure PostgreSQL is installed and running
- Create a new PostgreSQL database and user

```

CREATE DATABASE identity_reconciliation;
CREATE USER your_username WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE identity_reconciliation TO your_username;

```

5. Database Migrations

Run migrations to set up the database schema:

```
flask db init
flask db migrate -m "Add contact table"
flask db upgrade
```

6. Configuration

```
DATABASE_URI=postgresql://your_username:your_password@localhost/identity_reconciliation
PORT=PORT_NUMBER
```

### Endpoints

1. Reconcile Contact Information
POST /identify

This endpoint accepts a JSON payload containing a phone number and/or email, and reconciles the identity information accordingly.

Request Body:

```
{
  "email": "example@domain.com",
  "phoneNumber": "+1234567890"
}
```

Response:
```
{
  "contact": {
    "primaryContactId": 1,
    "emails": ["example@domain.com", "alternate@domain.com"],
    "phoneNumbers": ["+1234567890", "+0987654321"],
    "secondaryContactIds": [2, 3]
  }
}
```


### Troubleshooting

Common Issues:

1. Database Connection Errors

- Ensure PostgreSQL is running and the connection string in the ```.env``` file is correct.
- Double-check the database username, password, and database name.

2. Missing or Invalid .env Configuration

- Make sure the ```.env``` file exists and is correctly set up in the root of the project.
- Ensure ```DATABASE_URI``` follows the correct format for your PostgreSQL connection.

3. Flask Application Fails to Start

- Ensure you have activated your virtual environment (```source venv/bin/activate```).
- Verify all dependencies are installed via ```pip install -r requirements.txt```

4. Migrations Not Applied

- Run ```flask db upgrade``` to apply migrations if your database schema is out of date.