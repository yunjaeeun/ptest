from django.db import models
from django.conf import settings

################################################
# 질문 게시판
# 질문 게시판 글 작성 기능
class HelpArticle(models.Model):
    # 카테고리 선택사항 정의
    CATEGORY_CHOICES = [
        ('HELP', '도와줘요'),
        ('RECOM', '추천해요'),
        ('TOGETHER', '함께해요'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="작성자")
    help_category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, verbose_name="질문 카테고리")
    help_title = models.CharField(max_length=255, verbose_name="질문 제목")
    help_content = models.TextField(verbose_name="질문 내용")
    help_date = models.DateField(auto_now_add=True, verbose_name="질문 작성일")
    help_delete_date = models.DateField(null=True, blank=True, verbose_name="삭제일")

    def __str__(self):
        return self.help_title


# 질문 게시판 좋아요
class HelpLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="좋아요한 회원")
    help_article = models.ForeignKey(HelpArticle, on_delete=models.CASCADE, verbose_name="좋아요한 질문")

    class Meta:
        unique_together = ("user", "help_article")  # 중복 좋아요 방지


# 질문 게시판 댓글
class HelpComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="작성자")
    help_article = models.ForeignKey(HelpArticle, on_delete=models.CASCADE, verbose_name="관련 질문")
    help_comment_content = models.TextField(verbose_name="댓글 내용")
    help_comment_date = models.DateField(auto_now_add=True, verbose_name="작성일")
    help_comment_delete_date = models.DateField(null=True, blank=True, verbose_name="삭제일")

    def __str__(self):
        return f"{self.user}의 댓글: {self.help_comment_content[:20]}"
################################################