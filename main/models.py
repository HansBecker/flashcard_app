from django.db import models
from users.models import User


class FlashCardCollection(models.Model):
    """
    Collection of FlashCardDecks. Can have many FlashCardDeck objects
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now=True)


class FlashCardDeck(models.Model):
    """
    FlashCardDeck which contains FlashCards and belongs to a FlashCardCollection
    """

    name = models.CharField(max_length=256)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(FlashCardCollection, on_delete=models.CASCADE, null=True)


class FlashCard(models.Model):
    """
    FlashCard that is the basic unit of learning for the flashcard app
    """

    deck = models.ForeignKey(FlashCardDeck, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
