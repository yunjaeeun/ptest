from rest_framework import serializers
from .models import HelpArticle, HelpLike, HelpComment
from accounts.models import User

################################################
# 질문
# 질문 게시판 글
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class HelpArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    like_count = serializers.IntegerField(read_only=True, required=False)
    
    def validate_help_category(self, value):
        valid_categories = dict(HelpArticle.CATEGORY_CHOICES).keys()
        if value not in valid_categories:
            raise serializers.ValidationError(f"Invalid category. Must be one of: {', '.join(valid_categories)}")
        return value
    
    class Meta:
        model = HelpArticle
        fields = ['id', 'user', 'help_category', 'help_title', 'help_content', 
                'help_date', 'help_delete_date', 'like_count']
        read_only_fields = ['id', 'user', 'help_date']


class HelpArticleCreateSerializer(serializers.ModelSerializer):

    def validate_help_category(self, value):
        valid_categories = dict(HelpArticle.CATEGORY_CHOICES).keys()
        if value not in valid_categories:
            raise serializers.ValidationError(f"올바른 카테고리를 선택해주세요. 가능한 카테고리: {', '.join(valid_categories)}")
        return value
    
    def validate_help_title(self, value):
        if len(value) > 255:
            raise serializers.ValidationError("제목은 255자를 초과할 수 없습니다.")
        return value

    def validate_help_content(self, value):
        if len(value) > 10000:  # 예시로 10000자로 제한
            raise serializers.ValidationError("내용이 너무 깁니다. 더 짧게 작성해주세요.")
        return value
    
    class Meta:
        model = HelpArticle
        fields = ['id', 'user', 'help_category', 'help_title', 'help_content', 'help_date', 'help_delete_date']
        read_only_fields = ['id', 'user', 'help_date']

# 질문 좋아요
class HelpLikeSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    
    class Meta:
        model = HelpLike
        fields = ['id', 'user', 'help_title', 'help_content', 'help_date', 'like_count']
        read_only_fields = ['id', 'user', 'help_date', 'like_count']

# 질문 댓글
class HelpCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = HelpComment
        fields = ['id', 'user', 'help_article', 'help_comment_content', 'help_comment_date', 'help_comment_delete_date']
################################################