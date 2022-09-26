from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 
 
 
class SignUpForm(UserCreationForm): 
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs.update({ 
            'class': 'mdl-textfield__input is-invalid', 
            'required':'', 
            'name':'username', 
            'id':'username', 
            'type':'text',  
            
            }) 
        self.fields['email'].widget.attrs.update({ 
            'class': 'mdl-textfield__input is-invalid', 
            'required':'', 
            'name':'email', 
            'id':'email', 
            'type':'email', 
            }) 
        self.fields['password1'].widget.attrs.update({ 
            'class': 'mdl-textfield__input is-invalid', 
            'required':'', 
            'name':'password1', 
            'id':'password1', 
            'type':'password',
         
            }) 
        self.fields['password2'].widget.attrs.update({ 
            'class': 'mdl-textfield__input is-invalid', 
            'required':'', 
            'name':'password2', 
            'id':'password2', 
            'type':'password',
           
            }) 
 
 
    # username = forms.CharField(widget=forms.TextInput(attrs={'class': 'mdl-textfield__input'}))
    # email = forms.EmailField() 
 
    class Meta: 
        model = User 
        fields = ['username', 'email', 'password1', 'password2' ]