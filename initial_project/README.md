# Initial project

This simple project aims at being used as a **starting point** to see how could be **adapted** a django project **to cloud run**.

## Scenario
* A **media** directory stores a picture sample.
* Statics have been collected in a **static** directory.
* To go simple, a sqlite **database** is present and migrated.

## To run it:
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn config.wsgi
```

## Check
* [http://127.0.0.1:8000](http://127.0.0.1:8000) serves a view with an image.
* [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) serves admin interface, statics should be ok.