# Generated by Django 4.0.6 on 2022-07-31 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_alter_cart_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='totalPrice',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ordertable',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.cart'),
        ),
        migrations.AlterField(
            model_name='ordertable',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
