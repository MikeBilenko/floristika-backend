from django.db import models


class PricePercent(models.Model):
    percent = models.FloatField(default=20.00)

    def __str__(self):
        return f"Percent that will be added from price to non-authenticated users: {self.percent}%"