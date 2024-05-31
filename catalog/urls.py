from django.urls import path

from catalog import views
from catalog.views import ContactsView, HomeView, ProductDetailView, IndexView, AboutView, MenuView, \
    BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView, create_product, \
    ProductListView, ProductUpdateView, ProductDeleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('index/', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('blog/', BlogPostListView.as_view(), name='blogpost_list'),
    path('posts/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('posts/create/', BlogPostCreateView.as_view(), name='blogpost_create'),
    path('posts/<int:pk>/update/', BlogPostUpdateView.as_view(), name='blogpost_update'),
    path('posts/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blogpost_delete'),
    path('create_product/', create_product, name='create_product'),
    path('create_version/', views.create_version, name='create_version'),
    path('create_product_done/', views.create_product_done, name='create_product_done'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
