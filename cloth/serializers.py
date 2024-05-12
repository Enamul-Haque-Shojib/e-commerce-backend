from rest_framework import serializers
from . import models

class ClothSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False)
    category = serializers.StringRelatedField(many=False)
    color = serializers.StringRelatedField(many=True)
    Size = serializers.StringRelatedField(many=True)
    class Meta:
        model = models.Cloth
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Color
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Size
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

 



class ClothWishListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False)
    category = serializers.StringRelatedField(many=False)
    # color = serializers.StringRelatedField(many=True)
    # Size = serializers.StringRelatedField(many=True)
    class Meta:
        model = models.ClothWishList
        fields = '__all__'

class ClothCartListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False)
    category = serializers.StringRelatedField(many=False)
    color = serializers.StringRelatedField(many=True)
    Size = serializers.StringRelatedField(many=True)
    class Meta:
        model = models.ClothCartList
        fields = '__all__'





class ReviewSerializer(serializers.ModelSerializer):
    cloth = serializers.StringRelatedField(many=False)
    author = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Review
        fields = '__all__'


    
