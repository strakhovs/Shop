import io

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from .models import Profile, Avatar, profile_avatar_directory_path, Category, Tag, Product
from .paginators import CustomPaginator
from .serializers import AuthSerializer, RegisterSerializer, ProfileSerializer, AvatarSerializer, CategoriesSerializer, \
    TagsSerializer, ProductSerializer, CatalogRequestSerializer, FullProductSerializer


class SignIn(APIView):
    def post(self, request: Request) -> Response:
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)
        serializer = AuthSerializer(data=data)
        serializer.is_valid()
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = authenticate(
            self.request,
            username=username,
            password=password,)
        if user:
            login(request=self.request, user=user)
            return Response(status=200)
        else:
            return Response(status=401)


class SignUp(APIView):
    def post(self, request: Request) -> Response:
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)
        serializer = RegisterSerializer(data=data)
        serializer.is_valid()
        name = serializer.validated_data.get('name')
        username = serializer.validated_data.get('username')
        password = make_password(serializer.validated_data.get('password'))
        try:
            User.objects.get(username=username)
            return Response(status=401)
        except User.DoesNotExist:
            user = User.objects.create(
                first_name=name,
                username=username,
                password=password,
            )
            profile = Profile.objects.create(user=user, fullName=name)
            Avatar.objects.create(profile_id=profile.pk)
        login(request=self.request, user=user)
        return Response(status=200)


class ProfileView(APIView):
    def get(self, request: Request) -> Response:
        profile = Profile.objects.get(user_id=request.user)
        print(profile)
        serializer = ProfileSerializer(profile)

        data = JSONRenderer().render(serializer.data)
        print(serializer.data)
        print(data)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        print(request.data)
        profile = Profile.objects.get(user_id=request.user)
        data = request.data
        serializer = ProfileSerializer(data=data)
        serializer.is_valid()
        profile.fullName = serializer.validated_data.get('fullName')
        profile.email = serializer.validated_data.get('email')
        profile.phone = serializer.validated_data.get('phone')
        profile.save()
        serializer = ProfileSerializer(profile)
        data = JSONRenderer().render(serializer.data)
        return Response(data)


class AvatarUpdateView(APIView):
    def post(self, request: Request) -> Response:
        print(request.FILES)
        profile = Profile.objects.get(user=request.user)
        avatar = Avatar.objects.get(profile_id=profile.pk)
        avatar.avatar = request.FILES["avatar"]
        filename = request.FILES["avatar"].name
        avatar.src = '/media/' + profile_avatar_directory_path(profile, filename)
        print(avatar.src, '!!!!!!!!!!!!!!!!!!!!!!')
        avatar.alt = 'avatar'
        avatar.save()
        serializer = AvatarSerializer(avatar)
        print(serializer.data)
        data = JSONRenderer().render(serializer.data)
        print(data)
        return Response(data)


class PasswordUpdateView(APIView):
    def post(self, request: Request) -> Response:
        user = request.user
        print(request.data)
        return Response(status=200)


class CategoriesView(ListAPIView):
    queryset = Category.objects.filter(parent=None).prefetch_related('subcategories')
    serializer_class = CategoriesSerializer
    paginator = None


class TagsView(APIView):
    def get(self, request: Request) -> Response:
        category = request.query_params.get('category')
        if category == 'NaN':
            return Response([])
        item = Tag.objects.get(id=category)
        serializer = TagsSerializer(item)
        # data = JSONRenderer().render(serializer.data)
        return Response([serializer.data])


class LimitedProductsView(ListAPIView):
    queryset = Product.objects.filter(is_limited=True).prefetch_related('tags')[:16]
    serializer_class = ProductSerializer
    paginator = None


class PopularProductsView(ListAPIView):
    queryset = Product.objects.order_by('number_of_purchases', 'title').prefetch_related('tags')[:16]
    serializer_class = ProductSerializer
    paginator = None


class BannersView(ListAPIView):
    queryset = Product.objects.filter(on_banner=True).prefetch_related('tags')[:6]
    serializer_class = ProductSerializer
    paginator = None


class CatalogView(ListAPIView):

    serializer_class = ProductSerializer
    pagination_class = CustomPaginator

    def get_queryset(self):
        name = self.request.GET.get('filter[name]')
        min_price = self.request.GET.get('filter[minPrice]')
        max_price = self.request.GET.get('filter[maxPrice]')
        free_delivery = True if self.request.GET.get('filter[freeDelivery]') == 'true' else False
        available = 1 if self.request.GET.get('filter[available]') == 'true' else 0
        current_page = self.request.GET.get('currentPage')
        sort = self.request.GET.get('sort')
        sort_type = self.request.GET.get('sortType')
        limit = self.request.GET.get('limit')
        print(name, min_price, max_price, free_delivery, available, current_page, sort, sort_type, limit)
        queryset = Product.objects.filter(title__icontains=name,
                                          price__range=(min_price, max_price),
                                          freeDelivery=free_delivery,
                                          count__gte=available
                                          )
        if sort:
            if sort_type == 'dec':
                sort = '-'+sort
            queryset = queryset.order_by(sort)
        print(queryset)
        return queryset


class CategoryCatalogView(CatalogView):
    def get(self, request, category, *args, **kwargs):
        print('!!!!', category)


class ProductView(APIView):
    def get(self, request: Request, product_id) -> Response:
        product = Product.objects.get(pk=product_id)
        serializer = FullProductSerializer(product)
        return Response(serializer.data)
