from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Products,Carts,Reviews
from api.serializers import ProductsSerializers,ProductModelSerializer,UserSerializer,CartsSerialiser,ReviewSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions






class ProductsView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Products.objects.all()
        serializer=ProductsSerializers(qs,many=True)
        return Response(data=serializer.data)

    def post(self,request,*args,**kwargs):
        serializer=ProductsSerializers(data=request.data)
        if serializer.is_valid():
            Products.objects.create(**serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class ProductDetailsView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Products.objects.get(id=id)
        serializer=ProductsSerializers(qs,many=False)
        return Response(data=serializer.data)

    def put(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Products.objects.filter(id=id).update(**request.data)
        qs=Products.objects.get(id=id)
        serializer=ProductsSerializers(qs,many=False)
        return Response(data=serializer.data)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get('id')
        Products.objects.get(id=id).delete()
        return Response(data="object deleted")


class ProductViewSetView(viewsets.ModelViewSet):

    serializer_class = ProductModelSerializer
    queryset = Products.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    # def list(self,request,*args,**kwargs):
    #     qs=Products.objects.all()
    #     serialiser=ProductModelSerializer(qs,many=True)
    #
    #     return Response(data=serialiser.data)
    
    # def create(self,request,*args,**kwargs):
    #     serialiser=ProductModelSerializer(data=request.data)
    #     if serialiser.is_valid():
    #         serialiser.save()
    #         return Response(data=serialiser.data)
    #     else:
    #         return Response(data=serialiser.errors)
    #
    # def retrieve(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     qs=Products.objects.get(id=id)
    #     serialiser=ProductModelSerializer(qs,many=False)
    #
    #     return Response(data=serialiser.data)
    #
    # def update(self,request,*args,**kwargs):
    #    id=kwargs.get("pk")
    #    obj=Products.objects.get(id=id)
    #    serialiser=ProductModelSerializer(data=request.data,instance=obj)
    #    if serialiser.is_valid():
    #        serialiser.save()
    #        return Response(data=serialiser.data)
    #    else:
    #        return Response(data=serialiser.errors)
    #
    # def destroy(self,request,*args,**kwargs):
    #     id=kwargs.get("pk")
    #     Products.objects.get(id=id).delete()
    #
    #     return Response(data='objects deleted')


    @action(methods=["GET"],detail=False)
    def categories(self,request,*args,**kwargs):
        res=Products.objects.values_list('category',flat=True).distinct()
        return Response(data=res)


    @action(methods=["POST"],detail=True)
    def addto_cart(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        item=Products.objects.get(id=id)
        user=request.user
        user.carts_set.create(product=item)
        #or
        #Carts.objects.create(user=user,product=item)
        return Response(data="item added to cart")

    @action(methods=['POST'],detail=True)
    def add_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        item=Products.objects.get(id=id)
        user=request.user
        serialiser=ReviewSerializer(data=request.data)
        if serialiser.is_valid():
            serialiser.save(product=item,user=user)
            return Response(data=serialiser.data)
        else:
            return Response(data=serialiser.errors)
    @action(methods=["GET"],detail=True)
    def reviews(self,request,*args,**kwargs):
        item=self.get_object()
        qs=item.reviews_set.all()
        #or
        #id=kwargs.get("pk")
        #item=Products.objects.get(id=id)
        serializer=ReviewSerializer(qs,many=True)
        return Response(data=serializer.data)



class UsersView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # def create(self,request,*args,**kwargs):
    #     serialiser=UserSerializer(data=request.data)
    #     if serialiser.is_valid():
    #         serialiser.save()
    #         return Response(data=serialiser.data)
    #     else:
    #         return Response(serialiser.errors)

class CartsView(viewsets.ModelViewSet):
    serializer_class = CartsSerialiser
    queryset = Carts.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user)
        #or
        #return self.reuest.user.carts_set.all()


    # def list(self,request,*args,**kwargs):
    #     qs=request.user.carts_set.all()
    #     serialiser=CartsSerialiser(qs,many=True)
    #
    #     return Response(data=serialiser.data)
    #

class ReviewDeleteReview(APIView):
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Reviews.objects.filter(id=id).delete()
        return  Response(data="review deleted")