- [Backend setup](#backend-setup)
  * [Installation](#installation)
    + [Environment Variables](#environment-variables)
    + [Installing dependencies](#installing-dependencies)
    + [Setting up database](#setting-up-database)
    + [Running the server](#running-the-server)
  * [Environment variables](#environment-variables)
    + [Django](#django)
      - [Development](#development)
      - [Production](#production)
    + [Database](#database)
      - [Development](#development-1)
      - [Production](#production-1)
    + [Email backend](#email-backend)
      - [Development and Production](#development-and-production)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with
markdown-toc</a></i></small>

# Backend setup

## Installation

### Adding environment variables

Refer [this section](#environment-variables) of the README to add all the environment variables.

### Installing dependencies

Using a virtual environment is encouraged.

`pip install -r requirements.txt`

### Setting up database

```
python manage.py reset_db
python manage.py migrate
```

### Running the server

`python manage.py runserver`

## Environment variables

### Django

`RMP_SECRET_KEY`: The secret key used in Django projects. Read more about
it [here](https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-SECRET_KEY).

#### Development

In order to generate your own secret key, checkout [this](https://miniwebtool.com/django-secret-key-generator/).

#### Production

Be more careful with what secret key you use in production. Checkout [this](https://stackoverflow.com/q/41298963).

### Database

`RMP_DB_URL`: The URL to the database to be used.

#### Development

For quick development-setup, you can go with SQLite. The corresponding URL will be:
`sqlite:///PATH`. `PATH` is the path to the SQLite database file (which does not exist beforehand).

Example: `sqlite:////home/reeshabh/Desktop/mentoringplatform/backend/db.sqlite3`.

**Note**: In some rare cases, it might be required that the SQLite database needs to exist beforehand. In those cases,
create an empty file named `db.sqlite` at `PATH`.

#### Production

For production environments, avoid SQLite. URLs for other database servers can be
found [here](https://github.com/jacobian/dj-database-url).

### Email backend

`RMP_EMAIL_HOST`: The email service being used.

`RMP_EMAIL_HOST_USER`: The account name/username from which the emails are sent.

`RMP_EMAIL_HOST_PASSWORD`: The password/secret-key to authenticate the outgoing emails.

#### Development and Production

We suggest using SendGrid as the email backend.

`RMP_EMAIL_HOST`: `smtp.sendgrid.net`

`RMP_EMAIL_HOST_USER`: `apikey` (literally)

`RMP_EMAIL_HOST_PASSWORD`: Generate API key from Sendgrid using SMTP mode.
Refer [this](https://app.sendgrid.com/guide/integrate/langs/python) after making a Sendgrid account. However, feel free
to use any other service as your email-backend. Make sure you check out the offers available in
your [GitHub Student Developer Pack](https://education.github.com/pack).