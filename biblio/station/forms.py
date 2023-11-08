from django import forms
from .models import Reader, Book
class IssueBookForm(forms.Form):
    reader = forms.ModelChoiceField(queryset=Reader.objects.all(), label='Читатель')
    book = forms.ModelChoiceField(queryset=Book.objects.filter(status='available'), label='Книга')

    def __init__(self, *args, **kwargs):
        super(IssueBookForm, self).__init__(*args, **kwargs)
        # Определите, какие книги доступны для выдачи и обновите queryset для поля 'book'.
        self.fields['book'].queryset = Book.objects.filter(status='available')


class ReturnBookForm(forms.Form):
    reader = forms.ModelChoiceField(queryset=Reader.objects.all(), label='Читатель')
    book = forms.ModelChoiceField(queryset=Book.objects.filter(status='checked_out'), label='Книга')

    def __init__(self, *args, **kwargs):
        super(ReturnBookForm, self).__init__(*args, **kwargs)
        # Определите, какие книги можно вернуть и обновите queryset для поля 'book'.
        self.fields['book'].queryset = Book.objects.filter(status='checked_out')

class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ['user', 'last_name', 'first_name', 'birth_date']