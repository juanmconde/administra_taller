# Generated by Django 5.1.4 on 2024-12-24 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maquinas', '0007_alter_maquina_problema'),
    ]

    operations = [
        migrations.AddField(
            model_name='reparacion',
            name='id_unico',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
