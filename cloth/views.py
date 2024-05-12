from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework import viewsets, filters, pagination
from rest_framework.views import APIView
# Create your views here.
from . import models

from . import serializers
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.response import Response
from rest_framework import generics
import stripe


class ClothViewSet(viewsets.ModelViewSet):
    queryset = models.Cloth.objects.all()
    serializer_class = serializers.ClothSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'price', 'color__name', 'Size__name', 'category__name']
    ordering_fields = ['Size__name', 'rating', 'price']


class ColorViewSet(viewsets.ModelViewSet):
    queryset = models.Color.objects.all()
    serializer_class = serializers.ColorSerializer

class SizeViewSet(viewsets.ModelViewSet):
    queryset = models.Size.objects.all()
    serializer_class = serializers.SizeSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer



class ClothWishListFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, query_set, view):
        u = request.user 
        if u:
            return query_set.filter(author = u)
        return query_set

class ClothWishListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.ClothWishList.objects.all()
    serializer_class = serializers.ClothWishListSerializer
    filter_backends = [ClothWishListFilter]
    

      


class ClothCartListFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, query_set, view):
        u = request.user
        if u:
            return query_set.filter(author = u)
        return query_set

class ClothCartListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.ClothCartList.objects.all()
    serializer_class = serializers.ClothCartListSerializer
    filter_backends = [ClothCartListFilter] 
    

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer



class ClothWishListView(APIView):
    def post(self, request):
        author = request.data.get('author')
        userAuth=None
        for auth in models.User.objects.all():
            if auth.username == author:
                userAuth = auth
                break
        wlist=[]
        wishlist = models.ClothWishList.objects.filter(author = userAuth)
        for wish in wishlist:
            wlist.append(serializers.ClothWishListSerializer(wish).data)
        print('>>>>>>>',wlist)
        return Response(wlist)


class ClothWishListAddView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        author = request.data.get('author')
        cloth = models.Cloth.objects.get(clothid = product_id)
        clothAuthor=None
        userAuth=None
        for auth in models.User.objects.all():
            if auth.username == author:
                userAuth = auth
                break
                # print('>',userAuth)
        for clothw in models.ClothWishList.objects.all():
            if author == clothw.author.username:
                clothAuthor = clothw.author
                break
        
        if clothAuthor == None:
            print('Not found')
            cloth_wishlist = models.ClothWishList()
            cloth_wishlist.clothid = cloth.clothid
            cloth_wishlist.name = cloth.name
            cloth_wishlist.price = cloth.price
            cloth_wishlist.description = cloth.description
            cloth_wishlist.category = cloth.category
            cloth_wishlist.rating = cloth.rating
            cloth_wishlist.author = userAuth
            cloth_wishlist.image = cloth.image
            cloth_wishlist.quantity = cloth.quantity
                    
            cloth_wishlist.save()

            # cloth_wishlist.Size.add(cloth)
            # cloth_wishlist.color.add(cloth)

            cloth_wishlist.save()

        else:
            # print(clothAuthor)
            check_in_cloth_wishlist = models.ClothWishList.objects.filter(clothid = cloth.clothid, name = cloth.name, author = clothAuthor)
            print(check_in_cloth_wishlist)
            if check_in_cloth_wishlist:
                return Response('You have already added')
            else:
                # print('>---------',userAuth)
                cloth_wishlist = models.ClothWishList()
                cloth_wishlist.clothid = cloth.clothid
                cloth_wishlist.name = cloth.name
                cloth_wishlist.price = cloth.price
                cloth_wishlist.description = cloth.description
                cloth_wishlist.category = cloth.category
                cloth_wishlist.rating = cloth.rating
                cloth_wishlist.author = userAuth
                    
                cloth_wishlist.image = cloth.image
                cloth_wishlist.quantity = cloth.quantity
                    

                cloth_wishlist.save()

                # cloth_wishlist.Size.add(cloth)
                # cloth_wishlist.color.add(cloth)

                cloth_wishlist.save()
        
        return Response({'message': 'Data received successfully'})
    
