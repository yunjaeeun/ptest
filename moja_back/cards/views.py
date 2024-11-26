from django.shortcuts import render
import requests
from pprint import pprint as pprint
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404

from .models import Company, Card, CardOption, OptionCategory
from .serializers import CardSerializer
from decouple import config
from openai import OpenAI  # 변경된 import 방식


# Create your views here.
@api_view(["GET"])
def card_list(requset):
    cards = Card.objects.all()

    serializer = CardSerializer(cards, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def card_detail(request, pk):
    card = Card.objects.get(pk=pk)

    serializer = CardSerializer(card)
    return Response(serializer.data)


# OpenAI 클라이언트 인스턴스 생성
client = OpenAI(api_key=config("OPENAI_API_KEY"))


@api_view(["POST"])
def recommend(request):
    # Step 1: 사용자가 원하는 혜택 ID 받기
    user_preferences = request.data.get("preferences", [])
    card_type = request.data.get("card_type", None)
    if not user_preferences or not isinstance(user_preferences, list):
        return Response(
            {
                "error": "Invalid preferences provided. It should be a list of OptionCategory IDs."
            },
            status=400,
        )

    # Step 2: OptionCategory ID를 기반으로 관련 카드 옵션 필터링
    matching_options = CardOption.objects.filter(
        option_category__id__in=user_preferences
    )
    matching_cards = Card.objects.filter(
        cardoption__in=matching_options
    ).select_related(
        'company',
        'card_category'
    ).prefetch_related(
        'cardoption_set',
        'cardoption_set__option_category'
    ).distinct()

    if not matching_cards.exists():
        return Response(
            {"error": "No matching cards found for the given preferences."}, status=404
        )

    # Step 3: 카드 데이터를 직렬화
    card_data = CardSerializer(matching_cards, many=True).data

    # Step 4: OpenAI 프롬프트 생성
    selected_categories = OptionCategory.objects.filter(id__in=user_preferences)
    preferences_str = ", ".join(
        [category.option_category for category in selected_categories]
    )

    try:
        # Step 5: GPT 호출 (OpenAI 최신 API 방식)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """주어진 카드 목록에서 상위 5개의 카드를 추천해주세요.
                    아래 형식으로 JSON 객체를 반환해주세요:
                    {
                        "recommended_cards": [
                            {
                                "id": "카드 pk",
                                "card_name": "카드명",
                                "company": {
                                    "name": "카드사명",
                                    "url": "카드사 URL"
                                },
                                "cardoption_set": [
                                    {
                                        "option_category": "혜택 카테고리",
                                        "detail": "혜택 상세 내용"
                                    }
                                ],
                                "reason": "이 카드를 추천하는 이유"
                            }
                        ],
                        "summary": "전체 추천 결과에 대한 요약"
                    }
                    
                    performance 점수가 높은 순으로 정렬하되, 사용자의 선호 카테고리와 매칭되는 혜택을 우선적으로 고려해주세요."""
                },
                {
                    "role": "user",
                    "content": f"""
                사용자가 원하는 혜택 카테고리: {preferences_str},
                사용자가 원하는 카드 카테고리: {card_type},

                추천 가능한 카드 목록:
                {card_data}

                위 데이터를 바탕으로 사용자의 선호 카테고리와 가장 잘 매칭되는 상위 5개의 카드를 추천해주세요.
                각 카드별로 추천하는 이유도 설명해주시고, 마지막에는 전체적인 추천 결과에 대한 요약도 추가해주세요.
                """,
                },
            ],
        )

        # Step 6: 응답 처리 - JSON 문자열을 파싱하여 JSON 객체로 변환
        import json
        gpt_response = json.loads(response.choices[0].message.content)
        return Response({"recommendations": gpt_response})

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
from .models import UserCards
from .serializers import UserCardSerializer, UserCardCreateSerializer
from accounts.models import User

@api_view(['GET', 'POST', 'DELETE'])
def user_card(request):
    if request.method == "GET":
        user_id = request.query_params.get('user_id')
        user = User.objects.get(pk=user_id)
        user_cards = UserCards.objects.filter(user=user)
        serializer = UserCardSerializer(user_cards, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        print(request.data)
        serializer = UserCardCreateSerializer(data={
        'user': request.data.get('user_id'),
        'card': request.data.get('card_id')
    })
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        user_product = UserCards.objects.filter(card__id = request.data.get('card_id'), user__id = request.data.get('user_id'))
        user_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.db.models import Count

@api_view(['GET'])
def best_card(request):
    # 전체 사용자 기준 카드 사용 데이터를 그룹화 및 집계
    card_usage = (
        UserCards.objects.values("card__id", "card__card_category__card_category")
        .annotate(usage_count=Count("id"))
        .order_by("-usage_count")
    )

    # 체크카드와 신용카드를 나누기 위한 분류
    check_cards = card_usage.filter(card__card_category__card_category="체크카드")[:10]
    credit_cards = card_usage.filter(card__card_category__card_category="신용카드")[:10]

    # 카드 객체 가져오기
    check_card_objs = Card.objects.filter(id__in=[card["card__id"] for card in check_cards])
    credit_card_objs = Card.objects.filter(id__in=[card["card__id"] for card in credit_cards])

    # 결과 데이터 준비
    best_cards = {
        "check_cards": CardSerializer(check_card_objs, many=True, context={"request": request}).data,
        "credit_cards": CardSerializer(credit_card_objs, many=True, context={"request": request}).data,
    }

    return Response(best_cards)