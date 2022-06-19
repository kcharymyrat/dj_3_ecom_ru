from pyexpat import model
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

# Create your models here.

####################
# 1. Category
# 2. Product
# 3. CartProduct
# 4. Cart
# 5. Order
###################
# 6. Customer
# 7. Specifications


class LatestProductsManager:
    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get("with_respect_to")
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = (
                ct_model.model_class()._base_manager.all().order_by("-id")[:5]
            )
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products,
                        key=lambda x: x.__class__._meta.model_name.startswith(
                            with_respect_to
                        ),
                        reverse=True,
                    )
        return products


class LatestProducts:
    objects = LatestProductsManager()


class Category(models.Model):

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    class Meta:
        abstract = True

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField()
    decription = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.title


class Notebook(Product):
    diagonal = models.CharField(max_length=255)
    display_type = models.CharField(max_length=255)
    processor_freq = models.CharField(
        max_length=255, verbose_name="Processor frequency"
    )
    ram = models.CharField(max_length=255)
    video = models.CharField(max_length=255)
    time_without_charge = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category.name}: {self.title}"


class Smartphone(Product):
    diagonal = models.CharField(max_length=255)
    display_type = models.CharField(max_length=255)
    resolution = models.CharField(max_length=255)
    accum_volume = models.CharField(max_length=255, verbose_name="Battery volume")
    ram = models.CharField(max_length=255)
    sd = models.BooleanField(default=True)
    sd_volume_max = models.CharField(max_length=255, verbose_name="Max SD volume")
    main_cam_mp = models.CharField(max_length=255, verbose_name="Main camera")
    frontal_cam_mp = models.CharField(max_length=255, verbose_name="Frontal camera")

    def __str__(self) -> str:
        return f"{self.category.name}: {self.title}"


class CartProduct(models.Model):

    user = models.ForeignKey(
        "Customer", verbose_name="Customer", on_delete=models.CASCADE
    )
    cart = models.ForeignKey(
        "Cart", on_delete=models.CASCADE, related_name="related_products"
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f"Products (for cart): {self.product.title}"

    class Meta:
        indexes = [models.Index(fields=["content_type", "object_id"])]


class Cart(models.Model):

    owner = models.ForeignKey("Customer", on_delete=models.CASCADE)
    products = models.ManyToManyField(
        CartProduct, blank=True, related_name="related_cart"
    )
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self) -> str:
        return self.id


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Phone number")
    address = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return f"Customer: {self.user.first_name} {self.user.last_name}"
