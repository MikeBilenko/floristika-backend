import datetime
import os
from rest_framework.permissions import AllowAny
from django.template.loader import get_template
from rest_framework.views import APIView
from rest_framework.response import Response
from weasyprint import HTML
from django.http import HttpResponseServerError
from users.models import AddressBook, Company
from .models import Order, Cart, Guest, OrderItem, Shipping, Billing,BankDetails
from .serializers import OrderSerializer, CartSerializer
from product.models import Product
import random
from rest_framework import status
from discount.models import Discount
from common.models import AuthPercent
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from store.models import Store
from django.core.mail import EmailMessage
from django.conf import settings


class OrderListAPIView(APIView):
    def get(self, request):
        orders = Order.objects.filter(user=self.request.user).order_by('-order_created')

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 5  # Set the number of items per page

        paginated_orders = paginator.paginate_queryset(orders, request)

        serializer = OrderSerializer(paginated_orders, many=True)
        return paginator.get_paginated_response(serializer.data)


class CartAPIView(APIView):
    def get(self, request):
        if self.request.user:
            carts = Cart.objects.filter(user=self.request.user)
            serializer = CartSerializer(carts, many=True)
            return Response(serializer.data)
        return Response(None)

    def post(self, request):
        if self.request.user:
            data = self.request.data
            product = Product.objects.get(slug=data['product'])
            cart = Cart.objects.create(
                user=self.request.user,
                product=product,
                quantity=data['quantity']
            )
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        return Response(None)

    def put(self, request):
        if self.request.user:
            data = self.request.data
            product = Product.objects.get(slug=data['product'])
            cart = Cart.objects.get(
                user=self.request.user,
                product=product,
            )
            cart.quantity = data['quantity']
            cart.save()
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        return Response(None)

    def delete(self, request):
        if self.request.user:
            data = self.request.data
            product = Product.objects.get(slug=self.request.GET.get('product'))
            cart = Cart.objects.get(
                user=self.request.user,
                product=product,
            )
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('Item deleted')


def generate_numeric_order_number(length=8):
    # Generate random order number using digits from the provided list
    order_number = ''.join(random.choices(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], k=length))
    return order_number


class OrderAPIView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        number = generate_numeric_order_number()
        if self.request.user:
            cartItems = Cart.objects.filter(user=self.request.user)
            auth_percent = AuthPercent.objects.first().percent
            cart_objs = []
            total = 0
            total_auth = 0
            shipping = None
            store = None

            company = None
            discount = None

            if self.request.data.get("shipping") is not None:
                if self.request.data.get('shipping') == 'default':
                    shipping = Shipping.objects.create(
                        address=self.request.user.address,
                        city=self.request.user.city,
                        postal_code=self.request.user.postal_code,
                        country=self.request.user.country,
                        phone=self.request.user.address_book_phone
                    )
                else:
                    address_book_item = AddressBook.objects.get(id=int(self.request.data.get('shipping')))
                    shipping = Shipping.objects.create(
                        address=address_book_item.address,
                        city=address_book_item.city,
                        postal_code=address_book_item.postal_code,
                        country=address_book_item.country,
                        phone=address_book_item.phone
                    )
            else:
                if self.request.data.get("store") is not None:
                    store = Store.objects.get(id=int(self.request.data.get("store")))

            if self.request.data.get('billing') == 'default':
                billing = Billing.objects.create(
                    address=self.request.user.address,
                    city=self.request.user.city,
                    postal_code=self.request.user.postal_code,
                    country=self.request.user.country,
                    phone=self.request.user.address_book_phone
                )
            else:
                address_book_item = AddressBook.objects.get(id=int(self.request.data.get('billing')))
                billing = Billing.objects.create(
                    address=address_book_item.address,
                    city=address_book_item.city,
                    postal_code=address_book_item.postal_code,
                    country=address_book_item.country,
                    phone=address_book_item.phone
                )

            if int(self.request.data.get('companyDiscount')) > 0:
                company = Company.objects.get(user=self.request.user)

            if len(self.request.data.get('discount')):
                discount = Discount.objects.get(code=self.request.data.get('discount'))
            for item in cartItems:
                order_item = OrderItem.objects.create(
                    product=item.product,
                    quantity=item.quantity,
                    user=self.request.user
                )
                product = Product.objects.get(pk=item.product.id)
                product.qty -= item.quantity
                product.sold += item.quantity
                product.save()
                price = item.product.price
                if item.product.sale:
                    price = item.product.price - (item.product.price * item.product.sale_percent / 100)
                price_auth = price - (price * auth_percent / 100)
                total += price * item.quantity
                total_auth += price_auth * item.quantity
                cart_objs.append(order_item)
                item.delete()

            order = Order.objects.create(
                user=self.request.user,
                company=company,
                discount=discount,
                total=total,
                auth_percent=auth_percent,
                total_auth=total_auth,
                number=number,
                shipping=shipping,
                store=store,
                billing=billing,
                order_created=datetime.now()
            )
            for cart_obj in cart_objs:
                order.items.add(cart_obj)
            order.save()
            bank_details = BankDetails.objects.first()
            #  12 October, 2023
            given_datetime = datetime(2024, 4, 6, 12, 43)

            # Format to keep only the date part
            formatted_date = given_datetime.strftime('%B %d, %Y')

            new_items = []

            for cart_item in cart_objs:
                product = cart_item.product

                name = product.name
                price = product.price
                sale = product.sale
                sale_percent = product.sale_percent
                quantity = cart_item.quantity
                auth_price = price - (price * auth_percent / 100)
                sale_price = price - (price * sale_percent / 100)
                sale_auth_price = auth_price - (auth_price * sale_percent / 100)

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

            context_data = {
                "user": self.request.user,
                "auth_percent": auth_percent if auth_percent else 0,
                "bank_details": bank_details,
                "items": new_items,
                "number": order.number,
                "created_date": order.order_date,
                "total": "{:.2f}".format(order.total_auth),  # Format total to 2 digits after the decimal point
                "total_discount": "{:.2f}".format(
                    order.total_auth - order.total_auth * order.discount.discount / 100) if order.discount else 0,
                "discount": order.discount.discount if order.discount else 0,
                "company": "{:.2f}".format(company.sale_percent) if company else 0,
                "billing": billing
            }
            template = get_template('orders/invoice.html')
            html_content = template.render(context_data)

            pdf_file = HTML(string=html_content).write_pdf()

            directory_path = os.path.join(settings.MEDIA_ROOT, "invoices", number)
            os.makedirs(directory_path, exist_ok=True)
            file_path = os.path.join(directory_path, f"invoice_{number}.pdf")
            with open(file_path, 'wb') as f:
                f.write(pdf_file)

            order.invoice = file_path
            print("file_path", file_path)

            url = f"{settings.BASE_URL_PATH}{file_path.split('app')[1]}"
            order.invoice_url = url
            print("file_path", url)
            order.save()

            email_body = (
                'Dear Customer,\n\n'
                'Thank you for your order. '
                'Please make the payment and send the invoice to us so we can update your status.\n\n'
                'Best regards,\n'
                'Floristika'
            )

            email = EmailMessage(
                subject='Your Invoice',
                body=email_body,
                to=['mike@codnity.com'],
            )
            email.attach_file(file_path)
            email.send()

            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)

    def get(self, request, pk):
        if self.request.user:
            order = Order.objects.get(user=self.request.user, id=pk)
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)


