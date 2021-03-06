# Generated by Django 2.2.5 on 2019-11-18 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import library.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='ISBN',
            field=models.CharField(max_length=13, primary_key=True, serialize=False, verbose_name='ISBN'),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=32, verbose_name='作者'),
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(default='文学', max_length=64, verbose_name='分类'),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, default='null', upload_to=library.models.custom_path, verbose_name='封面'),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.CharField(default='', max_length=1024, verbose_name='详细'),
        ),
        migrations.AlterField(
            model_name='book',
            name='index',
            field=models.CharField(max_length=16, null=True, verbose_name='索引'),
        ),
        migrations.AlterField(
            model_name='book',
            name='location',
            field=models.CharField(default='图书馆1楼', max_length=64, verbose_name='位置'),
        ),
        migrations.AlterField(
            model_name='book',
            name='press',
            field=models.CharField(max_length=64, verbose_name='出版社'),
        ),
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.CharField(max_length=20, null=True, verbose_name='价格'),
        ),
        migrations.AlterField(
            model_name='book',
            name='quantity',
            field=models.IntegerField(default=1, verbose_name='数量'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=128, verbose_name='书名'),
        ),
        migrations.AlterField(
            model_name='borrowing',
            name='ISBN',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Book', verbose_name='ISBN'),
        ),
        migrations.AlterField(
            model_name='borrowing',
            name='amount_of_fine',
            field=models.FloatField(default=0.0, verbose_name='欠款'),
        ),
        migrations.AlterField(
            model_name='borrowing',
            name='date_due_to_returned',
            field=models.DateField(verbose_name='应还时间'),
        ),
        migrations.AlterField(
            model_name='borrowing',
            name='date_issued',
            field=models.DateField(verbose_name='借出时间'),
        ),
        migrations.AlterField(
            model_name='borrowing',
            name='date_returned',
            field=models.DateField(null=True, verbose_name='还书时间'),
        ),
        migrations.AlterField(
            model_name='borrowing',
            name='reader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Reader', verbose_name='读者'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='balance',
            field=models.FloatField(default=0.0, verbose_name='余额'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='max_borrowing',
            field=models.IntegerField(default=5, verbose_name='可借数量'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='name',
            field=models.CharField(max_length=16, unique=True, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='phone',
            field=models.IntegerField(unique=True, verbose_name='电话'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='photo',
            field=models.ImageField(blank=True, upload_to=library.models.custom_path, verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='读者'),
        ),
        migrations.CreateModel(
            name='mysearchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_date', models.DateTimeField(blank=True, default=None, null=True, verbose_name='查询时间')),
                ('ISBN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Book', verbose_name='ISBN')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Reader', verbose_name='读者')),
            ],
            options={
                'verbose_name': '我的查询历史',
                'verbose_name_plural': '我的查询历史',
            },
        ),
        migrations.CreateModel(
            name='Mylibrary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('In_date', models.DateTimeField(blank=True, default=None, null=True, verbose_name='加入时间')),
                ('ISBN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Book', verbose_name='ISBN')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='读者')),
            ],
            options={
                'verbose_name': '我的图书馆',
                'verbose_name_plural': '我的图书馆',
            },
        ),
    ]
