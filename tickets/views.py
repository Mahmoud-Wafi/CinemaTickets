from .models import Guest , Movie , Reservation
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import GuestSerializer , MovieSerializer , ReservationSerializer
from rest_framework import status
@api_view(["GET","POST"])
def guest_list_create(request):
    if request.method=="GET":
        queryset=Guest.objects.all()
        serializer= GuestSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    if request.method=="POST":
        serializer=GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.data , status=status.HTTP_400_BAD_REQUEST)
@api_view(["GET", "PUT", "DELETE"])
def get_update_delete_guest(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = GuestSerializer(guest)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        guest.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)

