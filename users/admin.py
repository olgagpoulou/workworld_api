from django.contrib import admin

import users
from .models import User, ProfessionalProfile

admin.site.register(User)
# Τα μοντέλα μου που θα φαίνονται σε σελίδα του Admin
class ProfessionalProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_type', 'ministry', 'company_type', 'specialization')  # Τα πεδία που θες να εμφανίζονται στην λίστα
    search_fields = ('user__email', 'user__name')  # Πεδίο αναζήτησης για τον χρήστη
    list_filter = ('job_type',)  # Φίλτρο για τα τύπους εργασίας, για παράδειγμα

# Καταχώρηση του ProfessionalProfile στο admin
admin.site.register(ProfessionalProfile, ProfessionalProfileAdmin)


# Register your models here.
