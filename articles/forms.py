from .models import Section, Article
from django.forms import ModelForm, TextInput, Textarea, DateTimeField, Select, NumberInput
from bootstrap_datepicker_plus import DatePickerInput
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ArticleForm(ModelForm):
    publication_date = DateTimeField(
        input_formats = ['%d/%m/%Y'],
        widget = DatePickerInput(format='%d/%m/%Y'),
        label = 'Дата публикации'
    )

    class Meta:
        model = Article
        fields = ['section', 'header', 'content', 'publication_date', 'position']

        widgets = {
            'section': Select(attrs={
                'class': 'form-control',
            }),
            'publication_date': DatePickerInput(),
            'header': TextInput(attrs={
                'class': 'form-control',
            }),
            'content': CKEditorUploadingWidget(config_name='default'),
            'position': NumberInput(attrs={
                'class': 'form-control',
            })
        }
