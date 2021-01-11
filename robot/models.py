import os

from django.db import models

from robot import FILES_DIR


class ChromeProfile(models.Model):
    name = models.CharField(max_length=45, unique=True)
    path = models.TextField()


class CSVCollection(models.Model):
    name = models.CharField(max_length=45, unique=True)
    filename = models.CharField(max_length=45)
    path = models.CharField(max_length=45)