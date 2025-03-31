from django_filters import FilterSet, DateTimeFilter, ModelMultipleChoiceFilter
from .models import Post, Category
from django.forms import DateTimeInput


class SearchPost(FilterSet):
   created_at = DateTimeFilter(
        field_name='created_at',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'}
        )
   )

   class Meta:
       model = Post
       fields = {
           # поиск по названию
           'title': ['icontains'],
           # количество товаров должно быть больше или равно
           'author__user__username': ['icontains'],
       }

   categories = ModelMultipleChoiceFilter(
       field_name='categories',  # имя поля в модели Post
       queryset=Category.objects.all(),
       label='Категории',
   )
