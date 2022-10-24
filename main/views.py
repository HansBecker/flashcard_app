from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import FlashCardFormset, CollectionForm, FlashCardDeckForm
from .models import FlashCard, FlashCardDeck, FlashCardCollection


class HomeView(LoginRequiredMixin, View):
    template_name = "main/home.html"

    def get(self, request, *args, **kwargs):
        """
        Return overview of FlashCardCollection objects. First view after login.
        """
        context = {"collections": FlashCardCollection.objects.filter(user=request.user)}
        return render(request, self.template_name, context)


class CollectionDetailView(LoginRequiredMixin, View):
    template_name = "main/collection_detail.html"

    def get(self, request, *args, **kwargs):
        """
        Shows the FlashCardDeck objects in a FlashCardCollection
        """
        collection_id = kwargs["collection_id"]
        flashcard_decks = FlashCardDeck.objects.filter(
            collection_id=collection_id, collection__user=request.user
        )
        for deck in flashcard_decks:
            deck.count = FlashCard.objects.filter(deck=deck).count()

        context = {
            "collection": FlashCardCollection.objects.get(id=collection_id),
            "flashcard_decks": flashcard_decks,
        }
        return render(request, self.template_name, context)


class CreateCollectionView(LoginRequiredMixin, View):
    template_name = "main/create_collection.html"
    form = CollectionForm

    def get(self, request, *args, **kwargs):
        """
        Returns the form to create a FlashCardCollection
        """
        context = {"form": self.form()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Validates the FlashCardCollectionForm and creates a new FlashCardCollection
        """
        form = self.form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect("home")
        else:
            context = {"form": form}
            return render(request, self.template_name, context)


class DeleteCollectionView(View):
    def post(self, request, *args, **kwargs):
        FlashCardCollection.objects.get(id=kwargs["pk"]).delete()
        return redirect("home")


class CreateFlashDeckView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "main/create_deck.html"

    def get(self, request, *args, **kwargs):
        """
        View for adding new flashcards to a FlashCardDeck
        """
        context = {
            "form": FlashCardDeckForm(),
            "formset": FlashCardFormset(),
            "collection": FlashCardCollection.objects.get(id=kwargs["collection_id"]),
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Processes the new flashcards
        """
        form = FlashCardDeckForm(request.POST)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.collection_id = kwargs["collection_id"]
            deck.save()
            return redirect("collection-detail", collection_id=kwargs["collection_id"])
        else:
            context = {
                "form": form,
            }
            return render(request, self.template_name, context)

    def test_func(self):
        """
        Checks whether the FlashCardCollection belongs to the user that is request it.
        """
        collection = FlashCardCollection.objects.get(id=self.kwargs["collection_id"])
        if collection.user == self.request.user:
            return True
        else:
            return False


class ViewFlashCardDeck(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "main/flashcard_deck.html"

    def get(self, request, *args, **kwargs):
        """
        View a FlashCardDeck and its related FlashCard objects
        """
        deck_id = kwargs["deck_id"]
        deck = FlashCardDeck.objects.get(id=deck_id)
        flashcards = FlashCard.objects.filter(deck=deck)
        context = {
            "deck": deck,
            "flashcards": flashcards,
            "formset": FlashCardFormset(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Processes new flashcards
        """
        deck_id = kwargs["deck_id"]
        deck = FlashCardDeck.objects.get(id=deck_id)
        formset = FlashCardFormset(request.POST)

        if formset.is_valid():
            new_flashcards = []
            for form in formset:
                new_card = FlashCard(
                    deck=deck,
                    question=form.cleaned_data["question"],
                    answer=form.cleaned_data["answer"],
                )
                new_flashcards.append(new_card)
            FlashCard.objects.bulk_create(new_flashcards)

        context = {
            "deck": deck,
            "flashcards": FlashCard.objects.filter(deck=deck),
            "formset": FlashCardFormset(),
        }
        return render(request, self.template_name, context)

    def test_func(self):
        """
        Checks whether the FlashCardDeck belongs to the logged in user
        """
        deck_id = self.kwargs["deck_id"]
        deck = FlashCardDeck.objects.get(id=deck_id)
        if deck.collection.user == self.request.user:
            return True
        else:
            False


class DeleteFlashCard(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, *args, **kwargs):
        """
        Deletes a FlashCard
        """
        FlashCard.objects.get(id=request.POST["flashcard_id"]).delete()
        return HttpResponse("OK")

    def test_func(self):
        """
        Checks whether the FlashCard object belongs to the logged in user
        """
        flashcard_id = self.request.POST["flashcard_id"]
        flashcard = FlashCard.objects.get(id=flashcard_id)
        if flashcard.deck.collection.user == self.request.user:
            return True
        else:
            return False


class DeleteFlashCardDeck(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        """
        Deletes a FlashCardDeck
        """
        deck_id = kwargs["deck_id"]
        FlashCard.objects.filter(deck_id=deck_id).delete()
        FlashCardDeck.objects.get(id=deck_id).delete()
        redirect("collection-view-flashcards", collection_id=kwargs["collection_id"])

    def test_func(self):
        """
        Checks whether the FlashCardDeck belongs to the logged in user
        """
        deck = FlashCardDeck.objects.get(id=self.kwargs["deck_id"])
        if deck.collection.user == self.request.user:
            return True
        else:
            return False


class PracticeFlashcards(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = "main/practice_flashcards.html"

    def get(self, request, *args, **kwargs):
        """
        Returns a random flashcard
        """
        deck_id = kwargs["deck_id"]
        deck = FlashCardDeck.objects.get(id=deck_id)
        flashcard = FlashCard.objects.filter(deck=deck).order_by("?").first()

        context = {"card": flashcard, "deck": deck}
        return render(request, self.template_name, context)

    def test_func(self):
        """
        Checks whether the FlashCardDeck belongs to the logged in user.
        """
        deck = FlashCardDeck.objects.get(id=self.kwargs["deck_id"])
        if deck.collection.user == self.request.user:
            return True
        else:
            return False
