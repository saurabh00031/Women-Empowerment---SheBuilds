from django.urls import path
from SSapp import views
from django.contrib.auth import views as auth_views


urlpatterns = [


 
    path('list/',views.getAllSchollerships,name="SchollershipList"),
    path('home/',views.frontend_home,name="frontend_home"),
    path('rights',views.getAllRights,name="WommenRights"),
    path('list',views.getAllSchollerships,name="SchollershipList"),
    path('sg_user/', views.UsrView.as_view(), name="sg_user"),
    path('sg_mentor/', views.MentorView.as_view(), name="sg_mentor"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('sgin_user/',views.sgin_user,name="sgin_user"),
    path('sgin_mentor/',views.sgin_mentor,name="sgin_mentor"),
    path('logout_user/',views.logout_user,name="logout_user"),
    path('blog/', views.index, name = 'index'),
    path('<str:slug>', views.blog_detailView, name = 'blog_detail'),
    path('addPost/' , views.addPost,name="addPost" ),   
    path('my_posts/',views.my_posts,name="my_posts"),
    path('sginpg_mentor/',views.sginpg_mentor,name="sginpg_mentor"),
    path('sginpg_user/',views.sginpg_user,name="sginpg_user"),   
    path('search/', views.search, name="search"),
    path('send_request/<id>/', views.send_request, name="send_request"),
    path('send_request_user/<username>/', views.send_request_user, name="send_request_user"),
    path('contact_us/', views.contact_us, name="contact_us"),
   



]
