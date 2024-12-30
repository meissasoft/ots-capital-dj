# Generated by Django 5.1.4 on 2024-12-29 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OHLC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10)),
                ('timeframe', models.CharField(default='1m', max_length=10)),
                ('timestamp', models.DateTimeField()),
                ('open_price', models.FloatField()),
                ('high_price', models.FloatField()),
                ('low_price', models.FloatField()),
                ('close_price', models.FloatField()),
                ('volume', models.FloatField(default=0.0)),
            ],
            options={
                'indexes': [models.Index(fields=['symbol', 'timeframe', 'timestamp'], name='trading_ohl_symbol_7cb5ff_idx')],
                'unique_together': {('symbol', 'timeframe', 'timestamp')},
            },
        ),
    ]