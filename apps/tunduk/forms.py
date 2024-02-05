from django import forms
from django.core.exceptions import ValidationError


class InfocomForm(forms.Form):
    inn = forms.CharField(label='ИНН', widget=forms.TextInput(
        attrs={
            "placeholder": "Введите инн",
            "class": "form-group",
        }
    ))
    passport_series = forms.CharField(label='Серия паспорта', widget=forms.TextInput(
        attrs={
            "placeholder": "Введите номер паспорта",
            "class": "form-group",
        }
    ))
    passport_number = forms.CharField(label='Номер паспорта', widget=forms.TextInput(
        attrs={
            "placeholder": "Введите инн",
            "class": "form-group",
        }
    ))


class INNForm(forms.Form):
    inn = forms.CharField(label='ИНН', widget=forms.TextInput(
        attrs={
            "placeholder": "Введите ИНН",
            "class": "form-group",
        }
    ))


class ENICodeForm(forms.Form):
    eni_code = forms.CharField(label='Код ЕНИ', widget=forms.TextInput(
        attrs={
            "placeholder": "Введите код ЕНИ",
            "class": "form-group",
        }
    ))

    def clean(self):
        super().clean()

        if eni_code := self.cleaned_data.get('eni_code'):
            self.cleaned_data['eni_code'] = eni_code.replace('-', '')

        if not self.cleaned_data['eni_code'].isdigit():
            raise ValidationError('Введите только цифры')

        return self.cleaned_data


