from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost, Product, Version
from django.urls import reverse, reverse_lazy
from .forms import ProductForm, VersionForm, CustomModeratorForm, CustomOwnerForm
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView
from django.views.decorators.cache import cache_page

from .services import get_cached_categories


def home(request):
    return render(request, 'catalog/base.html')


def contacts(request):
    return render(request, 'catalog/contacts.html')


@cache_page(300)
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product.detail.html', {'product': product})


def index(request):
    return render(request, 'catalog/index.html')


def about(request):
    return render(request, 'catalog/about.html')


def menu(request):
    return render(request, 'catalog/menu.html')


def products(request):
    product_list = Product.objects.all()
    context = {'product_list': product_list}
    return render(request, 'catalog/product_list.html', context)


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


class MenuView(TemplateView):
    template_name = 'catalog/menu.html'


class IndexView(TemplateView):
    template_name = 'catalog/index.html'


class AboutView(TemplateView):
    template_name = 'catalog/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['versions'] = Version.objects.all()
        return context


class ProductDetailView(TemplateView):
    model = Product
    template_name = 'catalog/templates/catalog/product.detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['versions'] = Version.objects.all()

        return context


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()

        for product in products:
            versions = Version.objects.filter(product=product)
            active_version = versions.filter(is_active=True).first()
            product.active_version_name = active_version.version_name if active_version else "Нет активной версии"

        context['products'] = products
        return context


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

    def get_success_url(self):
        return reverse('blogpost_detail', args=[self.object.pk])


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalog:product_list')  # Перенаправление на страницу списка продуктов
    else:
        form = ProductForm()

    return render(request, 'create_product.html', {'form': form})


def create_version(request):
    if request.method == 'POST':
        form = VersionForm(request.POST)
        if form.is_valid():
            new_version = form.save(commit=False)  # Создание объекта версии без сохранения в базу данных
            # Установка флага is_active
            new_version.is_active = True  # устанавливаем активной только что созданную версию
            new_version.save()  # Сохранение версии
            return redirect('catalog:create_product_done')  # Перенаправление на страницу списка продуктов
    else:
        form = VersionForm()

    return render(request, 'create_version.html', {'form': form})


def create_product_done(request):
    return render(request, 'product_list.html')


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields_owner = ['name', 'description', 'price', 'category', 'image']
    fields_moderator = ['name', 'description', 'price', 'category']

    template_name = 'catalog/product_update.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        user = self.request.user
        product = self.get_object()
        return user.is_staff or user.groups.filter(name='moderators').exists() or product.user == user

    def get_form_class(self):
        if self.request.user.is_staff:
            return super().get_form_class()
        elif self.request.user.groups.filter(name='moderators').exists():
            return CustomModeratorForm
        else:
            return CustomOwnerForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_delete.html'
    success_url = reverse_lazy('catalog:product_list')


def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.user == product.owner:

        return render(request, 'edit_product.html', {'product': product})
    else:
        return HttpResponseForbidden("Вы не администратор. Редактирование запрещено")
