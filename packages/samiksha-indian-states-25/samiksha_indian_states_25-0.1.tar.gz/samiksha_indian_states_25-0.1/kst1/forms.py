from django.db import forms
from .states import INDIAN_STATES

class StateSelect(forms.Select):
	def__init__(self,attrs=None)
		super().__init__(attrs,choices=INDIAN_STATES)
