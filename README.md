## Flask Base

This ia a flask + flask-restx example with
```shell script
Flask-Bcrypt
Flask-JWT-Extended
Flask-Migrate
Flask-SQLAlchemy
loguru
marshmallow
```

## Usage

### Run program

production
```shell script
gunicorn -c config/gunicorn.py "backend_server:create_app()"
```

visit
```shell script
http://127.0.0.1:8000/s/token/
```