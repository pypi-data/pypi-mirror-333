from django import forms
from .states import INDIAN_STATES

class StateSelect(forms.Select):
    def _init_(self, attrs=None):
        super()._init_(attrs, choices=INDIAN_STATES)