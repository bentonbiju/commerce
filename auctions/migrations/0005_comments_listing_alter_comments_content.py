# Generated by Django 4.2.4 on 2023-11-13 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_listing_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing', to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='content',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
