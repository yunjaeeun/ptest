from django.shortcuts import render
import requests
from pprint import pprint as pprint
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Count, Avg
from django.db.models import Q, F
from datetime import datetime

from .models import Bank, Product, ProductCategory, ProductOption, UserProducts, Exchange
from .serializers import BankListSerializer, ProductListSerializer, ProductDetailSerializer, ExchangeSerializer

# Create your views here.
API_KEY = settings.BANK_API_KEY

@api_view(['GET'])
def save_banks(request):
    response = requests.get(f"http://finlife.fss.or.kr/finlifeapi/companySearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1")
    
    # response가 정상적으로 데이터를 반환하는지 확인
    if response.status_code == 200:
        for val in response.json().get('result', {}).get('baseList', []):
            bank_name = val.get('kor_co_nm')
            bank_url = val.get('homp_url')
            bank_code = val.get('fin_co_no')
            
            if not Bank.objects.filter(bank_name=bank_name).exists():
                Bank.objects.create(bank_name=bank_name, bank_url=bank_url, bank_code=bank_code)
        
        # 성공적으로 처리된 후 응답
        data = {'title': '정상적으로 생성 되었습니다.'}
        return Response(data, status=status.HTTP_201_CREATED)
    
    # 요청이 실패했을 경우 처리
    else:
        data = {'error': '은행 정보를 가져오는 데 실패했습니다.'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def bank_list(request):
    banks = Bank.objects.all()
    serializer = BankListSerializer(banks, many = True)

    return Response(serializer.data)

@api_view(['GET'])
def save_prdt(request):
    response = requests.get(f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1")
    
    if response.status_code == 200:
        for val in response.json().get('result').get('baseList'):
            fin_code = val.get('fin_co_no')
            prdt_name = val.get('fin_prdt_nm')
            prdt_code = val.get('fin_prdt_cd')
            join_way = val.get('join_way')
            spcl_cnd = val.get('spcl_cnd')
            mtrt_int = val.get('mtrt_int')
            if val.get('join_deny') == '1':
                join_deny = '제한없음'
            elif val.get('join_deny') == '2':
                join_deny = '서민전용'
            elif val.get('join_deny') == '3':
                join_deny = '일부제한'
            join_member = val.get('join_member')
            etc_note = val.get('etc_note')
            max_limit = val.get('max_limit')
            bank = Bank.objects.get(bank_code = fin_code)
            product_category = ProductCategory.objects.get(pk = 1)

            if not Product.objects.filter(prdt_code = prdt_code).exists():
                Product.objects.create(
                    fin_code = fin_code,
                    prdt_name = prdt_name,
                    prdt_code = prdt_code,
                    join_way = join_way,
                    spcl_cnd = spcl_cnd,
                    mtrt_int = mtrt_int,
                    join_deny = join_deny,
                    join_member = join_member,
                    etc_note = etc_note,
                    max_limit = max_limit,
                    bank = bank,
                    product_category = product_category
                )
        for val in response.json().get('result').get('optionList'):
            product = Product.objects.get(prdt_code = val.get('fin_prdt_cd'))
            bank = Bank.objects.get(bank_code = val.get('fin_co_no'))
            rate_type = val.get('intr_rate_type_nm')
            save_trm = val.get('save_trm')
            intr_rate = val.get('intr_rate')
            max_intr_rate = val.get('intr_rate2')

            if not ProductOption.objects.filter(product = product, save_trm = save_trm):
                ProductOption.objects.create(
                    product = product,
                    bank = bank,
                    rate_type = rate_type,
                    save_trm = save_trm,
                    intr_rate = intr_rate,
                    max_intr_rate = max_intr_rate
                )
            
        data = {'title': '정상적으로 생성 되었습니다.'}
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {'error': '은행 정보를 가져오는 데 실패했습니다.'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def save_savings(request):
    response = requests.get(f"http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1")
    
    if response.status_code == 200:
        for val in response.json().get('result').get('baseList'):
            fin_code = val.get('fin_co_no')
            prdt_name = val.get('fin_prdt_nm')
            prdt_code = val.get('fin_prdt_cd')
            join_way = val.get('join_way')
            spcl_cnd = val.get('spcl_cnd')
            mtrt_int = val.get('mtrt_int')
            if val.get('join_deny') == '1':
                join_deny = '제한없음'
            elif val.get('join_deny') == '2':
                join_deny = '서민전용'
            elif val.get('join_deny') == '3':
                join_deny = '일부제한'
            join_member = val.get('join_member')
            etc_note = val.get('etc_note')
            max_limit = val.get('max_limit')
            bank = Bank.objects.get(bank_code = fin_code)
            product_category = ProductCategory.objects.get(pk = 2)

            if not Product.objects.filter(prdt_code = prdt_code).exists():
                Product.objects.create(
                    fin_code = fin_code,
                    prdt_name = prdt_name,
                    prdt_code = prdt_code,
                    join_way = join_way,
                    spcl_cnd = spcl_cnd,
                    mtrt_int = mtrt_int,
                    join_deny = join_deny,
                    join_member = join_member,
                    etc_note = etc_note,
                    max_limit = max_limit,
                    bank = bank,
                    product_category = product_category
                )
        for val in response.json().get('result').get('optionList'):
            product = Product.objects.get(prdt_code = val.get('fin_prdt_cd'))
            bank = Bank.objects.get(bank_code = val.get('fin_co_no'))
            rate_type = val.get('intr_rate_type_nm')
            rsrv_type = val.get('rsrv_type_nm')
            save_trm = val.get('save_trm')
            intr_rate = val.get('intr_rate')
            max_intr_rate = val.get('intr_rate2')

            if not ProductOption.objects.filter(product = product, save_trm = save_trm):
                ProductOption.objects.create(
                    product = product,
                    bank = bank,
                    rate_type = rate_type,
                    rsrv_type = rsrv_type,
                    save_trm = save_trm,
                    intr_rate = intr_rate,
                    max_intr_rate = max_intr_rate
                )
            
        data = {'title': '정상적으로 생성 되었습니다.'}
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {'error': '은행 정보를 가져오는 데 실패했습니다.'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def prdt_list(request):
    product_category = ProductCategory.objects.get(pk = 1)
    products = Product.objects.filter(product_category=product_category)
    
    serializer = ProductListSerializer(products, many = True)

    return Response(serializer.data)

@api_view(['GET'])
def prdt_detail(request, pk):
    product = Product.objects.get(pk = pk)
    
    serializer = ProductDetailSerializer(product)

    return Response(serializer.data)

@api_view(['GET'])
def prdt_list(request):
    # product_category = ProductCategory.objects.all()
    products = Product.objects.all()
    
    serializer = ProductListSerializer(products, many = True)

    return Response(serializer.data)


@api_view(['GET'])
def prdt_detail(request, pk):
    product = Product.objects.get(pk = pk)
    
    serializer = ProductDetailSerializer(product)

    return Response(serializer.data)

@api_view(['GET'])
def savings_list(request):
    product_category = ProductCategory.objects.get(pk = 2)
    products = Product.objects.filter(product_category=product_category)
    
    serializer = ProductListSerializer(products, many = True)

    return Response(serializer.data)

@api_view(['GET'])
def savings_detail(request, pk):
    product = Product.objects.get(pk = pk)
    
    serializer = ProductDetailSerializer(product)

    return Response(serializer.data)

@api_view(['POST'])
def recommend(request):
    data = request.data
    category = data.get('category')
    user_birthday = data.get('user_birthday')  # 사용자의 생년월일
    user_age = calculate_age(user_birthday)  # 사용자의 나이를 계산

    save_trm = data.get('save_trm')  # 입력된 저축 기간
    save_money = data.get('save_money')  # 입력된 저축 금액

    # 기본 상품 필터링
    products = ProductOption.objects.filter(
        product__product_category__product_category=category,
        save_trm__lte=save_trm,  # 저장 기간이 입력값 이하
        product__max_limit__gte=save_money  # 최대 가입 금액 조건 충족
    ).filter(
        Q(product__max_limit__isnull=True) | Q(product__max_limit__gte=save_money)
    )

    # 1. 금리 기반 추천
    max_intr_rate_product = products.order_by('-max_intr_rate').first()
    avg_intr_rate_product = products.annotate(avg_intr_rate=Avg('intr_rate')).order_by('-avg_intr_rate').first()
    max_intr_rate_actual_product = products.order_by('-intr_rate').first()

    recommended_products = []

    # 가장 높은 금리의 상품 추천
    if max_intr_rate_product:
        recommended_products.append(max_intr_rate_product.product)
        # 나머지 상품 필터링
        products = products.exclude(id=max_intr_rate_product.id)

    # 평균 금리가 높은 상품 추천
    if avg_intr_rate_product:
        recommended_products.append(avg_intr_rate_product.product)
        # 나머지 상품 필터링
        products = products.exclude(id=avg_intr_rate_product.id)

    # 실제 금리가 가장 높은 상품 추천
    if max_intr_rate_actual_product:
        recommended_products.append(max_intr_rate_actual_product.product)

    # 중복 없이 최대 3개까지 선택
    recommended_products = list(dict.fromkeys(recommended_products))
    if len(recommended_products) < 3:
        additional_products = products.exclude(product__in=[product.id for product in recommended_products])[:3 - len(recommended_products)]
        recommended_products.extend([product.product for product in additional_products])
    recommended_products = list(dict.fromkeys(recommended_products))[:3]

    # 2. 연령대 추천
    age_group_products = get_age_group_products(user_age)
    age_group_products = [product for product in age_group_products if product not in recommended_products]
    if len(age_group_products) < 3:
        additional_products = ProductOption.objects.exclude(product__in=[product.id for product in recommended_products + age_group_products])[:3 - len(age_group_products)]
        age_group_products.extend([product.product for product in additional_products])
    age_group_products = list(dict.fromkeys(age_group_products))[:3]

    # 3. 전체 사용자가 많이 선택한 상품 추천
    top_products_by_all_users = get_top_products_by_all_users()
    top_products_by_all_users = [product for product in top_products_by_all_users if product not in recommended_products and product not in age_group_products]
    if len(top_products_by_all_users) < 3:
        additional_products = ProductOption.objects.exclude(product__in=[product.id for product in recommended_products + age_group_products + top_products_by_all_users])[:3 - len(top_products_by_all_users)]
        top_products_by_all_users.extend([product.product for product in additional_products])
    top_products_by_all_users = list(dict.fromkeys(top_products_by_all_users))[:3]

    # 결과를 직렬화
    category_based_recommendations = ProductListSerializer(recommended_products, many=True).data
    age_group_recommendations = ProductListSerializer(age_group_products, many=True).data
    top_products_recommendations = ProductListSerializer(top_products_by_all_users, many=True).data

    # 최종 추천 리스트 반환
    return Response({
        'recommended_products': {
            'category_based_recommendations': category_based_recommendations,
            'age_group_recommendations': age_group_recommendations,
            'top_products_by_all_users': top_products_recommendations,
        }
    })


def calculate_age(birth_date_str):
    """
    생년월일을 받아서 나이를 계산하는 함수
    """
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
    today = datetime.today().date()  # 오늘 날짜
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def get_age_group_products(user_age):
    """
    사용자의 나이를 기반으로 연령대에서 가장 많이 가입한 상품 3개를 추천
    """
    if 20 <= user_age < 30:
        age_group = '20대'
    elif 30 <= user_age < 40:
        age_group = '30대'
    elif 40 <= user_age < 50:
        age_group = '40대'
    elif 50 <= user_age < 60:
        age_group = '50대'
    else:
        age_group = '기타'

    age_group_products = UserProducts.objects.filter(
        user__birth_date__year__gte=datetime.today().year - (user_age + 10),
        user__birth_date__year__lte=datetime.today().year - (user_age - 10)
    ).values('product').annotate(Count('product')).order_by('-product__count')[:3]

    recommended_age_group_products = []
    for entry in age_group_products:
        product = Product.objects.get(pk=entry['product'])
        recommended_age_group_products.append(product)

    return recommended_age_group_products


def get_top_products_by_all_users():
    """
    전체 사용자가 가장 많이 가입한 상품 3개를 추천
    """
    top_products = UserProducts.objects.values('product').annotate(Count('product')).order_by('-product__count')[:3]

    recommended_top_products = []
    for entry in top_products:
        product = Product.objects.get(pk=entry['product'])
        recommended_top_products.append(product)

    return recommended_top_products


@api_view(['GET'])
def get_exchange (request):
    EXCHANGE_API_KEY = settings.EXCHANGE_API_KEY
    response = requests.get(f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={EXCHANGE_API_KEY}&data=AP01').json()
    exist_response = Exchange.objects.all()
    
    if response: # 가 있다면기존 데이터를 업데이트
        if not exist_response: # 쿼리셋이 비어있다면
                serializer = ExchangeSerializer(data=response, many=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
        else: # exist_response가 존재한다면
            Exchange.objects.all().delete()
            serializer = ExchangeSerializer(data=response, many=True)     
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
    # 없다면
    serializer = ExchangeSerializer(exist_response, many=True)
    return Response(serializer.data)

from .models import UserProducts
from .serializers import UserProductSerializer, UserProductCreateSerializer
from accounts.models import User

@api_view(['GET','POST', 'PUT', 'DELETE'])
def user_products(request):
    if request.method == "GET":
        user_id = request.query_params.get('user_id')
        user = User.objects.get(pk=user_id)
        user_products = UserProducts.objects.filter(user=user)
        serializer = UserProductSerializer(user_products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        print(request.data)
        serializer = UserProductCreateSerializer()
        serializer = UserProductCreateSerializer(data={
        'user': request.data.get('user_id'),
        'product': request.data.get('product_id')
    })
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        user_product = UserProducts.objects.filter(product__id = request.data.get('product_id'), user__id = request.data.get('user_id'))
        user_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from .serializers import ProductOptionDetailSerializer
from django.core.mail import EmailMessage

@api_view(['GET', 'PUT'])
def option_detail(request, pk):
    product_option = ProductOption.objects.get(pk = pk)
    if request.method == 'GET':
        serializer = ProductOptionDetailSerializer(product_option)

        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProductOptionDetailSerializer(product_option, request.data, partial = True)
        if serializer.is_valid(raise_exception = True):
            serializer.save()

            users = UserProducts.objects.filter(product = product_option.product)

            for user in users:
                print(user.user.email)

                subject = "MOJA 예금 변동 알림"							# 타이틀
                to = [user.user.email]					# 수신할 이메일 주소
                from_email = "wodms6199@naver.com"			# 발신할 이메일 주소
                message = f"{product_option.product.prdt_name}상품의 금리가 변경되었습니다 상품 정보를 확인해보세요 :)"	# 본문 내용
                EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()

            return Response(serializer.data)