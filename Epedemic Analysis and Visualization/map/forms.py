from django import forms
from django.contrib.auth.models import User
from map.models import UserProfileInfo , Parameters


class UserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))

	class Meta():
		model = User
		fields = ('username','email','password')



class UserProfileInfoForm(forms.ModelForm):
	portfolio_site = forms.URLField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'website url'}))

	class Meta():
		model = UserProfileInfo
		fields = ('portfolio_site','profile_pic')


# ================== Parameter form ======================


class ParameterForm(forms.ModelForm):

	class Meta():
		model = Parameters
		fields = '__all__'
		 

