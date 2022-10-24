from django import forms
from django.forms import formset_factory
from .models import FlashCard, FlashCardCollection, FlashCardDeck


class CollectionForm(forms.ModelForm):
    """
    Form for creating a new FlashCardCollection object
    """

    class Meta:
        model = FlashCardCollection
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["class"] = "form-control"
        self.fields["description"].widget.attrs["class"] = "form-control"


class FlashCardDeckForm(forms.ModelForm):
    """
    Form for creating a new FlashCardDeck
    """

    class Meta:
        model = FlashCardDeck
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super(FlashCardDeckForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["class"] = "form-control"
        self.fields["description"].widget.attrs["class"] = "form-control"


class FlashCardForm(forms.ModelForm):
    """
    Form for creating a new FlashCard. Used as a formset
    to create multiple.
    """

    class Meta:
        model = FlashCard
        fields = ["question", "answer"]


FlashCardFormset = formset_factory(FlashCardForm, max_num=100, extra=0)
