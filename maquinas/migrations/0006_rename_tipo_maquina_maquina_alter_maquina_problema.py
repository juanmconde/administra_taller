# Generated by Django 5.1.4 on 2024-12-22 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maquinas', '0005_remove_reparacion_total_reparacion_cliente_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='maquina',
            old_name='tipo',
            new_name='maquina',
        ),
        migrations.AlterField(
            model_name='maquina',
            name='problema',
            field=models.TextField(max_length=100),
        ),
    ]