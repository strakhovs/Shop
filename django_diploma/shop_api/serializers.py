from django.db.models import Avg
from rest_framework import serializers
from .models import Avatar, Profile, Category, Tag, Product, Review, Specification, Order


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
        return model.name

    def get_alt(self, model):
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

    def get_tags(self, obj):
        item = obj.tags.all()
        serializer = TagsSerializer(item, many=True)
        return serializer.data

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

    def get_specs(self, obj):
        specs = obj.specifications.all()
        serializer = SpecsSerializer(specs, many=True)
        return serializer.data

    def get_rating(self, obj):
        return obj.review_set.all().aggregate(Avg("rate"))


class CartSerializer(ProductSerializer):
    count = serializers.SerializerMethodField(method_name='get_count')
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

    def get_count(self, obj):
        data = self.context
        for i in data:
            count = i['count']
            if next(iter(i.values())) == obj.id:
                return count

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


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(method_name='get_products')

    class Meta:
        model = Order
        fields = ['id',
                  'createdAt',
                  'fullName',
                  'email',
                  'phone',
                  'deliveryType',
                  'paymentType',
                  'totalCost',
                  'status',
                  'city',
                  'address',
                  'products']

    def get_products(self, obj):
        order_products = obj.orderproducts_set.all().values('product_id', 'count')
        products_ids = obj.orderproducts_set.all().values('product')
        products = Product.objects.filter(id__in=products_ids)
        serializer = CartSerializer(products, context=order_products, many=True)
        return serializer.data

    def save(self, instance, validated_data):
        instance.fullName = validated_data.get('fullName', instance.fullName)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.deliveryType = validated_data.get('deliveryType', instance.deliveryType)
        instance.paymentType = validated_data.get('paymentType', instance.paymentType)
        instance.totalCost = validated_data.get('totalCost', instance.totalCost)
        instance.status = 'confirmed'
        instance.city = validated_data.get('city', instance.city)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance


class SalesSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(method_name='get_images')

    class Meta:
        model = Product
        fields = ['id',
                  'price',
                  'salePrice',
                  'dateFrom',
                  'dateTo',
                  'title',
                  'images']

    def get_images(self, obj):
        images = obj.image_set.all()
        result = []
        for image in images:
            result.append({'src': image.image.url,
                           'alt': image.alt})
        return result