class OrderGuestAPIView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        number = generate_numeric_order_number()
        data = self.request.data
        shipping = None
        store = None
        guest, _guest = Guest.objects.get_or_create(
            email=data['email'],
            first_name=data['name'],
            last_name=data['surname'],
            phone_number=data['phone'],
            address=data['address'],
            city=data['city'],
            country=data['country'],
            zip_code=data['postal_code'],
        )
        if data.get("store") is None:

            shipping = Shipping.objects.create(
                address=data['address'],
                city=data['city'],
                postal_code=data['postal_code'],
                country=data['country'],
                phone=data['phone'],
            )
        else:
            store = Store.objects.get(id=int(data.get("store")))
        billing = Billing.objects.create(
            address=data['address'],
            city=data['city'],
            postal_code=data['postal_code'],
            country=data['country'],
            phone=data['phone'],
        )
        auth_percent = AuthPercent.objects.first().percent
        cart_objs = []
        total = 0
        total_auth = 0
        discount = None
        if len(self.request.data.get('discount')):
            discount = Discount.objects.get(code=self.request.data.get('discount'))
        for item in data.get('items'):
            product = Product.objects.get(slug=item['product'])
            quantity = int(item['quantity'])
            order_item = OrderItem.objects.create(
                product=product,
                quantity=quantity,
                guest=guest,
            )
            product.qty -= quantity
            product.sold += quantity
            product.save()
            price = product.price
            if product.sale:
                price = product.price - (product.price * product.sale_percent / 100)
            price_auth = price - (price * auth_percent / 100)
            total += price * quantity
            total_auth += price_auth * quantity
            cart_objs.append(order_item)

        order = Order.objects.create(
            guest=guest,
            discount=discount,
            total=total,
            auth_percent=auth_percent,
            total_auth=total_auth,
            number=number,
            shipping=shipping,
            store=store,
            billing=billing,
            order_created=datetime.now(),
        )
        for cart_obj in cart_objs:
            order.items.add(cart_obj)
        order.save()
        try:
            context_data = {}

            template = get_template('orders/invoice.html')
            html_content = template.render(context_data)

            pdf_file = HTML(string=html_content).write_pdf()

            directory_path = os.path.join(settings.MEDIA_ROOT, "invoices", str(generate_numeric_order_number()))
            os.makedirs(directory_path, exist_ok=True)
            file_path = os.path.join(directory_path, 'output.pdf')
            with open(file_path, 'wb') as f:
                f.write(pdf_file)

            # invoice_file=file_path,
            order.invoice = file_path
            order.save()

            email_body = (
                'Dear Customer,\n\n'
                'Thank you for your order. '
                'Please make the payment and send the invoice to us so we can update your status.\n\n'
                'Best regards,\n'
                'Your Company Name'
            )

            email = EmailMessage(
                subject='Your Invoice',
                body=email_body,
                to=['mike@codnity.com'],
            )
            email.attach_file(file_path)
            email.send()

            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)

        except Exception as e:
            return Response({'file_path': file_path, 'context': context_data})

    def get(self, request, number):
        print(number, "NUMBER")
        order = Order.objects.get(number=number)
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


class GeneratePDFAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Get data from request
            context_data = {
                'customer_name': 'John Doe',
            }

            # Render HTML template with context
            template = get_template('orders/invoice.html')
            html_content = template.render(context_data)
            print(html_content)
            # Convert HTML to PDF
            pdf_file = HTML(string=html_content).write_pdf()

            directory_path = os.path.join(settings.MEDIA_ROOT, "invoices" , str(generate_numeric_order_number()))
            print(directory_path, "DIRECTORY PATH")
            os.makedirs(directory_path, exist_ok=True)

            file_path = os.path.join(directory_path, 'output.pdf')

            with open(file_path, 'wb') as f:
                f.write(pdf_file)

            return Response({'file_path': file_path, 'context': context_data})

        except Exception as e:
            return HttpResponseServerError(str(e))
