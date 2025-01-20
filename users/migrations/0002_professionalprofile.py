# Generated by Django 4.2.18 on 2025-01-20 08:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessionalProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_type', models.CharField(choices=[('public', 'Δημόσιος Υπάλληλος'), ('private', 'Ιδιωτικός Υπάλληλος'), ('freelancer', 'Ελεύθερος Επαγγελματίας')], max_length=50)),
                ('ministry', models.CharField(blank=True, choices=[('education', 'Υπουργείο Παιδείας'), ('health', 'Υπουργείο Υγείας'), ('finance', 'Υπουργείο Οικονομικών')], max_length=50, null=True)),
                ('company_type', models.CharField(blank=True, choices=[('tech', 'Τεχνολογία'), ('finance', 'Χρηματοοικονομικά'), ('retail', 'Λιανικό Εμπόριο')], max_length=50, null=True)),
                ('specialization', models.CharField(blank=True, choices=[('doctor', 'Γιατρός'), ('lawyer', 'Δικηγόρος'), ('engineer', 'Μηχανικός')], max_length=50, null=True)),
                ('job_name', models.TextField(blank=True, null=True)),
                ('experience', models.TextField(blank=True, null=True)),
                ('job_address', models.TextField(blank=True, null=True)),
                ('job_phone', models.TextField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='professional_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]