from django.forms import ModelForm
from .models import Room
class RoomsForm(ModelForm):
    class Meta:
        model = Room
        fields  = '__all__'