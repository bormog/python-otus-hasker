from django.urls import path
from .views import QuestionList, QuestionCreate, QuestionDetail, QuestionSearch

app_name = 'questions'

urlpatterns = [
    path('', QuestionList.as_view(), name='index'),
    path('add/', QuestionCreate.as_view(), name='add'),
    path("<int:pk>/", QuestionDetail.as_view(), name='detail'),
    path("search/", QuestionSearch.as_view(), name='search'),
]