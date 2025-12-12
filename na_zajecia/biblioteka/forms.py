from django import forms
from .models import Osoba, Book, Stanowisko

# przykładowy formularz dla modelu Osoba
class OsobaForm(forms.ModelForm):
    class Meta:
        model = Osoba
        fields = ['imie', 'nazwisko', 'plec', 'stanowisko']  # pola do formularza

# Lab 8 (B)
## Zad 2
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'publication_month', 'book_format', 'author', 'genre', 'available_copies']
        
class StanowiskoForm(forms.ModelForm):
    class Meta:
        model = Stanowisko
        fields = ['nazwa', 'opis']