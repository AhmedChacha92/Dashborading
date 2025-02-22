# Generated by Django 5.1.5 on 2025-01-24 12:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('end_date', models.DateField()),
                ('budget_per_day', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('not_started', 'Pas débuté'), ('in_progress', 'En cours'), ('finished', 'Fini')], default='not_started', max_length=20)),
                ('assigned_users', models.ManyToManyField(blank=True, related_name='missions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='missions.mission')),
            ],
        ),
    ]
