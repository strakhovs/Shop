import datetime
import io
import json

import django.utils.timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password

from .models import Profile, Avatar, profile_avatar_directory_path, Category, Tag, Product, Review, Order, OrderProducts
from .paginators import CustomPaginator
from .serializers import AuthSerializer, RegisterSerializer, ProfileSerializer, AvatarSerializer, CategoriesSerializer, \
    TagsSerializer, ProductSerializer, CatalogRequestSerializer, FullProductSerializer, ReviewSerializer, \
    CartSerializer, OrderSerializer
from django.conf import settings


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
        category = self.request.GET.get('category')
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
        if category:
            queryset = Product.objects.filter(title__icontains=name,
                                              category=category,
                                              price__range=(min_price, max_price),
                                              freeDelivery=free_delivery,
                                              count__gte=available
                                              )
        else:
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


class ReviewAddView(APIView):
    def post(self, request, product_id):
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid()
        review = Review(
            product_id=Product.objects.get(id=product_id),
            author=serializer.validated_data.get('author'),
            email=serializer.validated_data.get('email'),
            text=serializer.validated_data.get('text'),
            rate=serializer.validated_data.get('rate'),
            date=django.utils.timezone.now()
            )
        review.save()
        return Response(serializer.data, status=200)


class BasketAPIView(ListAPIView):
    serializer_class = CartSerializer

    def data(self):
        queryset = self.get_queryset()
        serializer = CartSerializer(queryset, context=self.request.session.get('cart'), many=True)
        return serializer.data

    def get_queryset(self):
        if 'cart' in self.request.session:
            products = self.request.session['cart']
            ids = list()
            print(products)
            for i in products:
                ids.append(i['id'])
            data = Product.objects.filter(id__in=ids)
        else:
            data = ''
        return data

    def delete(self, request):
        data = json.loads(request.body)
        product_id = data['id']
        count = int(data['count'])
        for index, value in enumerate(request.session['cart']):
            if next(iter(value.values())) == product_id:
                request.session['cart'][index]['count'] -= count
                if request.session['cart'][index]['count'] == 0:
                    request.session['cart'].remove(request.session['cart'][index])
                request.session.save()
                return Response(self.data())
        return Response(status=500)

    def get(self, request):
        return Response(self.data())

    def post(self, request):
        product_id = request.data['id']
        count = int(request.data['count'])
        if 'cart' in request.session:
            for index, value in enumerate(request.session['cart']):
                if next(iter(value.values())) == product_id:
                    request.session['cart'][index]['count'] += count
                    request.session.save()
                    return Response(self.data())
            request.session['cart'].append({'id': product_id, 'count': count})
            request.session.save()
            return Response(self.data())
        request.session['cart'] = [{'id': product_id, 'count': count}]
        request.session.save()
        return Response(self.data())


class OrderAPIView(ListAPIView):
    serializer_class = OrderSerializer
    paginator = None

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        serializer = OrderSerializer(queryset, many=True)
        print('\n\n', serializer.data)
        return queryset

    def post(self, request):
        data = request.data
        for item in data:
            print(item.get('id'), item.get('count'))
        order = Order(user=request.user)
        order.save()
        for item in data:
            product = OrderProducts(order=order,
                                    product=Product.objects.get(id=item.get('id')),
                                    count=item.get('count'))
            product.save()
        return Response({'orderId': order.pk})


class OrderDetailsView(APIView):
    def data(self):
        queryset = self.get_queryset()
        serializer = CartSerializer(queryset, context=self.request.session.get('cart'), many=True)
        return serializer.data

    def get(self, request, order_id):
        print('order id - ', order_id)
        data = Order.objects.get(id=order_id)
        print('order - ', data)
        serializer = OrderSerializer(data)
        # serializer.is_valid()
        print('\n', serializer)
        result = JSONRenderer().render(serializer.data)
        print(result)
        return Response(serializer.data)

    def post(self, request, order_id):
        instance = Order.objects.get(id=order_id)
        serializer = OrderSerializer(instance=instance, data=request.data)
        serializer.is_valid()
        print(serializer.data)
        serializer.save(instance=instance, validated_data=serializer.data)
        request.session['cart'] = []
        request.session.save()
        return Response(status=200)
