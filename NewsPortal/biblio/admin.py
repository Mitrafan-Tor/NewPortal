from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment



# @admin.register(CategorySubscriber)
# class CategorySubscriberAdmin(admin.ModelAdmin):
#     list_display = ('user', 'category', 'subscribed_at')

# Настраиваем отображение связанных категорий для постов
class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1

# Настраиваем отображение постов в админке
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_type', 'created_at', 'rating')  # Отображаемые поля в списке
    list_filter = ('post_type', 'categories', 'created_at')  # Фильтры справа
    search_fields = ('title', 'text')  # Поиск по этим полям
    inlines = [PostCategoryInline]  # Включаем связанные категории

# Настраиваем отображение комментариев
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at', 'rating')
    list_filter = ('created_at', 'rating')
    search_fields = ('text', 'user__username')

# Настраиваем отображение авторов
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    search_fields = ('user__username',)

# Регистрируем модели в административной панели
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)