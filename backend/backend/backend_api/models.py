from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    address = models.CharField(max_length=42, unique=True, blank=True, null=True)
    imgURI = models.CharField(max_length=255, blank=True, null=True)  # URL immagine profilo
    creationDate = models.DateTimeField(auto_now_add=True)  # Data di creazione dell'utente


class NFTBase(models.Model):
    id = models.AutoField(primary_key=True)  # ID univoco per ogni NFT
    name = models.CharField(max_length=255)
    event_name = models.CharField(max_length=255)  # Nome dell'evento associato
    cid = models.CharField(max_length=255)  # CID IPFS dell'immagine o metadati NFT

    class Meta:
        abstract = True  # Questa classe non verrà creata nel DB

class BadgeNFT(NFTBase):
    pass  # Identico a NFTBase, ma separato per chiarezza

class AwardNFT(NFTBase):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
      # L'id dell'utente a cui è stato assegnato il premio

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name_event = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    creationDate = models.DateTimeField(auto_now_add=True)  # Data creazione evento
    
    # Relazioni
    participants = models.ManyToManyField(User, related_name="events")  # Molti utenti partecipano a molti eventi
    awards = models.ManyToManyField(AwardNFT, related_name="event_awards")  # Premi NFT assegnati all'evento
    badges = models.ManyToManyField(BadgeNFT, related_name="event_badges")  # Badge NFT distribuiti ai partecipanti
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_event