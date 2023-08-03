import io
import json

import django.utils.timezone
from rest_framework.generics import ListAPIView
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
from .serializers import (AuthSerializer, RegisterSerializer, ProfileSerializer, AvatarSerializer, CategoriesSerializer,
                          TagsSerializer, ProductSerializer, FullProductSerializer, ReviewSerializer, CartSerializer,
                          OrderSerializer, SalesSerializer)


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
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
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
        profile = Profile.objects.get(user=request.user)
        avatar = Avatar.objects.get(profile_id=profile.pk)
        avatar.avatar = request.FILES["avatar"]
        filename = request.FILES["avatar"].name
        avatar.src = '/media/' + profile_avatar_directory_path(profile, filename)
        avatar.alt = 'avatar'
        avatar.save()
        serializer = AvatarSerializer(avatar)
        data = JSONRenderer().render(serializer.data)
        return Response(data)


class PasswordUpdateView(APIView):
    def post(self, request: Request) -> Response:
        user = request.user
        return Response(status=200)


class CategoriesView(ListAPIView):
    queryset = Category.objects.filter(parent=None).prefetch_related('subcategories')
    serializer_class = CategoriesSerializer
    paginator = None


class TagsView(APIView):
    def get(self, request: Request) -> Response:
        category = request.query_params.get('category')
        if category:
            item = Tag.objects.get(id=category)
            serializer = TagsSerializer(item)
            return Response([serializer.data])
        else:
            items = Tag.objects.all()
            serializer = TagsSerializer(items, many=True)
            return Response(serializer.data)


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


def get_categories(category):
    categories_list = Category.objects.all()
    result = []
    for i in categories_list:
        if i.id == int(category):
            result.append(i.id)
        if i.parent_id == int(category):
            result += get_categories(i.id)
    return result


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
        if category:
            categories = get_categories(category)
            queryset = Product.objects.filter(title__icontains=name,
                                              category__in=categories,
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
            if sort == 'reviews':
                sort = 'review'
            elif sort == 'rating':
                sort = 'number_of_purchases'
            if sort_type == 'dec':
                sort = '-'+sort
            queryset = queryset.order_by(sort)
        return queryset


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
        return queryset

    def post(self, request):
        data = request.data
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        order = Order(user=user, totalCost=0)
        order.save()
        for item in data:
            product = Product.objects.get(id=item.get('id'))
            count = item.get('count')
            if product.count >= count:
                order_product = OrderProducts(order=order,
                                              product=product,
                                              count=count)
                order.totalCost += product.price * count
                order_product.save()
                product.count -= count
                product.number_of_purchases += count
                product.save()
        order.save()
        return Response({'orderId': order.pk})


class OrderDetailsView(APIView):
    def data(self):
        queryset = self.get_queryset()
        serializer = CartSerializer(queryset, context=self.request.session.get('cart'), many=True)
        return serializer.data

    def get(self, request, order_id):
        data = Order.objects.get(id=order_id)
        serializer = OrderSerializer(data)
        return Response(serializer.data)

    def post(self, request, order_id):
        instance = Order.objects.get(id=order_id)
        serializer = OrderSerializer(instance=instance, data=request.data)
        serializer.is_valid()
        serializer.save(instance=instance, validated_data=serializer.data)
        request.session['cart'] = []
        request.session.save()
        return Response(status=200)


class PaymentView(APIView):
    def post(self, request, order_id):
        success = False
        print(request.data)
        card_number = request.data.get('number')
        year = request.data.get('year')
        month = request.data.get('month')
        code = request.data.get('code')
        if card_number.isdigit() and len(card_number) == 16 and not card_number.endswith('0'):
            order = Order.objects.get(id=order_id)
            order.status = 'paid'
            order.save()
            return Response(status=200)
        else:
            return Response(status=418)


class SalesView(ListAPIView):
    serializer_class = SalesSerializer
    pagination_class = CustomPaginator
    queryset = Product.objects.exclude(salePrice=None)
