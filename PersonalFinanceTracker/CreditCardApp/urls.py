from django.urls import path
from . import views

urlpatterns = [
    path('credit/', views.credit_view, name='credit'),
    path('allcards/', views.all_credit_users_view, name='allcards'),
    path('apply-card/<int:card_id>/', views.apply_card, name='apply_card'),
    path('delete-card/<int:card_id>/', views.delete_user_view, name='delete_card')
]
