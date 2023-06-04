# reviews

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

## Commands

Run the dev server:

```bash
npm run dev
# OR
./dev
```

Watch for html changes with Tailwind:

```bash
npm run tailwind
# OR
./css
```

Run both the server and Tailwind:

```bash
npm start
```
