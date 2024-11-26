from rest_framework import serializers
from .models import Company, Card, CardOption, CardCategory, OptionCategory, UserCards
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionCategory
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CardCategory
        fields = '__all__'

class CardOptionSerializer(serializers.ModelSerializer):
    option_category = OptionSerializer()  # OptionCategory 직렬화를 위해 OptionSerializer 사용

    class Meta:
        model = CardOption
        fields = ['option_category', 'detail']  # 포함할 필드 명시

class CardSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    cardoption_set = CardOptionSerializer(many=True)

    class Meta:
        model = Card
        fields = '__all__'
        
class UserCardSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    card = CardSerializer()

    class Meta:
        model = UserCards
        fields = '__all__'

class UserCardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCards
        fields = '__all__'
