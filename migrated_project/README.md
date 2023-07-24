# Migrated project
Here is how I adapted [initial project](../initial_project/README.md) to fit in a **google cloud run** architecture.

## Start project in local
* Setup a google cloud bucket, manage authenrication and copy [media/photofunky_Rln9w8K.gif](photofunky_Rln9w8K.gif)
* `cp .env.sample .env`
* Populate env variables from corresponding cloud
* `docker compose up`

## Step 1: Dockerize
Following file have been added:
* [Dockerfile](Dockerfile)
* [docker-compose.yaml](docker-compose.yaml) (convenient for developpement purposes)
* [.dockerignore](.dockerignore)

## Step 2: Save media in google cloud storage
The idea here is to use a google cloud storage bucket to store media files such as pictures. More on [how to setup google storage here](../doc/setup_cloud_bucket.md).

## Step 3: Update project
Here what I updated in initial project.

### Install librairies:
* [django-storages[google]](https://django-storages.readthedocs.io/en/latest/backends/gcloud.html) allows to have cloud storages
* [google-auth](https://github.com/googleapis/google-auth-library-python) allows to authenticate to google cloud

### Setup media storage
```py
# settings.py

...
# Storage
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_BUCKET_NAME = env("DJANGO_GS_BUCKET_NAME")
GS_PROJECT_ID = env("DJANGO_GS_PROJECT_ID")
GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
    json.loads(env("DJANGO_GS_CREDENTIALS"))
)
...
```

### Serve statics
Statics could be hosted in cloud as well, but to keep it simple, I use [whitenoise](https://whitenoise.readthedocs.io/en/latest/) which allows static serving from the container.

```py
# settings.py

...
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",         #<===ADD
    "django.contrib.sessions.middleware.SessionMiddleware",
...
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
...
```

### Update ALLOWED_HOSTS
Here the idea is to let allowed hosts to change according to environnements.
```py
# settings.py

...
ALLOWED_HOSTS = [env("DJANGO_ALLOWED_HOSTS")]
...
```

## Step 4: build image and push to repo
The project is ready to be deployed. A google cloud image repository is required for this step.
```bash
docker build -t <REPO-URL>/migrate-django-to-cloud-run .
docker push <REPO-URL>/migrate-django-to-cloud-run
```

## Deploy to google cloud run
In google cloud console: **Cloud Run > Create Service**
Then select pushed image.
In **Container, Networking, Security**:
* **Container port** has to patch [Dockerfile's](Dockerfile) exposed one. (8000)
* Adjust Memory, CPU ...

In **Environment variable** the following variables have to be populated:
* DJANGO_ALLOWED_HOSTS: this on will be assigned after the first deploy to have host
* DJANGO_SECRET_KEY
* DJANGO_GS_BUCKET_NAME
* DJANGO_GS_PROJECT_ID
* DJANGO_GS_CREDENTIALS

*Some of them would be defined as secrets in a real project.*

Once all these steps are performed, the site should be up and running as [https://migrate-django-to-cloud-run-xwcykomr3a-od.a.run.app](https://migrate-django-to-cloud-run-xwcykomr3a-od.a.run.app)
