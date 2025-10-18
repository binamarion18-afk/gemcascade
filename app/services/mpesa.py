from __future__ import annotations
import os
import base64
import datetime as dt
import requests

M_PESA_BASE = os.environ.get("MPESA_BASE", "https://sandbox.safaricom.co.ke")
CONSUMER_KEY = os.environ.get("MPESA_CONSUMER_KEY", "test")
CONSUMER_SECRET = os.environ.get("MPESA_CONSUMER_SECRET", "test")
BUSINESS_SHORT_CODE = os.environ.get("MPESA_SHORT_CODE", "174379")
PASSKEY = os.environ.get("MPESA_PASSKEY", "passkey")
CALLBACK_URL = os.environ.get("MPESA_CALLBACK_URL", "https://example.com/api/payments/callback")


def get_access_token() -> str:
    resp = requests.get(
        f"{M_PESA_BASE}/oauth/v1/generate?grant_type=client_credentials",
        auth=(CONSUMER_KEY, CONSUMER_SECRET),
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json().get("access_token", "")


def stk_push(msisdn: str, amount: int, account_ref: str, tx_desc: str) -> dict:
    timestamp = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(f"{BUSINESS_SHORT_CODE}{PASSKEY}{timestamp}".encode()).decode()
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "BusinessShortCode": BUSINESS_SHORT_CODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": msisdn,
        "PartyB": BUSINESS_SHORT_CODE,
        "PhoneNumber": msisdn,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": account_ref,
        "TransactionDesc": tx_desc,
    }
    resp = requests.post(f"{M_PESA_BASE}/mpesa/stkpush/v1/processrequest", json=payload, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()
