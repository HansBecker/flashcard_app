from django.test import TestCase, Client
from testing.factories import (
    UserFactory,
    FlashCardCollectionFactory,
    FlashCardDeckFactory,
    FlashCardFactory,
)


class TestLoginView(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = UserFactory.create()

    def test_get(self):
        client = Client()
        response = client.get("")
        assert response.status_code == 200

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()


class TestHomeView(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = UserFactory.create()

    def test_get(self):
        client = Client()
        client.force_login(self.user)
        response = client.get("/home/")
        assert response.status_code == 200

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()


class TestCreateCollectionView(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = UserFactory.create()

    def test_get(self):
        client = Client()
        client.force_login(self.user)
        response = client.get("/create_collection")
        assert response.status_code == 200

    def test_post(self):
        client = Client()
        client.force_login(self.user)
        data = {"name": "Test collection", "description": "Test"}
        response = client.post("/create_collection", data)
        # On success redirects to /home/
        assert response.status_code == 302
        assert response.url == "/home/"

    def test_post_no_data(self):
        client = Client()
        client.force_login(self.user)
        response = client.post("/create_collection", {})
        assert response.status_code == 200

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()


class TestDeleteCollectionView(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.collection = FlashCardCollectionFactory.create()
        cls.user = cls.collection.user

    def test_post(self):
        client = Client()
        client.force_login(self.collection.user)
        id = self.collection.id
        response = client.post(f"/delete_collection/{id}")
        assert response.status_code == 302
        assert response.url == "/home/"

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()


class TestCreateFlashDeckView(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.collection = FlashCardCollectionFactory.create()
        cls.user = cls.collection.user

    def test_get(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(f"/collection/{self.collection.id}/create")
        assert response.status_code == 200

    def test_post(self):
        client = Client()
        client.force_login(self.user)
        data = {"name": "Test flashdeck", "description": "-"}
        response = client.post(f"/collection/{self.collection.id}/create", data)
        assert response.status_code == 302
        assert response.url == f"/collection/{self.collection.id}"

    def test_post_no_data(self):
        client = Client()
        client.force_login(self.user)
        response = client.post(f"/collection/{self.collection.id}/create", {})
        assert response.status_code == 200

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()


class TestViewFlashCardDeck(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.flashcard_deck = FlashCardDeckFactory.create()
        cls.user = cls.flashcard_deck.collection.user

    def test_get(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(
            f"/collection/{self.flashcard_deck.collection.id}/flashcards/{self.flashcard_deck.id}"
        )
        assert response.status_code == 200

    def test_post(self):
        client = Client()
        client.force_login(self.user)
        data = {"form-0-answer": "answer", "form-0-question": "question"}
        response = client.get(
            f"/collection/{self.flashcard_deck.collection.id}/flashcards/{self.flashcard_deck.id}",
            data,
        )
        assert response.status_code == 200

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()


class TestDeleteFlashCard(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.flashcard = FlashCardFactory.create()
        cls.user = cls.flashcard.deck.collection.user

    def test_post(self):
        client = Client()
        client.force_login(self.user)
        data = {"flashcard_id": self.flashcard.id}
        response = client.post("/delete_flashcard", data)
        assert response.status_code == 200

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()


class TestDeleteFlashCardDeck(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.deck = FlashCardDeckFactory.create()
        cls.user = cls.deck.collection.user

    def test_get(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(f"/collection/{self.deck.collection.id}/flashcards/{self.deck.id}")
        assert response.status_code == 200

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
