from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User



class RoomForm(ModelForm):
    # meta data will come from Room Class and it will bring room names and etc in order to choose
    class Meta:
        model = Room
        fields = '__all__'

        #which selection shouldnot be in the form
        exclude = ['host','participants']
        #['name','field']
        

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email']
