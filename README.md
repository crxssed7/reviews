# reviews

## What is this?

This is a simple Flask webapp that interfaces with the AniList api and retrieves a users manga list. It also displays any reviews made by the user.

## How do I use this?

First you need to create two custom lists on AniList: Collecting and Favourites. They're pretty self explanitory. You then need to follow the below steps, making sure to put your USER_ID in the `.env` file.

## Setup

Install Redis (used for caching):

```bash
sudo pacman -S redis
```

Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies with pipenv:

```bash
pipenv install
```

Install node packages:

```bash
npm install
```

Rename `.env.example` and fill in your details:

```bash
mv .env.example .env
vim .env
```

## Commands

Run the dev server:

```bash
npm run dev
```

Watch for html changes with Tailwind:

```bash
npm run css
```

Run both the server and Tailwind:

```bash
npm start
```

When deploying, you have to rebuild the for any new css changes:

```bash
npm run build:css
```
