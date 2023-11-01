import firebase_admin
from firebase_admin import auth
from django.http import JsonResponse

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("credentials.json")  # Replace with your Firebase credentials file
firebase_admin.initialize_app(cred)

class FirebaseTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        id_token = request.META.get("HTTP_AUTHORIZATION")
        if id_token:
            try:
                decoded_token = auth.verify_id_token(id_token)
                request.firebase_user = decoded_token
            except Exception as e:
                pass

        response = self.get_response(request)
        return response
