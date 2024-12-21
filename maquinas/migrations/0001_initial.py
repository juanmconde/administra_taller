# Generated by Django 5.1.4 on 2024-12-19 10:42

import datetime
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=15)),
                ('fecha_registro', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Maquina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=100)),
                ('problema', models.TextField()),
                ('fecha_entrada', models.DateField(default=datetime.date.today)),
                ('id_unico', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('cliente', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='maquinas', to='maquinas.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Reparacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('mano_obra', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('maquina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reparaciones', to='maquinas.maquina')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleReparacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('descripcion', models.CharField(max_length=255)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('reparacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='maquinas.reparacion')),
            ],
        ),
    ]
