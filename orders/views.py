import datetime
import os
from .helpers import (
    generate_numeric_order_number,
    generate_invoice,
    generate_invoice_delivery
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from users.models import AddressBook, Company
from .models import Order, Cart, Guest, OrderItem, Shipping, Billing,BankDetails
from .serializers import OrderSerializer, CartSerializer
from product.models import Product
from rest_framework import status
from discount.models import Discount
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from store.models import Store
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.status import HTTP_404_NOT_FOUND


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


class OrderGetAPIView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get(self, request, pk):
        if self.request.user:
            order = Order.objects.get(id=pk)
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class OrderAPIView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        number = generate_numeric_order_number()
        if self.request.user:

            cartItems = Cart.objects.filter(user=self.request.user)
            cart_objs = []
            total = 0
            shipping = None
            store = None
            delivery_price = 0.00
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

            company_total_auth = None
            if company:
                company_total_auth = total * company.sale_percent / 100

            order = Order.objects.create(
                user=self.request.user,
                company=company,
                discount=discount,
                total=total,
                delivery_price=delivery_price,
                number=number,
                shipping=shipping,
                store=store,
                billing=billing,
                order_created=datetime.now(),
                company_total_auth=company_total_auth,
            )
            order.save()
            for item in cartItems:
                order_item = OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    user=self.request.user,
                    price=item.product.price,
                    sale=item.product.sale,
                )
                product = Product.objects.get(pk=item.product.id)
                product.qty -= item.quantity
                product.sold += item.quantity
                product.save()
                price = item.product.price
                if item.product.sale:
                    price = price - (price * item.product.sale / 100)
                total += price * item.quantity
                cart_objs.append(order_item)
                item.delete()
                
            for cart_obj in cart_objs:
                cart_obj.order = order
                cart_obj.save()
                order.items.add(cart_obj)
            order.total = total
            order.save()

            email_body = (
                'Dear Customer,\n\n'
                'Thank you for your order. '
                'We are processing your order and will get back to you with invoice soon.\n'
                'We need to inform you that some items might missing in our stock.\n'
                'Our manager will contact you soon.\n'
                'Thanks for waiting! \n\n'
                'Best regards,\n'
                'Floristika'
            )

            email = EmailMessage(
                subject=f"{number} Order Floristika",
                body=email_body,
                to=[self.request.user.email,],
                from_email=settings.EMAIL_HOST_USER,
            )
            # email.attach_file(file_path)
            email.send()

            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)


class OrgerGuestGetAPIView(APIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get(self, request, number):
        order = Order.objects.get(number=number)
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
        delivery_price = 0.00
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
        cart_objs = []
        total = 0
        discount = None
        if len(self.request.data.get('discount')):
            discount = Discount.objects.get(code=self.request.data.get('discount'))

        order = Order.objects.create(
            guest=guest,
            discount=discount,
            total=total,
            number=number,
            shipping=shipping,
            store=store,
            billing=billing,
            delivery_price=delivery_price,
            order_created=datetime.now(),
        )
        order.save()
        for item in data.get('items'):
            product = Product.objects.get(slug=item['product'])
            quantity = int(item['quantity'])
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                guest=guest,
                price=product.price,
                sale=product.sale,
            )
            product.qty -= quantity
            product.sold += quantity
            product.save()
            price = product.price
            if product.sale:
                price = product.price - (product.price * product.sale / 100)
            total += price * quantity
            cart_objs.append(order_item)
        for cart_obj in cart_objs:
            order.items.add(cart_obj)
        order.total = total
        order.save()

        email_body = (
            'Dear Customer,\n\n'
            'Thank you for your order. '
            'We are processing your order and will get back to you with invoice soon.\n'
            'We need to inform you that some items might missing in our stock.\n'
            'Our manager will contact you soon.\n'
            'Thanks for waiting! \n\n'
            'Best regards,\n'
            'Floristika'
        )

        email = EmailMessage(
            subject=f"{number} Order Floristika",
            body=email_body,
            to=[guest.email,],
            from_email=settings.EMAIL_HOST_USER,
        )
        email.send()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


class OrderInvoiceAPIView(APIView):
    """Get Invoice Api View"""
    serializer_class = OrderSerializer
    permission_classes = [AllowAny, ]
    
    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        bank_details = BankDetails.objects.first()

        invoice = generate_invoice(
            order=order,
            bank_details=bank_details,
            billing=order.billing,
            company=order.company,
            cart_objs=order.items.all(),
            number=order.number,
            company_total_auth=order.company_total_auth,
        )

        return FileResponse(open(invoice, "rb"), as_attachment=True)

    def delete(self, request, pk):
        order = Order.objects.get(id=pk)
        directory_path = os.path.join(settings.MEDIA_ROOT, "invoices", order.number)
        os.makedirs(directory_path, exist_ok=True)
        file_path = os.path.join(directory_path, f"invoice_{order.number}.pdf")
        if os.path.exists(file_path):
            os.remove(file_path)
            return Response(
                {"message": "The file deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"message": "The file does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class OrderInvoiceSendAPIView(APIView):
    """Send Invoice Api View"""
    serializer_class = OrderSerializer
    permission_classes = [AllowAny, ]

    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        bank_details = BankDetails.objects.first()

        invoice = generate_invoice(
            order=order,
            bank_details=bank_details,
            billing=order.billing,
            company=order.company,
            cart_objs=order.items.all(),
            number=order.number,
            company_total_auth=order.company_total_auth,
        )

        email_body = (
            'Dear Customer,\n\n'
            'Thank you for your order. '
            'We are processing your order and will get back to you with invoice soon.\n'
            'Thanks for waiting! \n\n'
            'Best regards,\n'
            'Floristika'
        )
        if order.user:
            email = order.user.email
        else:
            email = order.guest.email

        email = EmailMessage(
            subject=f"{order.number} Order Floristika",
            body=email_body,
            to=[email,],
            from_email=settings.EMAIL_HOST_USER,
        )
        email.attach_file(invoice)
        email.send()
        os.remove(invoice)
        return Response(status=status.HTTP_200_OK)


class GetOrderStatusTelegramAPIView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, number):
        try:
            order = Order.objects.get(number=number)
            status = order.status
            return Response({"status": status})
        except:
            return Response({"message": "No such order."}, status=HTTP_404_NOT_FOUND)


class DeliveryOrderInvoiceAPIView(APIView):
    """Get Delivery Invoice Api View"""
    serializer_class = OrderSerializer
    permission_classes = [AllowAny, ]

    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        bank_details = BankDetails.objects.first()

        invoice = generate_invoice_delivery(
            order=order,
            bank_details=bank_details,
            billing=order.billing,
            number=order.number,
            delivery_price=order.delivery_price,
        )

        return FileResponse(open(invoice, "rb"), as_attachment=True)

    def delete(self, request, pk):
        order = Order.objects.get(id=pk)
        directory_path = os.path.join(settings.MEDIA_ROOT, "invoices", order.number)
        os.makedirs(directory_path, exist_ok=True)
        file_path = os.path.join(directory_path, f"delivery_invoice_{order.number}.pdf")
        if os.path.exists(file_path):
            os.remove(file_path)
            return Response(
                {"message": "The file deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"message": "The file does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class DeliveryOrderInvoiceSendAPIView(APIView):
    """Send Invoice Api View"""
    serializer_class = OrderSerializer
    permission_classes = [AllowAny, ]

    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        bank_details = BankDetails.objects.first()

        invoice = generate_invoice_delivery(
            order=order,
            bank_details=bank_details,
            billing=order.billing,
            number=order.number,
            delivery_price=order.delivery_price,
        )

        email_body = (
            'Dear Customer,\n\n'
            'Thank you for your order. '
            'Please pay for your order delivery.\n'
            'Thanks! \n\n'
            'Best regards,\n'
            'Floristika'
        )
        if order.user:
            email = order.user.email
        else:
            email = order.guest.email

        email = EmailMessage(
            subject=f"{order.number} Order Floristika",
            body=email_body,
            to=[email, ],
            from_email=settings.EMAIL_HOST_USER,
        )
        email.attach_file(invoice)
        email.send()
        os.remove(invoice)
        return Response(status=status.HTTP_200_OK)
