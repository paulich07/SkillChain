from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import logout
from .models import Event, BadgeNFT, AwardNFT, User
from .serializers import EventSerializer, BadgeNFTSerializer, AwardNFTSerializer, UserSerializer, RegisterUserSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class RegisterUserView(APIView):
    """
    View per registrare nuovi utenti.
    """
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        csrf_token = get_token(request)  # Genera un nuovo CSRF token
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data["password"])  # Hash della password
            user.save()

            return Response({
                "message": "Registrazione avvenuta con successo!",
                "user_id": user.id,
                "username": user.username,
                "csrf_token": csrf_token  # Invia il CSRF token per autenticazione futura
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(APIView):
    """
    Login con sessione Django (senza JWT).
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({"error": "Credenziali non valide"}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)  # Effettua il login dell'utente nella sessione

        csrf_token = get_token(request)  # Genera il CSRF token per sicurezza

        return Response({
            "message": "Login effettuato con successo",
            "csrf_token": csrf_token
        }, status=status.HTTP_200_OK)


class CustomLogoutView(APIView):
    """
    Effettua il logout dell'utente e cancella la sessione.
    """
    def post(self, request):
        logout(request)  # Cancella la sessione dell'utente
        return Response({"message": "Logout effettuato con successo"}, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    """
    View per ottenere o modificare i dati personali dell'utente autenticato.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        """Restituisce i dati dell'utente autenticato."""
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "address": user.address,
            "imgURI": user.imgURI,
            "creationDate": user.creationDate,
            "csrf_token": get_token(request)  # Aggiorna il CSRF token
        }, status=status.HTTP_200_OK)

    def patch(self, request):
        """Permette di modificare username o email."""
        user = request.user
        data = request.data

        if "username" in data:
            user.username = data["username"]
        if "email" in data:
            user.email = data["email"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        if "address" in data:
            user.address = data["address"]
        if "imgURI" in data:
            user.imgURI = data["imgURI"]
        

        user.save()
        return Response({"message": "Profilo aggiornato con successo!"}, status=status.HTTP_200_OK)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-start_date')
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]

    ## ✅ Aggiungere uno o più Badge a un evento con `POST` o `PATCH` ##
    @action(detail=True, methods=['post', 'patch'], url_path='badges')
    def add_badges(self, request, pk=None):
        event = get_object_or_404(Event, id=pk)
        badges_data = request.data.get("badges", [])
        
        created_badges = []
        for badge_data in badges_data:
            badge, created = BadgeNFT.objects.get_or_create(**badge_data)
            event.badges.add(badge)
            created_badges.append(badge)

        return Response(BadgeNFTSerializer(created_badges, many=True).data, status=status.HTTP_201_CREATED)

    ## ✅ Modificare un Badge specifico ##
    @action(detail=True, methods=['patch'], url_path='badges/(?P<badge_id>[^/.]+)')
    def update_badge(self, request, pk=None, badge_id=None):
        event = get_object_or_404(Event, id=pk)
        badge = get_object_or_404(event.badges, id=badge_id)

        serializer = BadgeNFTSerializer(badge, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ## ✅ Ottenere un Badge specifico di un evento ##
    @action(detail=True, methods=['get'], url_path='badges/(?P<badge_id>[^/.]+)')
    def get_badge(self, request, pk=None, badge_id=None):
        event = get_object_or_404(Event, id=pk)
        badge = get_object_or_404(event.badges, id=badge_id)
        return Response(BadgeNFTSerializer(badge).data)

    ## ✅ Stessa logica per gli AwardNFT ##
    @action(detail=True, methods=['post', 'patch'], url_path='awards')
    def add_awards(self, request, pk=None):
        event = get_object_or_404(Event, id=pk)
        awards_data = request.data.get("awards", [])

        created_awards = []
        for award_data in awards_data:
            award, created = AwardNFT.objects.get_or_create(**award_data)
            event.awards.add(award)
            created_awards.append(award)

        return Response(AwardNFTSerializer(created_awards, many=True).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='awards/(?P<award_id>[^/.]+)')
    def update_award(self, request, pk=None, award_id=None):
        event = get_object_or_404(Event, id=pk)
        award = get_object_or_404(event.awards, id=award_id)

        serializer = AwardNFTSerializer(award, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='awards/(?P<award_id>[^/.]+)')
    def get_award(self, request, pk=None, award_id=None):
        event = get_object_or_404(Event, id=pk)
        award = get_object_or_404(event.awards, id=award_id)
        return Response(AwardNFTSerializer(award).data)

    @action(detail=True, methods=['post'], url_path='register-user/(?P<user_id>[^/.]+)')
    def register_user(self, request, pk=None, user_id=None):
        event = get_object_or_404(Event, id=pk)
        user = get_object_or_404(User, id=user_id)

        event.participants.add(user)
        event.save()  # ✅ Salva il cambiamento nel DB

        return Response(
            {"message": f"User {user.username} added to event {event.name_event}"},
            status=status.HTTP_200_OK
        )

    ## ✅ Ottenere la struttura completa di un User registrato all'evento ##
    @action(detail=True, methods=['get'], url_path='users/(?P<user_id>[^/.]+)')
    def get_user(self, request, pk=None, user_id=None):
        event = get_object_or_404(Event, id=pk)
        user = get_object_or_404(event.participants, id=user_id)

        return Response(UserSerializer(user).data)

    ## ✅ Ottenere solo l'address di un User registrato all'evento ##
    @action(detail=True, methods=['get'], url_path='users/(?P<user_id>[^/.]+)/address')
    def get_user_address(self, request, pk=None, user_id=None):
        event = get_object_or_404(Event, id=pk)
        user = get_object_or_404(event.participants, id=user_id)

        return Response({"address": user.address})
    
    ## ✅ Ottenere tutti gli address degli utenti iscritti a un evento ##
    @action(detail=True, methods=['get'], url_path='addresses')
    def get_event_addresses(self, request, pk=None):
        event = get_object_or_404(Event, id=pk)

        # Recupera tutti gli utenti iscritti all'evento
        addresses = event.participants.values_list('address', flat=True)

        return Response({"addresses": list(addresses)}, status=status.HTTP_200_OK)
