from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def login(request):
    username_or_email = request.data.get('username')  # Puede ser username o email
    password = request.data.get('password')

    if not username_or_email or not password:
        return Response({"error": "Se requieren usuario/email y contraseña"}, status=status.HTTP_400_BAD_REQUEST)

    # Permitir login con email o username
    user = User.objects.filter(username=username_or_email).first() or User.objects.filter(email=username_or_email).first()

    if user is None:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=user.username, password=password)

    if not user:
        return Response({"error": "Credenciales inválidas"}, status=status.HTTP_400_BAD_REQUEST)

    tokens = get_tokens_for_user(user)
    serializer = UserSerializer(user)

    return Response({"tokens": tokens, "user": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        # Verificar si el email ya está registrado
        if User.objects.filter(email=serializer.validated_data['email']).exists():
            return Response({"error": "El email ya está en uso"}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el usuario primero
        user = serializer.save()

        # Asegúrate de encriptar la contraseña antes de guardar el usuario
        user.set_password(request.data['password'])
        user.save()

        # Agregar usuario al grupo "Clientes"
        clientes_group, _ = Group.objects.get_or_create(name="Users")
        user.groups.add(clientes_group)

        # Generar tokens
        tokens = get_tokens_for_user(user)
        return Response({"tokens": tokens, "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user  # Este usuario viene del token
    serializer = UserSerializer(user)
    return Response(serializer.data)
