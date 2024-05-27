from django import forms
from .models import Product, Version, Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super(StyledFormMixin, self).__init__(*args, **kwargs)

        # Переопределение классов полей формы
        self.fields = {field_name: field for field_name, field in self.fields.items()}
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Дополнительные стили для конкретных полей
        if 'is_active' in self.fields:
            self.fields['is_active'].widget.attrs['class'] = 'form-check-input'

        # Настройка стилей для формы
        self.helper = FormHelper()


class ProductForm(StyledFormMixin, forms.ModelForm):
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


class VersionForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ['product', 'version_number', 'version_name', 'is_current_version']
        widgets = {
            'is_current_version': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class CategoryForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'


class FormsetHelper:
    def __init__(self, *args, **kwargs):
        super(FormsetHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
