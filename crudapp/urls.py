
from django import views
from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('', views.login, name='login'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('signup/', views.signup, name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('usercreate/', views.usercreate, name='usercreate'),
    path('home/', views.home, name='home'),
    
    ####################################################################### -{Category}
    path('add_category/', views.add_category, name='add_category'),
    path('view_category/', views.view_category, name='view_category'),
    path('edit_category/<int:id>', views.edit_category, name='edit_category'),
    path('delete_category/<int:id>', views.delete_category, name='delete_category'),

    ###################################################################### -{Room}
    path('add_room/', views.add_room, name='add_room'),
    path('view_room/', views.view_room, name='view_room'),
    path('edit_room/<int:id>', views.edit_room, name='edit_room'),
    path('delete_room/<int:id>', views.delete_room, name='delete_room'),
    path('available_room', views.available_room, name='available_room'),

    ######################################################################### -{Special Rate}
    path('add_specialrate/', views.add_specialrate, name='add_specialrate'),
    path('view_offer/', views.view_offer, name='view_offer'),
    path('edit_specialrate/<int:id>', views.edit_specialrate, name='edit_specialrate'),
    path('delete_specialrate/<int:id>', views.delete_specialrate, name='delete_specialrate'),

    ######################################################################## -{reservation}
    path('reservation_home', views.reservation_home, name='reservation_home'),
    path('get_room', views.get_room, name='get_room'),
    path('reservation_view', views.reservation_view, name='reservation_view'),
    path('room_reservation', views.room_reservation, name='room_reservation'),
    
    
]
