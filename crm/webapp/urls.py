from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'records', views.RecordViewSet)

urlpatterns = [

    path('', views.home, name=""),

    path('register', views.register, name="register"),

    path('my-login', views.my_login, name="my-login"),

    path('user-logout', views.user_logout, name="user-logout"),

    path('about-us', views.about_us, name="about-us"),

    path('stadistic-views', views.stadistic_page, name="stadistic-views"),
    
    path('contact-us-api/', include(router.urls)),

    path('pdf', views.pdf, name="pdf"),
    
    path('contact-us', views.contact_us_page, name="contact-us"),




    # CRUD

    path('dashboard', views.dashboard, name="dashboard"),

    path('create-record', views.create_record, name="create-record"),

    path('update-record/<int:pk>', views.update_record, name='update-record'),

    path('record/<int:pk>', views.singular_record, name="record"),

    path('delete-record/<int:pk>', views.delete_record, name="delete-record"),

]
