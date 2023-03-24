# Generated by Django 3.2.6 on 2023-03-24 11:50

import django.db.models.deletion
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import migrations, models
from django.utils import timezone


# ------------- author field in Article model ----------------

def transfer_new_author_field_in_article_model(apps, schema_editor):
    User = get_user_model()
    Article = apps.get_model('blog', 'Article')
    for article in Article.objects.all():
        author = User.objects.filter(username__iexact=article.author).first()
        article.new_author_id = author.id
        article.save()


def transfer_new_category_field_in_article_model(apps, schema_editor):
    Category = apps.get_model('blog', 'Category')
    Article = apps.get_model('blog', 'Article')
    for article in Article.objects.all():
        # TODO: check distinct category
        category, created = Category.objects.get_or_create(title__iexact=article.category)
        print(category, created)
        if category:
            article.new_category_id = category.id
            category.title = article.category
            category.new_status = 'p'
            category.published = category.created
            category.updated = category.created
            category.save()
        else:
            article.new_category_id = None
        article.save()


# ------------- status field in Category model ----------------

# def transfer_data_to_new_design_of_category_model(apps, schema_editor):
#     Category = apps.get_model('blog', 'Category')
#     for category in Category.objects.all():
#         category.new_status = 'p'
#         category.published = category.created
#         category.updated = category.created
#         category.save()


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_category'),
    ]

    operations = [
        # ---------------------------------------- article model ----------------------------------------

        migrations.AddField(
            model_name='article',
            name='new_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL,
                                    null=True),
        ),
        migrations.RunPython(
            code=transfer_new_author_field_in_article_model,
            reverse_code=migrations.RunPython.noop
        ),
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='new_author',
            new_name='author',
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        # ---------------------------------------- category model ----------------------------------------
        migrations.AddField(
            model_name='category',
            name='published',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='category',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='category',
            name='new_status',
            field=models.CharField(choices=[('d', 'draft'), ('p', 'publish')], default='d', max_length=1),
        ),
        # migrations.RunPython(
        #     code=transfer_data_to_new_design_of_category_model,
        #     reverse_code=migrations.RunPython.noop
        # ),
        migrations.RemoveField(
            model_name='category',
            name='status',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='new_status',
            new_name='status',
        ),
        # ---------------------------------------- article model ----------------------------------------
        migrations.AddField(
            model_name='article',
            name='new_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.category'),
        ),
        migrations.RunPython(
            code=transfer_new_category_field_in_article_model,
            reverse_code=migrations.RunPython.noop
        ),
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='new_category',
            new_name='category',
        ),
        # ---------------------------------------- category model ----------------------------------------
        migrations.RemoveField(
            model_name='category',
            name='created',
        ),
    ]