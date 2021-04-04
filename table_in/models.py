from django.db import models
from django.forms import ModelForm
from django.shortcuts import reverse
from django.core.exceptions import ValidationError

# Create your models here.

SHIRT_SIZES = (
    ('1', 'Средний и старший НС'),
    ('2', 'Рядовой и младший НС'),
    ('3', 'Служащий'),
)
class UsersShtat(models.Model):
    name = models.CharField("наименование по штату", max_length=1, choices=SHIRT_SIZES)
    count_shtat = models.IntegerField("Всего по штату")

    def __str__(self):
        return f"{self.get_name_display()} ({self.count_shtat})"
        
    class Meta:
        verbose_name = "Кол-во по штату"
        verbose_name_plural = "Кол-во по штату сотрудников"


class TableStat(models.Model):
    name = models.CharField("Категория", max_length=150)
    number = models.PositiveIntegerField(
        "Последовательность", default=1, unique=True, help_text="Указать последоватлеьность категорий")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class TableUsers(models.Model):
    name = models.CharField("Имя сотрудника", max_length=100)
    user_category = models.CharField("Категория сотрудника",  max_length=1, choices=SHIRT_SIZES)
    doljnost = models.TextField(
        "Должность сотрудника", blank=True)
    user_corona = models.BooleanField("Проходил  обследование?", default=False)
    user_status = models.ForeignKey(
        TableStat, verbose_name="Где находится", on_delete=models.CASCADE, null=True)
    user_date_range = models.CharField("Период отпуска", max_length=19, blank=True, null=True)
    user_medical_date_range = models.CharField(
        "Период больничного", max_length=19, blank=True, null=True)
    image = models.ImageField(
        verbose_name="Подпись", upload_to='images', blank=True)
    users_sign = models.BooleanField(
        verbose_name="Использовать подпись?", default=False)

    def save(self, *args, **kwargs):
        if self.users_sign:
            qs = TableUsers.objects.filter(users_sign=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.count() != 0:
                # choose ONE of the next two lines
                #self.users_sign = False  # keep the existing "chosen one"
                qs.update(users_sign=False) # make this obj "the chosen one"
        super(TableUsers, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Имя"
        verbose_name_plural = "Имена"
