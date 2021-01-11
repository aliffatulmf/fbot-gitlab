from django import forms
from robot import models
from django.core.validators import FileExtensionValidator


class ChromeProfileForm(forms.ModelForm):
    class Meta:
        model = models.ChromeProfile
        fields = '__all__'


class CSVCollectionForm(forms.ModelForm):
    path = forms.FileField(label='path',
                           required=True,
                           validators=[FileExtensionValidator(['csv'])])

    class Meta:
        model = models.CSVCollection
        fields = '__all__'
