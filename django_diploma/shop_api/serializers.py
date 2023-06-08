from rest_framework import serializers

from .models import Avatar, Profile, Category


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
