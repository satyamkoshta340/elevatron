from django import forms
from .models import ElevatorSystem

class ElevatorSystemForm( forms.ModelForm ):
    class Meta:
        model = ElevatorSystem
        fields = '__all__'