from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('category/<int:cat_id>', views.category, name='category'),
    path('create/', views.create, name='create'),
    path('coursepage/<int:id>/', views.coursepage, name='coursepage'),
    path('profile/', views.profile, name='profile'),
    path('searchbar/', views.searchbar, name='searchbar'),
    path('create_lesson/<int:id>/', views.create_lesson, name='create_lesson'),
    path('lesson/<int:id>/', views.lesson, name='lesson'),

    
    path('add_course_to_user/<int:id>', views.add_course_to_user, name='add_course_to_user'),
    path('pay/<int:id>', views.pay, name= 'pay'),
    path('delete_course_from_user/<int:id>', views.delete_course_from_user, name='delete_course_from_user'),
    path('delete_course/<int:id>', views.delete_course, name='delete_course'),
    path('accept_course/<int:id>', views.accept_course, name='accept_course'),
    path('accountSettings', views.accountSettings, name='accountSettings'),
    path('moderator/', views.moderator, name='moderator'),
    path('send-message/', views.send_message, name='send_message'),
    
    
    path('currency/', views.currency, name='currency'),
    path('my_view/<int:id>', views.my_view, name='my_view'),
    path('cart/', views.cart, name='cart'),
    path('payall/', views.payall, name='payall'),
    path('api/<int:id>', views.UserList.as_view(), name='api'),
    path('api/', views.UserListAll.as_view(), name='apiall'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('send_message/', views.SendMessageView.as_view(), name='send_message'), 
    path('map/', views.map, name='map'),
]
    



