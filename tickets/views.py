from .models import Guest , Movie , Reservation
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import GuestSerializer , MovieSerializer , ReservationSerializer
from rest_framework import status
from rest_framework import filters 
from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# Function Based Views
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

#Class Based Views
from rest_framework.views import APIView  # import APIVIEW 
from django.http import Http404
class list_create_guest(APIView):
    def get(self,request):
        guests=Guest.objects.all()
        serializer=GuestSerializer(guests , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    def post(self, request):
        serializer=GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
CBV_guest=list_create_guest.as_view()

class get_update_delete(APIView):
    def get_object(self,pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
        
    def get( self,request , pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest)
        return Response(serializer.data , status=status.HTTP_200_OK)
    def put( self,request ,pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest ,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(serializer.data , status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        guest=self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)
get_guest=get_update_delete.as_view()



# using mixins 
# import generics , mixins
from rest_framework import generics , mixins
 
class mixins_list(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)
class mixins_pk(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk=None):
        return self.retrieve(request, pk=pk)

    def put(self, request, pk=None):
        return self.update(request, pk=pk)

    def delete(self, request, pk=None):
        return self.destroy(request, pk=pk)


#  using generics import generics


class generics_list(generics.ListCreateAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    
class geneerics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    
# using viewsets
from rest_framework import viewsets
class guest_viewset(viewsets.ModelViewSet):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    authentication_classes=[TokenAuthentication]
class movie_viewset(viewsets.ModelViewSet):
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer
    filter_backend=[filters.SearchFilter]
    search_fields=['movie']
    authentication_classes=[TokenAuthentication]
class reservation_viewset(viewsets.ModelViewSet):
    queryset=Reservation.objects.all()
    serializer_class=ReservationSerializer
    authentication_classes=[TokenAuthentication]
@api_view(["GET"])
def search(request):
    movie_name = request.data.get('movie')
    if not movie_name:
        return Response({"error": "'movie' parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
   
    movies = Movie.objects.filter(movie=movie_name)
    if movies.exists():
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)        
@api_view(["POST"])
def new_reservation(request):
    movie_title = request.data.get('movie')
    hall = request.data.get('hall')
    name = request.data.get('name')
    phone_number = request.data.get('phone_number')
    if not all([movie_title, hall, name, phone_number]):
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        movie = Movie.objects.get(movie=movie_title, hall=hall)
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found with the given title and hall."}, status=status.HTTP_404_NOT_FOUND)
    guest = Guest(name=name, phone_number=phone_number)
    guest.save()
    reservation = Reservation(movie=movie, guest=guest)
    reservation.save()
    serializer = ReservationSerializer(reservation)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

    
# @api_view(["POST"])
# def new_reservation(request):
#     movie= request.data.get('movie')
#     hall= request.data.get('hall')
#     movie=Movie.objects.get(movie=movie,hall=hall)
#     guest=Guest()
#     guest.name=request.data.get('name')
#     guest.phone_number=request.data.get('phone_number')
#     guest.save()
#     reservation=Reservation()
#     reservation.movie=movie
#     reservation.guest=guest
#     reservation.save()
#     return Response(status=status.HTTP_201_CREATED)
    
    