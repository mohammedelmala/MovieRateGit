from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
# Create your views here.


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny,)

    @action(detail=True,methods=['POST'])
    def rate_movie(self,request,pk=None):
        if "stars" in request.data:
            movie = Movie.objects.get(id=pk)
            # user = User.objects.get(id=1)
            user = request.user
            stars = request.data['stars']
            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating,many=False)
                response = {"message": "Rating Updated Successfully", "result": serializer.data}
                return Response(data=response, status=status.HTTP_200_OK)
            except:
                print("Create Rating")
                rating = Rating.objects.create(user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {"message": "Rating Created Successfully", "result": serializer.data}
                return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {"message": "stars not found"}
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def get_title(self,request,pk=None):
        try:
            movie = Movie.objects.get(id=pk)
            title = movie.title
            response = {"message": "Movie found","result":{"title": title}}
            return Response(data=response,status=status.HTTP_200_OK)
        except:
            response = {"message": "movie does not exist"}
            return Response(data=response,status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)