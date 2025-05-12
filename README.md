# Simple French Micro-Entrepreneur Accounting System

This project is a personal development initiative to build a simple accounting system tailored to the needs of a French micro-entrepreneur. It focuses on generating compliant monthly reports and invoices, and storing them securely in the cloud.

## Objectives

Automatically generate monthly accounting reports in PDF format

Generate professional, compliant invoices directly from the app

Securely store reports in the company's cloud

Facilitate manual declaration of chiffre d’affaires on the URSSAF portal



---

## Compliance with French Accounting Rules

### 1. Livre des recettes (Income Logbook)

A chronological and unalterable record of all income is required. This project will:

Record all revenue with required details

Include these records in a monthly PDF report


Mandatory data:

- Date of income

- Client name

- Nature of sale or service

- Amount received (with payment method: cash, cheque, transfer)

- Invoice number (if applicable)


### 2. Facturation (Invoicing)

The system will generate invoices that comply with French regulations.

Each invoice must include:

Your numéro SIRET

Invoice date

Sequential invoice number

Client name

Description of the product or service

Amount (HT - hors taxe)

Mandatory note:
"TVA non applicable, article 293 B du CGI" (if not subject to VAT)


### Livre des achats (Expense Logbook)

Although not required for most micro-entrepreneurs, especially those offering services, keeping track of expenses can be beneficial for personal analysis or in case of future transition to a different business status (e.g., régime réel).

What it is:
A chronological record of all professional expenses related to your activity.

Optional fields to track:

Date of expense

Supplier name

Nature of the expense

Amount (including VAT, even if not recoverable)

Payment method

Invoice or receipt number (if available)


Why include it?

Helps monitor profitability

Useful for tax-related discussions or status changes

Provides a more complete picture of business health

### 3. Conservation des documents

The system will store monthly PDF reports and invoices in the cloud, organized by year and month, to comply with the legal obligation of document retention for 10 years.

### Run once to generate django structure

docker compose run web django-admin startproject accounting .
docker-compose run web python manage.py startapp expenses


### Reminders for building images from scratch

# Stop containers and remove volumes (this clears the Postgres data too)
docker compose down -v

# Rebuild images to ensure latest code and settings are used
docker compose build --no-cache

# Start again
docker compose up --build

### Run to migrate from default sqlitedb to postgres db

docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migratepython manage.py migrate

### Create django superuser

docker compose exec web python manage.py createsuperuser

### Check if django is using postgres DB

 docker compose exec web python manage.py shell
 from django.db import connection
 print(connection.settings_dict['ENGINE'])

 ### Access the db by hand 

 docker compose exec db psql -U your_user -d your_database

