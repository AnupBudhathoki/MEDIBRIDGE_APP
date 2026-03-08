import hmac
import hashlib
import base64
import uuid
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse

from .models import Transaction


def _generate_signature(total_amount, transaction_uuid, product_code, secret):
    """
    Generate HMAC-SHA256 signature for eSewa v2 API.
    eSewa requires signed_field_names = "total_amount,transaction_uuid,product_code"
    and the message format: "total_amount=X,transaction_uuid=Y,product_code=Z"
    """
    message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    digest = hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return base64.b64encode(digest).decode()


@login_required(login_url='log_in')
def start_esewa_payment(request):
    """Initiate eSewa v2 payment for a slot booking."""
    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)

    # fee from the appointment slot
    amount = request.POST.get("fee", "0")

    # eSewa v2 requires total_amount = amount + service_charge + delivery_charge
    # Since both charges are 0 here, total_amount == amount
    service_charge = "0"
    delivery_charge = "0"
    total_amount = str(float(amount) + float(service_charge) + float(delivery_charge))
    # Remove unnecessary decimal if whole number (e.g. "500.0" → "500")
    if total_amount.endswith('.0'):
        total_amount = total_amount[:-2]

    transaction_uuid = str(uuid.uuid4())
    product_code = settings.ESEWA_MERCHANT_ID

    # Build absolute callback URLs — works in dev and production
    success_url = request.build_absolute_uri(reverse('success_esewa'))
    failure_url = request.build_absolute_uri(reverse('failure_esewa'))

    signature = _generate_signature(total_amount, transaction_uuid, product_code, settings.ESEWA_SECRET_KEY)

    # These are the EXACT fields eSewa v2 expects in the POST form
    form_data = {
        "amount": amount,
        "tax_amount": "0",
        "total_amount": total_amount,
        "transaction_uuid": transaction_uuid,
        "product_code": product_code,
        "product_service_charge": service_charge,
        "product_delivery_charge": delivery_charge,
        "success_url": success_url,
        "failure_url": failure_url,
        "signed_field_names": "total_amount,transaction_uuid,product_code",
        "signature": signature,
    }

    context = {
        "form_data": form_data,
        "payment_url": settings.ESEWA_PAYMENT_URL,
    }
    return render(request, "payments/esewa_form.html", context)


def success_esewa(request):
    """Handle eSewa v2 payment success callback (data comes as base64 GET param)."""
    encoded_data = request.GET.get("data") or request.POST.get("data")
    if not encoded_data:
        return HttpResponse("Invalid response: missing data parameter", status=400)

    # Decode base64 → JSON
    try:
        decoded_json = base64.b64decode(encoded_data).decode("utf-8")
        payload = json.loads(decoded_json)
    except Exception:
        return HttpResponse("Invalid data encoding", status=400)

    # Verify signature from eSewa
    try:
        signed_fields = payload.get("signed_field_names", "").split(",")
        message = ",".join([f"{f}={payload[f]}" for f in signed_fields])
        expected_sig = base64.b64encode(
            hmac.new(
                settings.ESEWA_SECRET_KEY.encode(),
                message.encode(),
                hashlib.sha256,
            ).digest()
        ).decode()

        received_sig = payload.get("signature", "")
        if expected_sig.rstrip('=') != received_sig.rstrip('='):
            return HttpResponse("Signature verification failed", status=400)

    except KeyError as e:
        return HttpResponse(f"Missing field in payload: {e}", status=400)

    # Save transaction (get_or_create prevents duplicate records on page refresh)
    txn, _ = Transaction.objects.get_or_create(
        transaction_uuid=payload["transaction_uuid"],
        defaults={
            "transaction_code": payload.get("transaction_code", ""),
            "product_code": payload.get("product_code", ""),
            "fee": payload.get("total_amount", payload.get("amount", 0)),
            "user": request.user if request.user.is_authenticated else None,
            "status": payload.get("status", "COMPLETE"),
        }
    )

    return render(request, "payments/success_esewa.html", {"txn": txn, "payload": payload})


def failure_esewa(request):
    return render(request, "payments/failure_esewa.html")
