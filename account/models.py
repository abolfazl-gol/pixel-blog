from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربری", related_name='profile')
    # name = models.CharField(max_length=100, verbose_name="نام")
    # family = models.CharField(max_length=100, null=True, verbose_name="نام خانوادگی")
    # email = models.EmailField(max_length=100, verbose_name="ایمیل")

    phone = models.CharField(max_length=11, verbose_name="شماره همراه")
    profile_image = models.ImageField(upload_to="account/images", null=True, verbose_name="عکس پروفایل")
    men = 1
    women = 2
    noidea = 3
    gender_choices = [(men, 'مرد'), (women, 'زن'), (noidea, 'نظری ندارم')]
    gender = models.IntegerField(choices=gender_choices, verbose_name="جنسیت", null=True)
    born_date = models.DateField(verbose_name="تاریخ تولد", null=True)
    credit = models.IntegerField(verbose_name="اعتبار", default=0)

    def __str__(self):
        return "نام کاربر:  {} {} ".format(self.User.first_name, self.User.last_name)

    class Meta:
        db_table = 'profiles'
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
