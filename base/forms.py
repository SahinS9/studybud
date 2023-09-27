from django.forms import ModelForm
from .models import Room

# from django.contrib.auth.models import User
## need to import User model from our own models
from .models import User
from django.contrib.auth.forms import UserCreationForm

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
        fields = ['avatar','name','username','email','bio']
