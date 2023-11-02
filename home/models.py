from django.db import models


# Create your models here.


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    yep_id = models.CharField(unique=True, max_length=255)
    event_name = models.CharField(max_length=255)
    end_date = models.DateTimeField()
    last_processed=models.IntegerField(null=True)

    def __str__(self):
        return self.event_name


class CA(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=15)
    verification = models.FileField(upload_to='protected-static/verification_files/', blank=True)
    verified = models.BooleanField(default=False)
    college = models.CharField(max_length=255)
    referral = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=50)
    old_verification = models.CharField(max_length=255, blank=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Registration(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.RESTRICT)
    booking_id = models.CharField(max_length=255, unique=True)
    ticket_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    number_of_tickets = models.PositiveIntegerField(blank=True)
    referral = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=20)
    total_payment = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
