from django.db import models
from account.models import *


class Aboutus(models.Model):
    address = models.CharField(max_length=200, default="قم", verbose_name="آدرس")
    phone = models.CharField(max_length=12, verbose_name="تلفن")
    email = models.EmailField(max_length=50, verbose_name="ایمبل")

    class Meta:
        db_table = 'aboutus'
        verbose_name = "درباره ما"
        verbose_name_plural = "درباره ما"

    def __str__(self):
        return 'شماره {}'.format(self.id)


class Contactus(models.Model):
    title = models.CharField(max_length=30, verbose_name="موضوع")
    email = models.EmailField(max_length=50, verbose_name="ایمبل")
    context = models.TextField(verbose_name='پیام')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contactus'
        verbose_name = "ارتباط با ما"
        verbose_name_plural = "ارتباط با ما"

    def __str__(self):
        return self.title


class Ticket(models.Model):  # ticket title
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True, verbose_name="کاربر")
    title = models.CharField(max_length=30, verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tickets'
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت"

    # is admin
    def __str__(self):
        # return "{} title:{}".format(account.models.Profile.__str__(), self.title)
        return self.profile.__str__()


class Images(models.Model):
    image = models.ImageField(upload_to='Mainimages/', verbose_name="عکس")
    description = models.CharField(max_length=50, verbose_name="توضیحات", null=True, blank=True)

    position_choices = [(1, 'بالا راست'), (2, 'بالا وسط'), (3, 'بالا چپ'), (4, 'وسط راست'), (5, 'وسط وسط'),
                        (6, 'وسط چپ'), (7, 'پایین راست'), (8, 'پایین وسط'), (9, 'پایین چپ')]
    position = models.IntegerField(choices=position_choices, null=True, blank=True, verbose_name="موقعیت")
    slider = 1
    logo = 2
    title_choices = [(slider, 'لوگو'), (logo, 'اسلایدر')]
    title = models.IntegerField(choices=title_choices, null=True, blank=True, verbose_name="کاربرد")
    pub_date = models.DateTimeField(null=True, blank=True, verbose_name="زمان انتشار")

    class Meta:
        db_table = 'base_images'
        verbose_name = "تصاویر"
        verbose_name_plural = "تصاویر"


    def __str__(self):
        return self.title.__str__()


class Socialmedia(models.Model):
    name = models.CharField(max_length=20, verbose_name="نام")
    link = models.URLField(max_length=200, unique=True, verbose_name="لینک")

    class Meta:
        db_table = 'socialmedias'
        verbose_name = "رسانه"
        verbose_name_plural = "رسانه"

    def __str__(self):
        return self.name


class HomeSetting(models.Model):
    slogan = models.CharField(max_length=300, verbose_name="شعار")
    superiority = models.TextField(null=True, blank=True, verbose_name="برتری")
    image = models.OneToOneField(Images, on_delete=models.PROTECT, verbose_name="تصاویر", related_name="photos",
                                 null=True, blank=True)
    aboutus = models.OneToOneField(Aboutus, on_delete=models.PROTECT, verbose_name="درباره ما")
    socialmedia = models.ManyToManyField(Socialmedia, verbose_name="شبکه های اجتماعی")
    sllider = models.ManyToManyField(Images, verbose_name="اسلایدر")
    logo = models.ForeignKey(Images, verbose_name="عکس لوگو", on_delete=models.PROTECT, related_name="logo",
                             null=True)

    class Meta:
        db_table = 'home_settings'
        verbose_name = "صفحه اصلی"
        verbose_name_plural = "صفحه اصلی"

    def __str__(self):
        return 'شماره {}'.format(self.id)
