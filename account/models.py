from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربری", related_name='profile')
    phone = models.CharField(max_length=11, verbose_name="شماره همراه")
    profile_image = models.ImageField(upload_to="account/images", null=True, blank=True, verbose_name="عکس پروفایل")
    men = 1
    women = 2
    noidea = 3
    gender_choices = [(men, 'مرد'), (women, 'زن'), (noidea, 'نظری ندارم')]
    gender = models.IntegerField(choices=gender_choices, verbose_name="جنسیت", null=True)
    born_date = models.DateField(verbose_name="تاریخ تولد", null=True)
    credit = models.IntegerField(verbose_name="اعتبار", default=0)

    class Meta:
        db_table = 'profiles'
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return "id: {} ".format(self.user.id)
    

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    phone =models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'addresses'

    def __str__(self):
        return self.name
