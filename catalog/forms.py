from django import forms
from .models import Product, Version, Category


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана",
                                      required=True)
    image = forms.ImageField(required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']

    def clean_name(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        name = self.cleaned_data.get('name', '')
        for word in forbidden_words:
            if word in name.lower():
                raise forms.ValidationError(f"Нельзя использовать слово '{word}' в названии продукта.")
        return name

    def clean_description(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        description = self.cleaned_data.get('description', '')
        for word in forbidden_words:
            if word in description.lower():
                raise forms.ValidationError(f"Нельзя использовать слово '{word}' в описании продукта.")
        return description


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['product', 'version_number', 'version_name', 'is_current_version']

    def __init__(self, *args, **kwargs):
        super(VersionForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['class'] = 'form-control'
        self.fields['version_number'].widget.attrs['class'] = 'form-control'
        self.fields['version_name'].widget.attrs['class'] = 'form-control'
        self.fields['is_current_version'].widget.attrs['class'] = 'form-check-input'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
