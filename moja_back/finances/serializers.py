from rest_framework import serializers
from .models import Bank, Product, ProductOption, Exchange, UserProducts
from accounts.models import User



class BankListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = "__all__"

class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = ['rate_type', 'rsrv_type', 'save_trm', 'intr_rate', 'max_intr_rate'] 

class ProductListSerializer(serializers.ModelSerializer):
    bank = BankListSerializer()
    product_options = serializers.SerializerMethodField()  # SerializerMethodField 사용

    class Meta:
        model = Product
        exclude = ['fin_code', 'prdt_code', 'etc_note']

    def get_product_options(self, obj):
        # `ProductOption`을 `intr_rate`가 최솟값인 것 하나와 `max_intr_rate`가 최댓값인 것 하나로 필터링
        options = obj.productoption_set.all()

        # `intr_rate`가 최솟값인 ProductOption
        min_intr_rate_option = options.order_by('intr_rate').first()  # intr_rate가 최소인 항목
        # `max_intr_rate`가 최댓값인 ProductOption
        max_intr_rate_option = options.order_by('-max_intr_rate').first()  # max_intr_rate가 최대인 항목

        # 필터링된 옵션을 직렬화
        serialized_options = []
        if min_intr_rate_option:
            serialized_options.append(ProductOptionSerializer(min_intr_rate_option).data)
        if max_intr_rate_option and max_intr_rate_option != min_intr_rate_option:  # 중복 방지
            serialized_options.append(ProductOptionSerializer(max_intr_rate_option).data)

        return serialized_options


class ProductDetailSerializer(serializers.ModelSerializer):
    bank = BankListSerializer()
    product_options = ProductOptionSerializer(source='productoption_set', many=True)

    class Meta:
        model = Product
        fields = '__all__'

class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserProductSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProducts
        fields = '__all__'

class UserProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProducts
        fields = '__all__'

class ProductForOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductOptionDetailSerializer(serializers.ModelSerializer):
    product = ProductForOptionSerializer()
    class Meta:
        model = ProductOption
        fields = '__all__'