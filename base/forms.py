from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    # meta data will come from Room Class and it will bring room names and etc in order to choose
    class Meta:
        model = Room
        fields = '__all__'

        #which selection shouldnot be in the form
        exclude = ['host','participants']
        #['name','field']
        

    