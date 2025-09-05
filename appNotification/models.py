from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.validators import MinLengthValidator
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from bs4 import BeautifulSoup

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=20, unique=True, default='None')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('tanks', _('Tanks')),
        ('heals', _('Heals')),
        ('dd', _('DD')),
        ('traders', _('Traders')),
        ('guildmasters', _('Guildmasters')),
        ('questgivers', _('Questgivers')),
        ('blacksmiths', _('Blacksmiths')),
        ('tanners', _('Tanners')),
        ('potionmakers', _('Potionmakers')),
        ('spellmasters', _('Spellmasters')),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=255, validators=[MinLengthValidator(5)])
    content = RichTextUploadingField(
        verbose_name=_('Content'),
        help_text=_('You can use rich text editor with images, videos and formatting')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_posts', blank=True)
    image = models.ImageField(
        upload_to='posts/images/',
        blank=True,
        null=True,
        verbose_name=_('Main Image'),
        help_text=_('Main image for the post card')
    )
    video = models.FileField(
        upload_to='posts/videos/',
        blank=True,
        null=True,
        verbose_name=_('Main Video'),
        help_text=_('Main video file (optional)')
    )
    notify_subscribers = models.BooleanField(default=True, verbose_name=_('Notify subscribers'))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return f"{self.title} by {self.author.email}"

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def get_category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)

    def get_embedded_content(self):
        """Извлекает встроенные медиа из контента"""
        # from bs4 import BeautifulSoup
        soup = BeautifulSoup(self.content, 'html.parser')

        embedded_content = {
            'images': [],
            'videos': [],
            'iframes': []
        }

        # Извлекаем изображения
        for img in soup.find_all('img'):
            embedded_content['images'].append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'class': img.get('class', [])
            })

        # Извлекаем видео
        for video in soup.find_all('video'):
            embedded_content['videos'].append({
                'src': video.get('src', ''),
                'controls': video.get('controls', False),
                'width': video.get('width', ''),
                'height': video.get('height', '')
            })

        # Извлекаем iframe (встроенные видео с YouTube и т.д.)
        for iframe in soup.find_all('iframe'):
            embedded_content['iframes'].append({
                'src': iframe.get('src', ''),
                'width': iframe.get('width', ''),
                'height': iframe.get('height', ''),
                'frameborder': iframe.get('frameborder', '0')
            })

        return embedded_content


class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='responses')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    text = models.TextField(validators=[MinLengthValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)  # Новое поле для отклоненных откликов

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Response')
        verbose_name_plural = _('Responses')

    def __str__(self):
        return f"Response to {self.post.title} by {self.author.email}"

    def delete_response(self):
        """Мягкое удаление отклика"""
        self.is_rejected = True
        self.save()


class News(models.Model):
    title = models.CharField(max_length=255, validators=[MinLengthValidator(5)])
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_news', blank=True)
    views_count = models.PositiveIntegerField(default=0, verbose_name=_('Views count'))
    notify_subscribers = models.BooleanField(default=True, verbose_name=_('Notify subscribers'))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('News')
        verbose_name_plural = _('News')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('news_detail', kwargs={'pk': self.pk})

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    news = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'category']
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')

    def __str__(self):
        if self.category:
            return f"{self.user.email} subscribed to {self.category.name}"
        elif self.news:
            return f"{self.user.email} subscribed to news"
        return f"{self.user.email} subscription"

    @classmethod
    def get_user_subscriptions(cls, user):
        return cls.objects.filter(user=user).select_related('category')

    @classmethod
    def is_user_subscribed_to_news(cls, user):
        return cls.objects.filter(user=user, news=True).exists()

    @classmethod
    def is_user_subscribed_to_category(cls, user, category):
        return cls.objects.filter(user=user, category=category).exists()
