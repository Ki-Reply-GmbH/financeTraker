This is a test update for a test PR that TIMO asked for
Please remove these 2 lines once teting is done

# Finance Tracking App

Welcome to the Finance Tracking App, your go-to solution for managing and monitoring your daily expenses with ease. This application is designed to help users gain better control over their financial health by tracking expenditures and categorizing them into various budget sections. Whether you're looking to keep a closer eye on your groceries, utilities, or leisure activities, our app makes it simple and intuitive.

## Docker Compose Setup

Before running the application with Docker Compose, you need to set up your environment variables:

1. Copy the `.env.example` file to `.env`:

   ```bash
   cp .env.example .env
   ```

2. Open the .env file and fill in the values for POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB.

3. Run the application using Docker Compose:

   ```bash
   cdocker-compose up
   ```

   The system should be up and running at http://localhost:8000

## Local development setup

Once you copied the repository,

1. Copy the `.env.example` file to `.env`:

   ```bash
   cp .env.example .env
   ```

2. Open the .env file and fill in the values for POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB.
3. fill in the value for DATABASE_URL as

   ```bash
   DATABASE_URL=postgresql://POSTGRES_USER:POSTGRES_PASSWORD@localhost:5432/POSTGRES_DB
   ```

4. open up terminal in the root directory and run these comands

```bash
docker-compose up db
```

This should start the DB container, Now open up another terminal and run this command

```bash

uvicorn app.main:app --reload
```

You should see in your termanal that the app has started.
