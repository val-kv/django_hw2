from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost
from .models import Product
from django.urls import reverse


def home_view(request):
    return render(request, 'catalog/base.html')


def contacts_view(request):
    return render(request, 'catalog/contacts.html')


def product_detail_view(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}
    return render(request, 'catalog/product.detail.html', context)


def index_view(request):
    return render(request, 'catalog/index.html')


def about_view(request):
    return render(request, 'catalog/about.html')


def menu_view(request):
    return render(request, 'catalog/menu.html')


def products_view(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/products.html', context)


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


class MenuView(TemplateView):
    template_name = 'catalog/menu.html'


class IndexView(TemplateView):
    template_name = 'catalog/index.html'


class AboutView(TemplateView):
    template_name = 'catalog/about.html'


class ProductsView(TemplateView):
    template_name = 'catalog/products.html'


class ProductDetailView(TemplateView):
    template_name = 'catalog/product.detail.html'


class BaseView(TemplateView):
    template_name = 'catalog/base.html'


class HomeView(TemplateView):
    template_name = 'catalog/home.html'


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'blogposts'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'blogpost'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'slug', 'content', 'preview', 'is_published']

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'slug', 'content', 'preview', 'is_published']

    def get_success_url(self):
        return reverse('blogpost_detail', args=[self.object.pk])


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = '/blog/'  # URL, куда перейти после удаления
