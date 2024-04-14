from django.db import models


class DataSources(models.Model):
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)  # Enforcing uniqueness
    url = models.CharField(max_length=255)
    frequency = models.IntegerField(help_text="Frequency of data fetch in minutes")
    last_fetched = models.DateTimeField(null=True, blank=True, help_text="Timestamp of the last successful fetch")

    def __str__(self):
        return self.name
