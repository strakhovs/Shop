from django.db.models import Avg
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from .models import Avatar, Profile, Category, Tag, Product, Review, Specification


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['src', 'alt']


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(required=False)

    class Meta:
        model = Profile
        fields = ['fullName', 'email', 'phone', 'avatar']


class CategoryImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()
    alt = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Category
        fields = ['src', 'alt']

    def get_src(self, model):
        print(model.name)
        return model.name

    def get_alt(self, model):
        print('model - ', model)
        return model.name


class CategoriesSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField(method_name='get_subcategories')
    image = serializers.SerializerMethodField(method_name='get_image')
    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'subcategories')

    def get_subcategories(self, obj):
        subcategories = [
            {
                'id': subcategory.id,
                'title': subcategory.title,
                'image': {
                    'src': subcategory.image.url,
                    'alt': 'Subcategory image'
                }
            }
            for subcategory in obj.subcategories.all()
        ]
        return subcategories

    def get_image(self, obj):
        print(obj.image.url)
        return {'src': obj.image.url,
                'alt': 'Category image'}


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name='get_images')
    tags = serializers.SerializerMethodField(method_name='get_tags')
    reviews = serializers.SerializerMethodField(method_name='get_reviews')
    rating = serializers.SerializerMethodField(method_name='get_rating')

    class Meta:
        model = Product
        fields = ['id',
                  'category',
                  'price',
                  'count',
                  'date',
                  'title',
                  'description',
                  'freeDelivery',
                  'images',
                  'tags',
                  'reviews',
                  'rating']

    def get_images(self, obj):
        images = obj.image_set.all()
        result = []
        for image in images:
            result.append({'src': image.image.url,
                           'alt': image.alt})
        return result

    def get_tags(self, obj):
        item = obj.tags.all()
        serializer = TagsSerializer(item, many=True)
        return serializer.data

    def get_reviews(self, obj):
        return obj.review_set.all().count()

    def get_rating(self, obj):
        return obj.review_set.all().aggregate(Avg("rate"))


class CatalogRequestSerializer(serializers.Serializer):
    name = serializers.CharField
    minPrice = serializers.DecimalField
    maxPrice = serializers.DecimalField
    freeDelivery = serializers.BooleanField
    available = serializers.BooleanField


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['author',
                  'email',
                  'text',
                  'rate',
                  'date']


class SpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['name',
                  'value']


class FullProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name='get_images')
    tags = serializers.SerializerMethodField(method_name='get_tags')
    reviews = serializers.SerializerMethodField(method_name='get_reviews')
    specifications = serializers.SerializerMethodField(method_name='get_specs')
    rating = serializers.SerializerMethodField(method_name='get_rating')

    class Meta:
        model = Product
        fields = ['id',
                  'category',
                  'price',
                  'count',
                  'date',
                  'title',
                  'description',
                  'fullDescription',
                  'freeDelivery',
                  'images',
                  'tags',
                  'reviews',
                  'specifications',
                  'rating']

    def get_images(self, obj):
        images = obj.image_set.all()
        result = []
        for image in images:
            result.append({'src': image.image.url,
                           'alt': image.alt})
        return result

        #images = obj.image_set.all()
        #result = []
        #for image in images:
        #    result.append(image.image.url)
        #return result

    def get_tags(self, obj):
        item = obj.tags.all()
        serializer = TagsSerializer(item, many=True)
        return serializer.data
        #tags = obj.tags.all()
        #result = []
        #for tag in tags:
        #    result.append(tag.name)
        #return result

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

    def get_specs(self, obj):
        specs = obj.specifications.all()
        print(specs)
        serializer = SpecsSerializer(specs, many=True)
        return serializer.data

    def get_rating(self, obj):
        return obj.review_set.all().aggregate(Avg("rate"))


