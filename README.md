### simple rating system with Django

#### Prerequisite

You will need an installed version of `python3` and to manage the dependencies, you need to install `virtualenv`

```bash
python -m pip install virtualenv
```



developed and tested with `python` version `3.9.7`

#### Initializing

cloning a copy of the distro and installing dependencies:

```bash
git clone https://github.com/maghorbani/quotes-rating
cd quotes-rating
python -m venv env

source env/bin/activate
pip install -r req.txt

```

and you should have a `.env` file (There is an example .env file)

```bash
cp .env.example .env
```

consider adding a `SECRET_KEY`

**note**: if you set the `DEBUG` to `False`, you will need to set `ALLOWED_HOSTS` (comma seprated) :

```bash
ALLOWED_HOSTS=127.0.0.1,example.com
```

and changing directory to the main Django dir

```bash
cd quotesrating
```

once the packages installed successfully, you can run tests:

```bash
./manage.py test
```

or running the server, note that before running the server, you need to migrate the database

*note:* the migrations are committed and the first command is not required

```bash
./manage.py makemigrations
./manage.py migrate
./manage.py runserver
```

can also create a superuser:

```bash
./manage.py createsuperuser
```

#### Technical Note

The average of scores for a quote is calculated using `Moving Average` method. because the number of ratings is considered a massive number, averaging each time in view will be a bottleneck, but using moving average the problem will be solved.

**Future development note:** The moving average calculations is done in the `/api/quotes/{qoute-id}/rate/`API View, so adding ratings withing python Django shell will not update the average score. so this calculations should be done in another level (not API View) maybe a level closer to Models or maybe using `postres` `AVG` function would be a better solution

#### Docs

The rout documentation is available in `/swagger` or `/redoc` routes

#### Authentication

A user after registering with the route `/api/auth/register` can retrieve a token from `/api/auth/login` and a token object like follow will be returned:

```json
{
	"access" : "access-token",
	"refresh" : "refresh-token"
}
```

  The note here is you should use the `access` token in the header of your requests with a `JWT`, `Bearer`, or `Token` (Eachone is valid) prefix like:

```bash
curl \
  -H "Authorization: Token the-access-token" \
  http://localhost:8000/the-route/
```

