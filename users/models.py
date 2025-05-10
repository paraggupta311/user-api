from django.db import models

class User(models.Model):
    """
    User model stores individual user details including name, company, location, and contact information.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    age = models.IntegerField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.IntegerField()
    email = models.EmailField()
    web = models.URLField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
