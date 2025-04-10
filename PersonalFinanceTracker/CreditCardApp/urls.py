from django.urls import path
from . import views

urlpatterns = [
    path('credit/', views.credit_view, name='credit'),
    path('apply-card/<int:card_id>/', views.apply_card, name='apply_card'),
]
