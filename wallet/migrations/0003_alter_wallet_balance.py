# Generated by Django 4.2.9 on 2024-01-26 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wallet", "0002_alter_transaction_amount_alter_wallet_balance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wallet",
            name="balance",
            field=models.DecimalField(decimal_places=4, default=0, max_digits=18),
        ),
    ]