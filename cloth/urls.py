from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views


router = DefaultRouter()

router.register('list', views.ClothViewSet)
router.register('color', views.ColorViewSet)
router.register('size', views.SizeViewSet)
router.register('category', views.CategoryViewSet)
router.register('wishlist', views.ClothWishListViewSet)
router.register('cartlist', views.ClothCartListViewSet)
router.register('reviews', views.ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # path('addwishlist/<int:clothid>', views.clothWishList, name='add_wishlist' ),
    path('addwishlist/', views.ClothWishListAddView.as_view(), name='add_wishlist' ),
    path('clothwishlist/', views.ClothWishListView.as_view(), name='clothwishlist' ),
    path('clothwishlistdelete/', views.ClothWishListDeleteView.as_view(), name='clothwishlist_delete' ),
    path('addcartlist/', views.ClothCartListAddView.as_view(), name='add_cartlist' ),
    path('addcartlistminus/', views.ClothCartListAddMinusView.as_view(), name='add_cartlistMinus' ),
    path('addcartlistplus/', views.ClothCartListAddPlusView.as_view(), name='add_cartlistPlus' ),
    path('cartlistdelete/', views.ClothCartListDeleteView.as_view(), name='cartlist_delete' ),
    path('clothcartlist/', views.ClothCartListView.as_view(), name='clothcartlist' ),
    path('clothcartlistcheckout/', views.ClothCartListCheckOutView.as_view(), name='clothcartlist_checkout' ),
    path('addreview/', views.ClothReviewAddView.as_view(), name='add_review' ),
    path('clothreviews/', views.ClothReviewView.as_view(), name='clothreviews' ),
    
]