class ClothCartListAddView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        author = request.data.get('author')
        quan = request.data.get('quan')
        print('>>>>>cart>>>>>>',product_id, author, quan)
        cloth = models.Cloth.objects.get(clothid = product_id)
        clothAuthor=None
        userAuth=None
        for auth in models.User.objects.all():
            if auth.username == author:
                userAuth = auth
                break
                # print('>',userAuth)
        for clothc in models.ClothCartList.objects.all():
            if author == clothc.author.username:
                clothAuthor = clothc.author
                break

        if clothAuthor == None:
            print('Not found')
            x = models.ClothCartList()
            x.clothid = cloth.clothid
            x.name = cloth.name
            x.price = cloth.price
            x.quantity = 1
            x.description = cloth.description
            x.category = cloth.category
            x.author = userAuth
            x.image = cloth.image
            x.rating = cloth.rating
            cloth.quantity = cloth.quantity - 1
            x.save()
            cloth.save()

        else:
            # print(clothAuthor)
            check_in_cloth_cartlist = models.ClothCartList.objects.filter(clothid = cloth.clothid, name = cloth.name, author = clothAuthor)
            # print(check_in_cloth_cartlist)
            if check_in_cloth_cartlist:
                if cloth.quantity != 0:
                    s = models.ClothCartList.objects.get(clothid = cloth.clothid, name = cloth.name, author=userAuth)
                    cloth.quantity = cloth.quantity-1
                    s.quantity = s.quantity + 1
                    s.price = s.price + cloth.price
                cloth.save()
                s.save()
            else:
                x = models.ClothCartList()
                x.clothid = cloth.clothid
                x.name = cloth.name
                x.price = cloth.price
                x.quantity = 1
                x.description = cloth.description
                x.category = cloth.category
                x.author = userAuth
                x.image = cloth.image
                x.rating = cloth.rating
                cloth.quantity = cloth.quantity - 1
                x.save()
                cloth.save()
        
        
        return Response({'message': 'Data received successfully'})
    

class ClothCartListView(APIView):
    def post(self, request):
        author = request.data.get('author')
        userAuth=None
        for auth in models.User.objects.all():
            if auth.username == author:
                userAuth = auth
                break
        clist=[]
        cartlist = models.ClothCartList.objects.filter(author = userAuth)
        for cart in cartlist:
            clist.append(serializers.ClothCartListSerializer(cart).data)
        # print('>>>>>>>',clist)
        return Response(clist)
    


class ClothReviewAddView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        product_name = request.data.get('product_name')
        author = request.data.get('author')
        cloth_review = request.data.get('body')
        cloth_ratings = request.data.get('ratings')
        userAuth=None
        for auth in models.User.objects.all():
            if auth.username == author:
                userAuth = auth
                break
        clothnm=None
        for cloth in models.Cloth.objects.all():
            if cloth.clothid == product_id:
                clothnm = cloth

        # print('>>>>>>>>', userAuth, clothnm)

        clothReview = models.Review()
        clothReview.cloth = clothnm
        clothReview.author = userAuth
        clothReview.body = cloth_review
        clothReview.rating = cloth_ratings
        clothReview.save()

        count_rating=0
        review_model = models.Review.objects.filter(cloth = clothnm)
        total_reviews = len(review_model)
        for rev in review_model:
            # print('>>>>',rev.rating)
            count_rating = count_rating + int(rev.rating)
        avg_rating = count_rating/total_reviews
        clothrating = format(avg_rating, ".1f")
        clothnm.rating = clothrating
        clothnm.save()




        clothRev=None
        for rev in models.Review.objects.all():
            if product_name == rev.cloth.name:
                clothRev = rev
                # print('>>>>>>>>>',rev.cloth.name)

        revlist=[]
        reviewlist = models.Review.objects.filter(cloth = clothRev.cloth)
        # print('>>>>>>>>>>>----------',reviewlist)
        for revw in reviewlist:
            revlist.append(serializers.ReviewSerializer(revw).data)
        # print('>>>>>>>................',revlist)

        return Response({'reviewlist':revlist, 'rating': clothrating})
    

