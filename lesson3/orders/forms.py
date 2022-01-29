from django import forms

from orders.models import Order


class OrderForm(forms.Form):
    COUNTRIES = (
        ('russia', 'Россия'),
        ('united_states', 'Англия'),
    )

    REGIONS = (
        ('moscow_region', 'Московская область'),
        ('krasnodar_region', 'Краснодарский край'),
    )

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'value': 'Иван'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'value': 'Иванов'}), required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'value': 'you@example.com'}), required=True)
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'value': 'ул. Мира, дом 6'}), required=True)
    country = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control'}), choices=COUNTRIES)
    region = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control'}), choices=REGIONS)
    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'}), required=True)
