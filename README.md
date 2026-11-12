# Chat We App

**Chat We App** is an early web-development project built with **Python, Django, Django Channels, WebSockets, HTML, CSS, and JavaScript**. I created it while learning to build interactive web applications and real-time communication features.

This project uses Django's traditional application structure, server-rendered templates, and browser-side JavaScript. It is **not presented as a REST API or Django REST Framework project**.

> **Project status:** An early learning and portfolio project. The code may require configuration or updates to run in a new environment; it should not be assumed production-ready.
# What the project demonstrates

- **Django backend:** application structure, views, routing, models, and migrations.
- **User accounts:** custom user and profile models, authentication-related views and templates, and email verification/password-reset flows.
- **Messaging:** chat models and views, conversation previews, and support for image fields in the chat data model.
- **Real-time communication:** Django Channels consumers and WebSocket routing.
- **External service exploration:** a Twilio integration module for messaging-related functionality.

## What I worked on

- Organizing a Django project into account-related and chat-related applications.
- Building browser interfaces with HTML templates and JavaScript.
- Exploring real-time chat communication with Django Channels and WebSockets.
- Working with Django models, views, URL routing, forms, and migrations.
- Building account and profile-related pages.

The repository includes code for additional account and chat functionality. The presence of a file or model does not necessarily mean every feature is fully implemented or tested.

## Technologies

| Area | Technology |
| --- | --- |
| Backend | Python, Django |
| Real-time communication | Django Channels, WebSockets, ASGI |
| Frontend | HTML, CSS, JavaScript, Django templates |
| Data handling | Django models and migrations |

## Repository structure

```text
chat-we-app/
├── accounts/          # Account-related Django app
├── chatapp/           # Django project configuration and ASGI entry point
├── chatapp2/          # Chat-related Django app and WebSocket consumers
├── templates/         # HTML templates for accounts and chat pages
├── manage.py          # Django management commands
├── requirements.txt   # Python dependencies
└── .gitignore
```

## Running the project locally

These are the *general* steps for a Django project. The precise configuration and any additional services needed for real-time messaging depend on `chatapp/settings.py` and the project dependencies.

```powershell
git clone https://github.com/phollarh/chat-we-app.git
cd chat-we-app

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Before starting, review the Django settings for required environment variables, database settings, and the configured Django Channels layer. Do **not** put real secrets or credentials into source control.

## Development background

This is one of my earlier projects, created while learning how to build web applications with Django and JavaScript. I later worked on more extensive business applications, including a [React and Django POS system](https://github.com/phollarh/react-drf-pos).

The project was uploaded to GitHub after its initial development, so the first public Git commit does not necessarily represent the date I started writing the application.

## Security and limitations

- This repository is shared for learning and portfolio purposes.
- It has not been independently security-audited.
- Never publish active credentials, `.env` files, customer or chat data, or local databases.
- Some features may need further testing or configuration before they work outside the original development environment.

## Author

GitHub: [@phollarh](https://github.com/phollarh)
