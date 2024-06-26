# Generated by Django 4.1.7 on 2024-05-21 12:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0002_remove_product_images"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("alt", models.CharField(max_length=255)),
                ("image", models.ImageField(upload_to="images/%Y/%m/%d")),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="images",
            field=models.ManyToManyField(
                blank=True, null=True, to="product.productimage"
            ),
        ),
    ]
