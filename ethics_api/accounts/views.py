from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from django.core.mail import send_mail
import random
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        phone = data.get("phone")

        print("REGISTER DATA:", data)

        if not all([username, password, email, phone]):
            return Response(
                {"error": "Usuario, contraseña, correo y teléfono requeridos"},
                status=400
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "El usuario ya existe"},
                status=400
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "El correo ya está registrado"},
                status=400
            )

        if User.objects.filter(phone=phone).exists():
            return Response(
                {"error": "El teléfono ya está registrado"},
                status=400
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone
        )

        return Response(
            {"message": "Usuario registrado correctamente"},
            status=201
        )



class LoginStepOneView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Usuario y contraseña requeridos"},
                status=400
            )

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"error": "Credenciales inválidas"},
                status=401
            )

        if not user.email:
            return Response(
                {"error": "Usuario sin correo registrado"},
                status=400
            )

        otp = str(random.randint(100000, 999999))
        cache.set(username, otp, timeout=300)

        send_mail(
            subject="Tu código de verificación",
            message=f"Tu código OTP es: {otp}",
            recipient_list=[user.email],
            from_email=None,
        )

        return Response({
            "message": "OTP enviado al correo",
            "username": username
        })


class VerifyOTPView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        otp = request.data.get("otp")

        if not username or not otp:
            return Response(
                {"error": "Datos incompletos"},
                status=400
            )

        cached_otp = cache.get(username)

        if cached_otp != otp:
            return Response(
                {"error": "OTP inválido o expirado"},
                status=400
            )

        user = User.objects.get(username=username)
        token = RefreshToken.for_user(user)

        cache.delete(username)

        return Response({
            "access": str(token.access_token),
            "refresh": str(token)
        })
