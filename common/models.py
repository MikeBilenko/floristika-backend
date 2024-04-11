from django.db import models


class AuthPercent(models.Model):
    percent = models.FloatField(verbose_name="Percent for authenticated users.", default=10.00)

    def __str__(self):
        return str(self.percent)
