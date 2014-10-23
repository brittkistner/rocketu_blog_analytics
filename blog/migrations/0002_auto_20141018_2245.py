# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import timedelta

from django.db import models, migrations
from django.utils.timezone import now


def create_initial_data(apps, schema_editor):
    Author = apps.get_model("blog", "Author")
    anna = Author.objects.create(name='Anna Conda', bio='Loves python!')
    george = Author.objects.create(name='George Orwell',
                                   bio='George Orwell was an English novelist, essayist, and critic.')

    Tag = apps.get_model("blog", "Tag")
    programming_tag = Tag.objects.create(name='Programming')
    awesomeness_tag = Tag.objects.create(name='Awesomeness')
    django_tag = Tag.objects.create(name='Django')

    Post = apps.get_model("blog", "Post")
    post_one = Post.objects.create(body='Django makes it easy to get from 0 to working application in weeks!',
                                   title='Why I Love Django',
                                   author=anna)
    # Need to set created after already saved
    post_one.created = now() - timedelta(days=14)
    post_one.save()
    post_one.tags.add(programming_tag, django_tag)

    post_two = Post.objects.create(body='In Django 1.7 we were introduced to built-in migrations!',
                                   title='How Django Got Better',
                                   author=anna)
    post_two.created = now() - timedelta(days=7)
    post_two.save()
    post_two.tags.add(programming_tag, awesomeness_tag, django_tag)

    post_three = Post.objects.create(body="Are they talking about Django Reinhardt or Django Unchained?",
                                     title="I've Never Heard of Django",
                                     author=george)
    post_three.created = now() - timedelta(days=21)
    post_three.save()
    post_three.tags.add(awesomeness_tag, django_tag)


def remove_initial_data(apps, schema_editor):
    Author = apps.get_model("blog", "Author")
    Author.objects.all().delete()

    Tag = apps.get_model("blog", "Tag")
    Tag.objects.all().delete()

    Post = apps.get_model("blog", "Post")
    Post.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_code=remove_initial_data)
    ]