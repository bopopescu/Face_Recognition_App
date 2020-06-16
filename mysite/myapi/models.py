from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    gender = models.CharField(max_length=60)
    image_url = models.CharField(max_length=100)
    # owner = models.ForeignKey('auth.User', related_name='people', on_delete=models.CASCADE)

    class Meta:
        app_label = 'person'

    def __str__(self):
        string = self.first_name + "\n" + self.last_name + "\n" + self.email + "\n"
        return string + "\n" + self.gender + "\n" + self.image_url


class Admin(models.Model):
    username = models.CharField(max_length=60)
    password = models.CharField(max_length=60)

    class Meta:
        app_label = 'admin'

    def __str__(self):
        return "Username: " + self.username + "\nPassword: " + self.password

