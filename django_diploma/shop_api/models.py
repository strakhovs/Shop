import django.utils.timezone
from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='name')

    def __str__(self):
        return self.name


class Specification(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    value = models.CharField(max_length=100, verbose_name='value')

    def __str__(self):
        return f'{self.name}: {self.value}'


class Category(models.Model):

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    title = models.CharField(max_length=50, verbose_name='category')
    image = models.ImageField(null=True, upload_to="categories/", verbose_name='image')
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               db_index=True,
                               related_name='subcategories')

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='category')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='price')
    count = models.IntegerField(verbose_name='count', default=0)
    date = models.DateTimeField(verbose_name='date', default=django.utils.timezone.now)
    title = models.CharField(max_length=50, verbose_name='title', default='')
    description = models.TextField(max_length=250, verbose_name='description')
    fullDescription = models.TextField(max_length=500, default='', verbose_name='full description')
    freeDelivery = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='tags')
    specifications = models.ManyToManyField(Specification, related_name='specifications')
    is_limited = models.BooleanField(verbose_name='is limited', default=False)
    number_of_purchases = models.IntegerField(verbose_name='number of purchases', default=0)
    on_banner = models.BooleanField(verbose_name='on banner', default=False)
    salePrice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dateFrom = models.DateField(null=True)
    dateTo = models.DateField(null=True)

    def __str__(self):
        return self.title


def product_image_directory_path(instance, filename):
    return "products/{pk}/{filename}".format(pk=instance.product_id.pk, filename=filename)


class Image(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product id')
    image = models.ImageField(upload_to=product_image_directory_path, verbose_name='image')
    alt = models.CharField(max_length=50, verbose_name='alt')


class Review(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product id')
    author = models.CharField(max_length=200, verbose_name='author')
    email = models.EmailField(verbose_name='email')
    text = models.TextField(max_length=250, verbose_name='text')
    rate = models.IntegerField(verbose_name='rate')
    date = models.DateTimeField(default=django.utils.timezone.now, verbose_name='date')


def profile_avatar_directory_path(instance: "Profile", filename: str) -> str:
    return "users/{pk}/avatar/{filename}".format(
        pk=instance.id,
        filename=filename,
    )


class Profile(models.Model):
    class Meta:
        verbose_name_plural = 'profiles'
        verbose_name = 'profile'

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user')
    fullName = models.CharField(max_length=100, null=False, blank=True)
    email = models.EmailField(null=False, blank=True)
    phone = models.CharField(max_length=15, blank=True, verbose_name='phone')


class Avatar(models.Model):
    class Meta:
        verbose_name = 'avatar'
    profile = models.OneToOneField(Profile, null=True, on_delete=models.CASCADE, verbose_name='user')
    avatar = models.ImageField(null=True, upload_to=profile_avatar_directory_path, verbose_name='avatar')
    src = models.CharField(max_length=100)
    alt = models.CharField(max_length=200)


class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    deliveryType = models.CharField(max_length=50)
    paymentType = models.CharField(max_length=50)
    totalCost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)


class OrderProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
