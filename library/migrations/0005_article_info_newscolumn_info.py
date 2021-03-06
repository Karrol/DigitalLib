# Generated by Django 2.2.5 on 2019-11-18 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_auto_20191119_0035'),
    ]

    operations = [
        migrations.CreateModel(
            name='newsColumn_info',
            fields=[
                ('columnName', models.CharField(default='News', max_length=20, primary_key=True, serialize=False, verbose_name='栏目名')),
                ('URL', models.CharField(max_length=200, verbose_name='网址')),
                ('abstract', models.CharField(max_length=200, verbose_name='简介')),
            ],
        ),
        migrations.CreateModel(
            name='article_info',
            fields=[
                ('articleID', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='栏目名')),
                ('tittle', models.CharField(max_length=200, verbose_name='标题')),
                ('content', models.CharField(max_length=2000, verbose_name='正文')),
                ('pubDate', models.DateTimeField(verbose_name='提交时间')),
                ('author', models.CharField(max_length=200, verbose_name='作者')),
                ('columnName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.newsColumn_info')),
            ],
        ),
    ]
