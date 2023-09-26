from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer


@api_view(['GET'])
#view to show all routes, links of the API
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]

    #safe means we can use more than python dictionary in the object that we refer - 
    ## so it s not dict. but JsonREsponse will change it to the JSon
    return Response(routes)


#python object - list can not be viewed as json file , need to serialize it
@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    #multiple objects that we serialize - many=True
    serializer = RoomSerializer(rooms, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id = pk)
    #oen room will be viewed - many=False
    serializer = RoomSerializer(room, many = False)
    return Response(serializer.data)