# Generated by Django 2.2.4 on 2019-10-30 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20191029_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='muestra',
            name='consent',
            field=models.BooleanField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='muestra',
            name='pred_true',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
