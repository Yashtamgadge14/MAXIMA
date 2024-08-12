from django.urls import path
from maximaapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
   
    path('home',views.home),
    path('index',views.index),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('register',views.register),
    path('po',views.po),
    path('pd/<pid>',views.product_details),
    path('cart',views.cart),
    path('sort/<sv>',views.sort),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('makepayment',views.makepayment),
    path('sendmail',views.sendusermail),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


