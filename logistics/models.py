from django.db import models

class ShippingMethod(models.Model):
    name = models.CharField(max_length=100)
    provider = models.CharField(max_length=100)
    base_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.provider})"
