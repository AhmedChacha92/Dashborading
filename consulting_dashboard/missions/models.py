from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class ConsultantManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Consultant(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='consultant_set',  # Ajoutez un related_name unique
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='consultant_set',  # Ajoutez un related_name unique
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = ConsultantManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Mission(models.Model):
    
    TYPE_CHOICES = [
        ('web_mobile', 'Développement Web/Mobile'),
        ('consulting', 'Consulting Informatique'),
        ('telephonie', 'Téléphonie'),
        ('reseau', 'Administration Réseau'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    end_date = models.DateField()
    budget_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    assigned_users = models.ManyToManyField(Consultant, related_name='missions', blank=True)
    status = models.CharField(max_length=20, choices=[('not_started', 'Pas débuté'), ('in_progress', 'En cours'), ('finished', 'Fini')], default='not_started')
    solo = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Complaint(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    user = models.ForeignKey(Consultant, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Complaint by {self.user.email} on {self.mission.name}"
