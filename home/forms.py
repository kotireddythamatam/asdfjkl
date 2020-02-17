from django import forms
from .models import User_Registration_Model,Profile

class User_Registration_Form(forms.ModelForm):
    class Meta:
        model =User_Registration_Model
        fields = ['first_name','last_name','email','username','password']

class User_Login_Form(forms.Form):
	email = forms.EmailField()
	password = forms.CharField()

class Profile_Form(forms.ModelForm):
	class Meta:
		model = Profile
		fields = "__all__"