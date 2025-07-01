from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import hmac
import hashlib
import json
from django.conf import settings

@csrf_exempt
def razorpay_webhook(request):
    if request.method == 'POST':
        data = request.body
        received_signature = request.headers.get('X-Razorpay-Signature')

        secret = settings.RAZORPAY_WEBHOOK_SECRET.encode()
        generated_signature = hmac.new(secret, data, hashlib.sha256).hexdigest()

        if hmac.compare_digest(received_signature, generated_signature):
            payload = json.loads(data)

            if payload['event'] == 'payment.captured':
                # TODO: match payment & update subscription
                print("Webhook received for payment:", payload['payload']['payment']['entity']['id'])

            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

    return HttpResponse("Only POST method allowed", status=405)
