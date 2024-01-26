from django.db import models
from dataclasses import dataclass


class BaseModel(models.Model):
    """The base and model"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True