from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

class Section(models.Model):
    name = models.CharField('Раздел', max_length=200, unique=True)
    position = models.PositiveIntegerField('Позиция раздела')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['position']


class Article(models.Model):
    section = models.ForeignKey(Section, verbose_name='Раздел', on_delete=models.CASCADE)
    header = models.CharField('Заголовок статьи', max_length=200, unique=True)
    content = RichTextUploadingField('Содержание статьи')
    publication_date = models.DateField('Дата публикации', default=timezone.now)
    position = models.PositiveIntegerField('Позиция в списке', default=1)

    def __str__(self):
        return self.header

    def get_absolute_url(self):
        return f'/articles/{self.section.name}/article-{self.id}'
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['position']

# при добавлении/обновлении статьи при совпадении номеров позиций
# статьи, у которых номер позиции >= номера позиции добавляемой/удаляемой статьи,
# увеличивают свой номер позициии на 1
@receiver(pre_save, sender=Article)
def article_save_signal_handler(sender, instance, **kwargs):
    is_equal_pos = False
    for article in Article.objects.filter(section_id=instance.section_id).order_by('position'):
        if article.position == instance.position and article != instance:
            is_equal_pos = True
        if is_equal_pos:
            article.position += 1
            article.save()

# при удалении ОДНОЙ статьи статьи с бОльшим номером позиции уменьшают номер своей позиции на 1
# при удалении нескольких статей это правило будет применяться только к первой удаляемой статье
# в любом случае, это не критично, и статьи могут содержать пробелы в нумерации позиций
@receiver(pre_delete, sender=Article)
def article_delete_signal_handler(sender, instance, **kwargs):
    for article in Article.objects.filter(section_id=instance.section_id).order_by('-position'):
        if article.position <= instance.position:
            break
        elif article.position > instance.position:
            article.position -= 1
            article.save()
            