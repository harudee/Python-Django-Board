# Generated by Django 3.2.7 on 2021-09-13 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_board_filesize'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('idx', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=500)),
                ('content', models.TextField(null=True)),
                ('point', models.IntegerField(default=0)),
            ],
        ),
    ]
