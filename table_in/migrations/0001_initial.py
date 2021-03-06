# Generated by Django 3.0.7 on 2020-09-06 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TableStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Категория')),
                ('number', models.PositiveIntegerField(default=1, help_text='Указать последоватлеьность категорий', unique=True, verbose_name='Последовательность')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='UsersShtat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('1', 'Средний и старший НС'), ('2', 'Рядовой и младший НС'), ('3', 'Служащий')], max_length=1, verbose_name='наименование по штату')),
                ('count_shtat', models.IntegerField(verbose_name='Всего по штату')),
            ],
            options={
                'verbose_name': 'Кол-во по штату',
                'verbose_name_plural': 'Кол-во по штату сотрудников',
            },
        ),
        migrations.CreateModel(
            name='TableUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя сотрудника')),
                ('user_category', models.CharField(choices=[('1', 'Средний и старший НС'), ('2', 'Рядовой и младший НС'), ('3', 'Служащий')], max_length=1, verbose_name='Категория сотрудника')),
                ('doljnost', models.CharField(blank=True, max_length=255, verbose_name='Должность сотрудника')),
                ('user_corona', models.BooleanField(default=False, verbose_name='Проходил  обследование?')),
                ('user_date_range', models.CharField(blank=True, max_length=19, null=True, verbose_name='Отпуск')),
                ('image', models.ImageField(blank=True, upload_to='images', verbose_name='Подпись')),
                ('user_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='table_in.TableStat', verbose_name='Где находится')),
            ],
            options={
                'verbose_name': 'Имя',
                'verbose_name_plural': 'Имена',
            },
        ),
        migrations.CreateModel(
            name='SignUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('users_sign', models.OneToOneField(auto_created=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='table_in.TableUsers', verbose_name='Использовать подпись')),
            ],
            options={
                'verbose_name': 'Подпись',
                'verbose_name_plural': 'Подпись',
            },
        ),
    ]
