from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # Суммарный рейтинг статей автора * 3
        posts_rating = self.post_set.aggregate(models.Sum('rating'))['rating__sum'] or 0
        posts_rating *= 3

        # Суммарный рейтинг комментариев автора
        author_comments_rating = Comment.objects.filter(user=self.user).aggregate(
            models.Sum('rating'))['rating__sum'] or 0

        # Суммарный рейтинг комментариев к статьям автора
        posts_comments_rating = Comment.objects.filter(post__author=self).aggregate(
            models.Sum('rating'))['rating__sum'] or 0

        # Обновляем рейтинг автора
        self.rating = posts_rating + author_comments_rating + posts_comments_rating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories', blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    POST_TYPES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.text}"

    def __str__(self):
        return f"{self.title}: {self.text[:20]}"

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"


# class CategorySubscriber(models.Model):
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     category = models.ForeignKey('Category', on_delete=models.CASCADE)
#     subscribed_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db_table = 'biblio_categorysubscriber'
#         unique_together = ('user', 'category')
#         verbose_name = 'Подписчик на категорию'
#
#     def __str__(self):
#         return f"{self.user.username} -> {self.category.name}"

