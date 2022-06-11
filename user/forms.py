from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserForm(forms.ModelForm):
    '''
        Form Definition for User
    '''

    class Meta:
        '''
            Meta definition for UserForm
        '''
        model = User
        fields = '__all__'

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user
