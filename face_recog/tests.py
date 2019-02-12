import json

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

# initialize the APIClient app
client = Client()
