from django.db import models


# Create your models here.
class Market_Details(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    symbol = models.CharField(max_length=10, null=True)
    image = models.URLField(null=True)
    name = models.CharField(max_length=200, null=True)
    current_price = models.FloatField(null=True)
    market_cap = models.BigIntegerField(null=True)
    market_cap_rank = models.BigIntegerField(null=True)
    fully_diluted_valuation = models.BigIntegerField(null=True)
    total_volume = models.BigIntegerField(null=True)
    high_24h = models.FloatField(null=True)
    low_24h = models.FloatField(null=True)
    price_change_24h = models.FloatField(null=True)
    price_change_percentage_24h = models.FloatField(null=True)
    market_cap_change_24h = models.FloatField(null=True)
    market_cap_change_percentage_24h = models.FloatField(null=True)
    circulating_supply = models.BigIntegerField(null=True)
    total_supply = models.BigIntegerField(null=True)
    max_supply = models.BigIntegerField(null=True)
    ath = models.FloatField(null=True)
    ath_change_percentage = models.FloatField(null=True)
    ath_date = models.DateField(null=True)
    atl = models.FloatField(null=True)
    atl_date = models.DateTimeField(null=True)
    atl_change_percentage = models.FloatField(null=True)
    roi = models.FloatField(null=True)
    last_updated = models.DateTimeField(null=True)

# ['id', 'symbol', 'name', 'image',
# 'current_price', 'market_cap', 'market_cap_rank', 'fully_diluted_valuation', 'total_volume', 'high_24h', 
# 'low_24h', 'price_change_24h', 'price_change_percentage_24h', 'market_cap_change_24h', 'market_cap_change_percentage_24h', 
# 'circulating_supply', 'total_supply', 'max_supply', 'ath', 'ath_change_percentage', 'ath_date', '
# atl', 'atl_change_percentage', 'atl_date', 'roi', 'last_updated']
