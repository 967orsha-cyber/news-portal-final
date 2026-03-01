from django.urls import path
from . import views

urlpatterns = [
    path('', views.BulletinListView.as_view(), name='bulletin_list'),
    path('<int:pk>/', views.BulletinDetailView.as_view(), name='bulletin_detail'),
    path('create/', views.BulletinCreateView.as_view(), name='bulletin_create'),
    path('<int:pk>/response/', views.ResponseCreateView.as_view(), name='response_create'),
    path('my-responses/', views.MyResponsesView.as_view(), name='my_responses'),
    path('response/<int:pk>/accept/', views.ResponseAcceptView.as_view(), name='response_accept'),
    path('response/<int:pk>/delete/', views.ResponseDeleteView.as_view(), name='response_delete'),
    path('<int:pk>/edit/', views.BulletinUpdateView.as_view(), name='bulletin_edit'),
]