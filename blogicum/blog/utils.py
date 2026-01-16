from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Count
from .models import Post


def get_published_posts():
    """Возвращает queryset с опубликованными постами."""
    return Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )


def get_posts_with_counts(queryset):
    """Добавляет аннотации к queryset постов."""
    return queryset.select_related(
        'category', 'location', 'author'
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')


def get_page_obj(request, queryset, per_page=10):
    """Создает объект страницы для пагинации."""
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def get_user_posts(user, request_user=None):
    """
    Получает посты пользователя.
    Если request_user не владелец, скрывает неопубликованные.
    """
    post_list = Post.objects.filter(author=user)
    
    if request_user != user:
        post_list = post_list.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )
    
    return get_posts_with_counts(post_list)
