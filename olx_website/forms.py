from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.forms import CharField
from olx_website import models
from olx_website.models import Profile

class SignUpForm(UserCreationForm):
    phone_number = CharField(label='Enter your phone number')

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'password1', 'password2']

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        result = super().save(commit)
        phone_number = self.cleaned_data['phone_number']
        profile = Profile(phone_number=phone_number, user=result)
        if commit:
            profile.save()
        return result

class LogginForm(AuthenticationForm):
    username = forms.CharField
    password = forms.CharField


class AddNewItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = ('title','image', 'condition', 'price', 'description', 'category' )
    #image = forms.ImageField()


class EditItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = ('title','image', 'condition', 'price', 'description', 'category')


class ChatMessage(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = ('content',)