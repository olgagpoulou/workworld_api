from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings

# Δημιουργία του Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Το πεδίο email πρέπει να είναι καταχωρημένο.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Χρησιμοποιούμε την έτοιμη μέθοδο του Django για τον κωδικό
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

# Ορισμός του προσαρμοσμένου μοντέλου χρήστη
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    username = None  # Δεν χρειάζεται πεδίο για username
    USERNAME_FIELD = 'email'  # Χρησιμοποιούμε το email ως username
    REQUIRED_FIELDS = []  # Δεν απαιτείται το username

    objects = CustomUserManager()  # Ορίζουμε τον Custom User Manager

#Ορισμός του μοντέλου επαγγελματικού προφίλ
#Επιλογές για το είδος του επαγγελματικού προφίλ
class ProfessionalProfile(models.Model):
    JOB_TYPE_CHOICES = [
        ('public', 'Δημόσιος Υπάλληλος'),
        ('private', 'Ιδιωτικός Υπάλληλος'),
        ('freelancer', 'Ελεύθερος Επαγγελματίας'),
    ]

    MINISTRY_CHOICES = [
        ('education', 'Υπουργείο Παιδείας'),
        ('health', 'Υπουργείο Υγείας'),
        ('finance', 'Υπουργείο Οικονομικών'),
    ]

    COMPANY_TYPE_CHOICES = [
        ('tech', 'Τεχνολογία'),
        ('finance', 'Χρηματοοικονομικά'),
        ('retail', 'Λιανικό Εμπόριο'),
    ]

    SPECIALIZATION_CHOICES = [
        ('doctor', 'Γιατρός'),
        ('lawyer', 'Δικηγόρος'),
        ('engineer', 'Μηχανικός'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="professional_profile"
    )
    job_type = models.CharField(
        max_length=50,
        choices=JOB_TYPE_CHOICES,

    )
    ministry = models.CharField(
        max_length=50,
        choices=MINISTRY_CHOICES,
        blank=True,
        null=True
    )
    company_type = models.CharField(
        max_length=50,
        choices=COMPANY_TYPE_CHOICES,
        blank=True,
        null=True
    )
    specialization = models.CharField(
        max_length=50,
        choices=SPECIALIZATION_CHOICES,
        blank=True,
        null=True
    )
    job_name = models.TextField(blank=True, null=True)  # Πεδίο που περιέχει τον τίτλο εργασίας (πχ ονομα υπηρεσίας ή εταιρείας)
    experience = models.TextField(blank=True, null=True)  # Πεδίο για επαγγελματική εμπειρία
    job_address = models.TextField(blank=True, null=True) #Πεδίο για την διεύθυνση εργασίας
    job_phone = models.TextField(blank=True, null=True) #Πεδίο για το τηλέωνο εργασίας

    # Φωτογραφία προφίλ
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)



    def __str__(self):
        return f"{self.user.name}'s Profile"

#Μοντελα για δημιουργια messanger
#Μοντελο συνομιλιων (περιέχει ολες τις συνομιλιες)
class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation ({self.id}) - Participants: {', '.join([p.name for p in self.participants.all()])}"

#Μοντέλο μηνυματων (περιλαμβανει ολα τα μνμ)
class Message(models.Model):
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)