# Generated by Django 4.1.7 on 2024-06-27 12:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0004_productimage_product_alter_product_images"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="vendor_code_public",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="images",
            field=models.ManyToManyField(
                blank=True, related_name="product_images", to="product.productimage"
            ),
        ),
    ]
