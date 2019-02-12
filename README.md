# IFridge API

**Awesome IFridge Web APIs.**


IFridge API is the IFridge API – a beautiful design of the IFridge REST API. IFridge is built for tracking and managing all of your foods in your fridge.

It’s built with Python – django rest api server and many other marvellous libraries on the back-end.

---

## Getting Started

Requirements
[Python](https://www.python.org/)
[Django](https://www.djangoproject.com/)
[django-rest-framework](https://www.django-rest-framework.org/)

## Installation

Clone Project

``` 
git clone https://github.com/ai-fridge/IFridge-api.git
cd IFridge-api 
```

Install Python Package

``` $ pip install -r requirements.txt ```


## Usage

Migrate:
``` $ python3 manage.py migrate ```

Starting a new Feature:
``` $ django-admin startapp `your feature name` ```

Running Server:
``` $ python3 manage.py runserver ```

---

#### Register a Route

##### Prefix Api Route
Which is the mainly route under the API.

```
    url(r'^api/', include('face_recog.urls')),
```

##### Feature Route
Adding a api route for your feature.

```
from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^face/recognition',
        views.verify_face_recognition,
        name='verify_face_recognition'
    ),
]
```


## Coding Style
Please follow these coding standards when writing code for inclusion in IFridge.

##### Python style

- Making sure you follow  **PEP 8**.

Use isort to automate import sorting using the guidelines below.

Quick start:
$ pip install isort
$ isort -rc .

If you're using PyCharm, it will automatically hint the coding style for you.

### Todo

- [x] Face Recognition
- [x] V1 Project Structure
- [ ] Testing
- [ ] Object Detection
- [ ] Docker
- [ ] Database