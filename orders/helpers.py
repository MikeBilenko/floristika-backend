import os
from django.conf import settings
from django.template.loader import get_template
from weasyprint import HTML

import random

def generate_numeric_order_number(length=8):
    order_number = ''.join(random.choices(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], k=length))
    return order_number

def generate_invoice(
    order,
    user,
    cart_objs,
    billing,
    company_total_auth,
    bank_details,
    company,
    number,
):
    new_items = []

    for cart_item in cart_objs:
        product = cart_item.product
        name = product.name
        price = product.price
        sale = product.sale
        sale_percent = product.sale
        quantity = cart_item.quantity
        auth_price = product.price_for_authenticated
        sale_price = None
        sale_auth_price = None
        if product.sale:

            sale_auth_price = auth_price - (auth_price * sale_percent / 100)
            sale_price = price - (price * sale_percent / 100)

        item_data = {
            'name': name,
            'price': price,
            'sale': sale,
            'sale_percent': sale_percent,
            'quantity': quantity,
            'auth_price': auth_price,
            'sale_price': sale_price,
            'sale_auth_price': sale_auth_price
        }

        new_items.append(item_data)

    total = order.total
    result = order.total
    if order.discount:
        discount = order.discount.discount
        result -= total * discount / 100

    if company_total_auth:
        result -= float(company_total_auth)

    context_data = {
        "user": user,
        "bank_details": bank_details,
        "items": new_items,
        "number": order.number,
        "created_date": order.order_date,
        "total": "{:.2f}".format(result + 3),
        "discount": order.discount.discount if order.discount else 0,
        "company": company.sale_percent if company else 0,
        "billing": billing,
    }
    template = get_template('orders/invoice.html')
    html_content = template.render(context_data)

    pdf_file = HTML(string=html_content).write_pdf()

    directory_path = os.path.join(settings.MEDIA_ROOT, "invoices", number)
    os.makedirs(directory_path, exist_ok=True)
    file_path = os.path.join(directory_path, f"invoice_{number}.pdf")
    with open(file_path, 'wb') as f:
        f.write(pdf_file)
    return file_path
    # order.invoice = file_path

    # url = f"{settings.BASE_URL_PATH}{file_path.split('app')[1]}"
    # order.invoice_url = url
    # order.save()
    

    # new_items = []

    #     for cart_item in cart_objs:
    #         product = cart_item.product
    #         name = product.name
    #         price = product.price
    #         sale = product.sale
    #         sale_percent = product.sale
    #         quantity = cart_item.quantity
    #         sale_price = None
    #         if product.sale:
    #             sale_price = price - (price * sale_percent / 100)

    #         item_data = {
    #             'name': name,
    #             'price': price,
    #             'sale': sale,
    #             'sale_percent': sale_percent,
    #             'quantity': quantity,
    #             'sale_price': sale_price,
    #         }

    #         new_items.append(item_data)

    #     total = order.total
    #     result = order.total
    #     if order.discount:
    #         discount = order.discount.discount
    #         result -= total * discount / 100

    #     context_data = {
    #         "user": self.request.user,
    #         "bank_details": bank_details,
    #         "items": new_items,
    #         "number": order.number,
    #         "created_date": order.order_date,
    #         "total": "{:.2f}".format(result + 3),
    #         "discount": order.discount.discount if order.discount else 0,
    #         "billing": billing
    #     }

    #     template = get_template('orders/invoice.html')
    #     html_content = template.render(context_data)

    #     pdf_file = HTML(string=html_content).write_pdf()

    #     directory_path = os.path.join(settings.MEDIA_ROOT, "invoices", str(generate_numeric_order_number()))
    #     os.makedirs(directory_path, exist_ok=True)
    #     file_path = os.path.join(directory_path, f"invoice_{number}.pdf")
    #     with open(file_path, 'wb') as f:
    #         f.write(pdf_file)
    #     order.invoice = file_path
    #     url = f"{settings.BASE_URL_PATH}{file_path.split('app')[1]}"
    #     order.invoice_url = url
    #     order.save()