class ClothReviewView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        product_name = request.data.get('product_name')
        author = request.data.get('author')
        # print(product_id, product_name, author)
        clothRev=None
        for rev in models.Review.objects.all():
            if product_name == rev.cloth.name:
                clothRev = rev
                # print('>>>>>>>>>',rev.cloth.name)

        
        revlist=[]
        if clothRev == None:
            return Response(revlist)
        reviewlist = models.Review.objects.filter(cloth = clothRev.cloth)
        # print('>>>>>>>>>>>----------',reviewlist)
        for revw in reviewlist:
            revlist.append(serializers.ReviewSerializer(revw).data)
        # print('>>>>>>>................',revlist)

        return Response(revlist)
    

class ClothCartListAddMinusView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        author = request.data.get('author')
        # quan = request.data.get('quan')

        cloth = models.Cloth.objects.get(clothid = product_id)
        for auth in models.User.objects.all():
            if auth.username == author:
                userAuth = auth
                break
        cloth_cartlist = models.ClothCartList.objects.get(clothid = cloth.clothid, name = cloth.name, author = userAuth)
        # print('>>>>>>>>>>>>>>',cloth_cartlist.quantity)
        if cloth_cartlist.quantity > 0:
            cloth.quantity = cloth.quantity+ 1 
            clothQuantity = cloth_cartlist.quantity - 1
            cloth_cartlist.quantity = clothQuantity
            clothPrice = cloth_cartlist.price - cloth.price
            cloth_cartlist.price = clothPrice
                    
            cloth.save()
            cloth_cartlist.save()
        else:
            return Response('No quantity')


        return Response({'Minus':clothPrice, 'Quantity': clothQuantity})
    
class ClothCartListAddPlusView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        author = request.data.get('author')
        # quan = request.data.get('quan')

        cloth = models.Cloth.objects.get(clothid = product_id)
        for auth in models.User.objects.all():
            if auth.username == author:
                userAuth = auth
                break
        cloth_cartlist = models.ClothCartList.objects.get(clothid = cloth.clothid, name = cloth.name, author = userAuth)
        # print('>>>>>>>>>>>>>>',cloth_cartlist.quantity)
        if cloth.quantity != 0:
            cloth.quantity = cloth.quantity - 1
            clothQuantity = cloth_cartlist.quantity + 1
            cloth_cartlist.quantity = clothQuantity
            clothPrice = cloth_cartlist.price + cloth.price
            cloth_cartlist.price = clothPrice
                    
            cloth.save()
            cloth_cartlist.save()
        else:
            return Response('Out of Stock')


        return Response({'Plus':clothPrice, 'Quantity': clothQuantity})
    

class ClothCartListDeleteView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        author = request.data.get('author')
        models.ClothCartList.objects.get(id = product_id).delete()
        return Response('Cart Delete')
    



import environ
env = environ.Env()
environ.Env.read_env()


stripe.api_key = env("API_KEY")


API_URL = 'http://127.0.0.1:8000'
def fun(cart): 
    # print('>>>>>>>>>', cart['image'])
    return {
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': cart['name'],
        #   'images': f"http://127.0.0.1:8000/{cart['image']}/",
        },
        'unit_amount': (cart['price'] * 100)//cart['quantity'],
      },
      'quantity': cart['quantity'],
    }
class ClothCartListCheckOutView(APIView):
    def post(self, request):
        cartList = request.data.get('clothList')
        author = request.data.get('author')

        items = map(fun, cartList)
    
        # for i in cartList:
        #     print(i)

        line_items = list(items)



        session = stripe.checkout.Session.create(
            line_items=line_items, 
  
    mode='payment',
    success_url='http://localhost:5173/success',
    cancel_url='http://localhost:5173/cartlist',
    # cancel_url='http://localhost:5173/cencale',
  )
        # return redirect(session.url, code=303)
        return Response({'url': session.url})
    




    
class ClothWishListDeleteView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        author = request.data.get('author')
        models.ClothWishList.objects.get(id = product_id).delete()
        return Response('Wish Delete')
    










# class ClothCardListDeleteView(generics.DestroyAPIView):
#     queryset = models.ClothCartList.objects.all()
#     serializer_class = serializers.ClothCartListSerializer

    


# class ClothWishListDeleteView(generics.DestroyAPIView):
#     queryset = models.ClothWishList.objects.all()
#     serializer_class = serializers.ClothWishListSerializer
    









    









    

