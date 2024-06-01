from django.forms import ModelForm


from .models import Notes,Contact


class NoteForm(ModelForm):
    class Meta:
        model = Notes
        fields = ['branch', 'notesfile', 'filetype' ,'description']
class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['notesfile','name','description','phone']