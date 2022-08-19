from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    Author_rating = models.IntegerField(default=0)

    def update_rating(self):
        sum_rating = self.post_set.aggregate(post_rating=Sum('post_rate'))
        result_sum_rating = 0
        try:
            result_sum_rating += sum_rating.get('post_rating')
        except TypeError:
            result_sum_rating = 0

        sum_comment_rating = self.authorUser.comment_set.aggregate(comment_rating=Sum('comment_rate'))
        result_sum_comment_rating = 0
        result_sum_comment_rating += sum_comment_rating.get('comment_rating')
        self.user_rate = result_sum_rating * 3 + result_sum_comment_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscriber', blank=True)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    POSITIONS = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    category_type = models.CharField(max_length=2, choices=POSITIONS, default=ARTICLE)
    created_date = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    post_rate = models.IntegerField(default=0)

    def like(self):
        self.post_rate += 1
        self.save()

    def dislike(self):
        self.post_rate -= 1
        self.save()

    def preview(self):
        return self.text[:125] + '...'

    def __str__(self):
        return f'{self.title}. {self.text[:10]} ...'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def message_subscriber(self):
        return f'Новая статья - "{self.title}" в разделе "{self.post_category.first()}" '


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rate = models.IntegerField(default=0)

    def like(self):
        self.comment_rate += 1
        self.save()

    def dislike(self):
        self.comment_rate -= 1
        self.save()


