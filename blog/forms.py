from django import forms
from .models import Post, Comment, Reply
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    
    class Meta:
        model = User
        fields = ['username']

    def clean_password(self):
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')   
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError("passoword don't match")
        return pass2
    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False) 
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Username')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')  

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply']