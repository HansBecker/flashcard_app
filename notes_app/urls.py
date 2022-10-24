"""notes_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import LoginView
from main.views import (
    HomeView,
    CreateFlashDeckView,
    CreateCollectionView,
    CollectionDetailView,
    DeleteFlashCard,
    ViewFlashCardDeck,
    DeleteFlashCardDeck,
    PracticeFlashcards,
    DeleteCollectionView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", LoginView.as_view(), name="login"),
    path("home/", HomeView.as_view(), name="home"),
    path("create_collection", CreateCollectionView.as_view(), name="create-collection"),
    path(
        "delete_collection/<int:pk>",
        DeleteCollectionView.as_view(),
        name="delete-collection",
    ),
    path(
        "collection/<int:collection_id>/create",
        CreateFlashDeckView.as_view(),
        name="create",
    ),
    path(
        "collection/<int:collection_id>",
        CollectionDetailView.as_view(),
        name="collection-detail",
    ),
    path(
        "collection/<int:collection_id>/flashcards/<int:deck_id>",
        ViewFlashCardDeck.as_view(),
        name="collection-view-flashcards",
    ),
    path(
        "collection/<int:collection_id>/flashcards/<int:deck_id>/practice",
        PracticeFlashcards.as_view(),
        name="collection-practice-flashcards",
    ),
    path(
        "collection/<int:collection_id>/flashcards/<int:deck_id>/delete",
        DeleteFlashCardDeck.as_view(),
        name="collection-delete-deck",
    ),
    path("delete_flashcard", DeleteFlashCard.as_view(), name="delete-flashcard"),
]
