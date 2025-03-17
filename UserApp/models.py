from django.db import models

class UserPersonalDetails(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name

class UserQualificationDetails(models.Model):
    user = models.ForeignKey(UserPersonalDetails, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    year_of_passing = models.IntegerField()

    def __str__(self):
        return f"{self.user.name} - {self.degree}"

class UserProfessionalDetails(models.Model):
    user = models.ForeignKey(UserPersonalDetails, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    experience = models.IntegerField()

    def __str__(self):
        return f"{self.user.name} - {self.company}"
