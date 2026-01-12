from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
import random
User = get_user_model()

class VerifyOTPView(APIView):
    authentication_classes = []  # sin JWT, es login

    def post(self, request):
        phone = request.data.get("phone")
        otp = request.data.get("otp")

        # Validación simple
        if not phone or not otp:
            return Response(
                {"error": "Teléfono y OTP son requeridos"},
                status=400
            )

        # Verificar OTP
        if cache.get(phone) != otp:
            return Response(
                {"error": "OTP inválido o expirado"},
                status=400
            )

        # Crear o recuperar usuario
        user, _ = User.objects.get_or_create(
            username=phone,
            defaults={"phone": phone}
        )

        # Generar JWT
        token = RefreshToken.for_user(user)

        return Response({
            "access": str(token.access_token),
            "refresh": str(token)
        })

class RequestOTPView(APIView):
    authentication_classes = []

    def post(self, request):
        phone = request.data.get("phone")

        if not phone:
            return Response({"error": "Teléfono requerido"}, status=400)

        otp = str(random.randint(100000, 999999))

        # Guardar OTP 5 minutos
        cache.set(phone, otp, timeout=300)

        # Simulación SMS
        print(f"OTP para {phone}: {otp}")

        return Response({"message": "OTP enviado"})
