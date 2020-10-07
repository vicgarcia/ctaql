import uuid
from django.db import models

class Route(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=250)

class Pattern(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    route = models.ForeignKey(Route, related_name="patterns", on_delete=models.CASCADE)
    number = models.CharField(max_length=6)
    direction = models.CharField(max_length=30)

class Stop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pattern = models.ForeignKey(Pattern, related_name="stops", on_delete=models.CASCADE)
    sequence = models.IntegerField()
    number = models.CharField(max_length=8)
    name = models.CharField(max_length=250)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        ordering = ['sequence']
