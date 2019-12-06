from django.db import models


class Profile(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100, blank=True)
    instaName = models.CharField(max_length=100, unique=True)
    token = models.CharField(max_length=200)
    googleID = models.CharField(max_length=100, unique=True)

class musician(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=250, unique=True)

class favoriteMusician(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image1 = models.ForeignKey(musician, on_delete=models.CASCADE, related_name="image1")
    image2 = models.ForeignKey(musician, on_delete=models.CASCADE, related_name="image2")
    image3 = models.ForeignKey(musician, on_delete=models.CASCADE, related_name="image3")
