from django.db import models
from prices.models import DataSources


class PriceRecords(models.Model):
    symbol = models.CharField(max_length=10, db_index=True)
    price_decimal = models.DecimalField(max_digits=19, decimal_places=4, help_text="Normalized price of the currency")
    price_raw = models.CharField(max_length=255, help_text="Original format of the price")
    source = models.ForeignKey(DataSources, on_delete=models.CASCADE, related_name='price_records')
    timestamp = models.DateTimeField()
    block_no = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.symbol} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.price_decimal}"
