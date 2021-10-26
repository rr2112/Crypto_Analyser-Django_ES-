# Generated by Django 3.2.8 on 2021-10-25 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexing', '0003_market_details_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market_details',
            name='ath',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='ath_change_percentage',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='ath_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='atl',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='atl_change_percentage',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='atl_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='circulating_supply',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='current_price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='fully_diluted_valuation',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='high_24h',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='image',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='last_updated',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='low_24h',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='market_cap',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='market_cap_change_24h',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='market_cap_change_percentage_24h',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='market_cap_rank',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='max_supply',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='price_change_24h',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='price_change_percentage_24h',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='roi',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='symbol',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='total_supply',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='market_details',
            name='total_volume',
            field=models.BigIntegerField(null=True),
        ),
    ]