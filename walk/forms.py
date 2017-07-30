''' forms for walk  '''
from django import forms
from .models import Algorithm, Comment

class RandWalkForm(forms.Form):
    steps = forms.CharField(label='number of steps',max_length=5)

class SelfAvoidForm(forms.Form):
    samples = forms.CharField(label='number of samples',max_length=5)
    steps = forms.CharField(label='number of steps',max_length=5)	

class AlgorithmForm(forms.ModelForm):
    class Meta:
        model=Algorithm
        fields=['text']
        labels={'text':''}		

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text':''}
        widgets = {'text': forms.Textarea(attrs={'cols':80})}
		