from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.views import View
from django.core.mail import send_mail
from .models import PaymentHistory 
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Price, Product

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutSessionView(LoginRequiredMixin,View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page

    need to run this command on cmd : listen --forward-to localhost:8000/products/webhooks/stripe/
    """
    
    LOGIN_URL = 'login'

    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(price.price) * 100,
                        "product_data": {
                            "name": price.product.name,
                            "description": price.product.desc,
                            "images": [
                                f"{settings.BACKEND_DOMAIN}/{price.product.thumbnail}"
                            ],
                        },
                    },
                    "quantity": price.product.quantity,
                }
            ],
            metadata={"product_id": price.product.id},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        return redirect(checkout_session.url)
    

@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    """
    Stripe webhook view to handle checkout session completed event.
    """

    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            print("Payment successful")
            session = event["data"]["object"]
            customer_email = session["customer_details"]["email"]
            product_id = session["metadata"]["product_id"]
            product = get_object_or_404(Product, id=product_id)

            send_mail(
                subject="Here is your product",
                message=f"Thanks for your purchase. The URL is: {product.url}",
                recipient_list=[customer_email],
                from_email="user@gmail.com",
            )

            PaymentHistory.objects.create(
                email=customer_email, product=product, payment_status="C"
            ) # Add this
        else :
            PaymentHistory.objects.create(
                email=customer_email, product=product, payment_status="F"
            ) # Add this
        # Can handle other events here.

        return HttpResponse(status=200)
    

def ProductListView(request):
     products = Product.objects.all()
     context = {'products':products}
     return render(request,'products/product_list.html', context)


def ProductDetailView(request,pk):

    product = get_object_or_404(Product, pk=pk)
    prices = Price.objects.filter(product=product)

    context = {
        'product': product,
        'prices': prices
    }
    return render(request,'products/product_detail.html', context)

def SuccessView(request):
    return render(request,"products/success.html")

def CancelView(request):
    return render(request,"products/cancel.html")


