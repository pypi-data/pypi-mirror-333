from django.db import models


class Wilaya(models.Model):
    name_ar = models.CharField(max_length=50)
    name_fr = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return str(self.name_fr) + "-" + str(self.code)


class Daira(models.Model):
    name_ar = models.CharField(max_length=50)
    name_fr = models.CharField(max_length=50)
    wilaya = models.ForeignKey("algeria_cities.Wilaya", on_delete=models.CASCADE)

    def __str__(self):
        return self.name_fr


class Commune(models.Model):
    name_ar = models.CharField(max_length=50)
    name_fr = models.CharField(max_length=50)
    daira = models.ForeignKey("algeria_cities.Daira", on_delete=models.CASCADE)

    def __str__(self):
        return self.name_fr