import factory
from factory.django import DjangoModelFactory
from users.models import User
from main.models import FlashCardCollection, FlashCardDeck, FlashCard


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = "john@doe.com"
    password = "password"


class FlashCardCollectionFactory(DjangoModelFactory):
    class Meta:
        model = FlashCardCollection

    name = "Test Collection"
    description = "-"
    user = factory.SubFactory(UserFactory)


class FlashCardDeckFactory(DjangoModelFactory):
    class Meta:
        model = FlashCardDeck

    name = "Test Deck"
    description = "-"
    collection = factory.SubFactory(FlashCardCollectionFactory)


class FlashCardFactory(DjangoModelFactory):
    class Meta:
        model = FlashCard

    deck = factory.SubFactory(FlashCardDeckFactory)
    question = "Question"
    answer = "answer"
