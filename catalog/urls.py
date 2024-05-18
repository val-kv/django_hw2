from django.urls import path
from catalog.views import ContactsView, HomeView, ProductDetailView, IndexView, AboutView, ProductsView, MenuView, BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('/', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('products/', ProductsView.as_view(), name='products'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('', BlogPostListView.as_view(), name='blogpost_list'),
    path('<int:pk>/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('create/', BlogPostCreateView.as_view(), name='blogpost_create'),
    path('<int:pk>/update/', BlogPostUpdateView.as_view(), name='blogpost_update'),
    path('<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blogpost_delete'),
]