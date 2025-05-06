

from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),


    path('updateuser/<int:user_id>/',views.update_user_view, name='update_user'),
    path('deleteuser/<int:user_id>/',views.delete_user_view, name='delete_user'),

    
    path('about/', views.about_view, name='about'),
    
    path('networth/', views.networth_view, name='networth'),
    path('check/', views.check_it_out_view, name='check_it_out'),
    path('contact/', views.contact_view, name='contact'),
    path('profile/', views.view_profile, name='profile'),
    path('allprofile/', views.all_profile_view, name='allprofile'),
    
    path('allcontact/', views.all_contact_view, name='allcontact'),



    path('calculator/', views.calculator_view, name='calculator'),
    path('fd/', views.fd_view, name='fd'),
    path('sip/', views.sip_view, name='sip'),
    path('emi/', views.emi_view, name='emi'),
    path('rd/', views.rd_view, name='rd'),
    path('savings/', views.savings_view, name='savings'),

]