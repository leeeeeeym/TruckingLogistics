from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# Create your models here.
from django.conf import settings
from django.conf import settings

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    address = models.TextField()
    company_name = models.CharField(max_length=100)

    assigned_user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name='assigned_customers'
    )



    assigned_user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name='assigned_customers'
    )




class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('office', 'Office'),
        ('driver', 'Driver'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return f"{self.username} ({self.role})"
        
class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name
    
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=255)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

from datetime import datetime
from django.conf import settings


class Booking(models.Model):
    booking_number = models.CharField(max_length=15, unique=True, editable=False)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='created_bookings')
    status = models.CharField(max_length=255, default="Ongoing")

    def save(self, *args, **kwargs):
        if not self.booking_number:  # Only generate if not already set
            current_year = datetime.now().year
            last_booking = Booking.objects.filter(
                booking_number__startswith=f"{current_year}-"
            ).order_by('id').last()
            if last_booking:
                last_number = int(last_booking.booking_number.split('-')[1])
                self.booking_number = f"{current_year}-{last_number + 1:05d}"
            else:
                self.booking_number = f"{current_year}-00001"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.booking_number  # Display the booking_number as a string
    
class Container(models.Model):
    SIZE_CHOICES = [
        (10, '10'),
        (20, '20'),
        (40, '40'),
    ]

    container_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    size = models.IntegerField(choices=SIZE_CHOICES)
    weight = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    contents = models.TextField()
    status = models.CharField(max_length=255, default='Pending')  # Default status set to Pending
    driver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='containers')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_booking_status()

    def update_booking_status(self):
        sibling_containers = Container.objects.filter(booking=self.booking)
        statuses = [container.status for container in sibling_containers]

        # Define the hierarchy of statuses
        status_hierarchy = ['Pending', 'Ongoing', 'Completed', 'Cancelled']

        # Find the lowest hierarchy status
        lowest_status = min(statuses, key=lambda status: status_hierarchy.index(status))
        self.booking.status = lowest_status
        self.booking.save()

    def get_incremented_booking_number(self):
        sibling_containers = Container.objects.filter(booking=self.booking).order_by('container_id')
        index = list(sibling_containers).index(self) + 1
        return f"{self.booking.booking_number}-{index:02d}"

    def __str__(self):
        return f"Container {self.container_id} for Booking {self.booking}"

    
class ContainerStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    container = models.ForeignKey(Container, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    recipient_name = models.CharField(max_length=255)
    digital_signature = models.BinaryField()

    def __str__(self):
        return f"Status {self.status_id} for Container {self.container}"

class Driver(models.Model):
    driver_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='Unknown')
    

    booking = models.ForeignKey('Booking', on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True)
    container = models.ForeignKey('Container', on_delete=models.SET_NULL, null=True, blank=True, related_name='driver_assignments')
    container = models.ForeignKey('Container', on_delete=models.SET_NULL, null=True, blank=True, related_name='driver_assignments')

    def __str__(self):
        return self.name

    def get_booking_number(self):
        return self.booking.booking_number if self.booking else 'N/A'

    def get_customer_name(self):
        return self.customer.name if self.customer else 'N/A'

    def get_container_contents(self):
        return self.container.contents if self.container else 'N/A'


