from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager

class User_Registration_Model(AbstractUser):
    STATUS_TYPE = (
    	(1,'Admin'),
    	(2,'User'),
    	(3,'guest_user'))
    username = models.CharField(max_length=64,unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    phone_number = models.IntegerField(null=True,blank=True)
    password = models.CharField(max_length=15)
    conform_password = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    age = models.PositiveIntegerField(null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    qualification = models.CharField(max_length=20)
    user_type = models.SmallIntegerField(choices=STATUS_TYPE,default=2)
    created_date = models.DateTimeField(auto_now_add=True)
    REQUIRED_FIELDS =['password']
    USERNAME_FIELD = 'email'

    objects = UserManager()



class Profile(models.Model):
	user = models.OneToOneField(User_Registration_Model,on_delete=models.CASCADE)
	image = models.ImageField(upload_to='media')


class Comments(models.Model):
    COMMENT_CATEGORY =(
    	(1,'Home'),
    	(2,'Python'),
    	(3,'Django'),
    	(4,'Restapi'),
    	(5,'HTML'),
    	(6,'CSS'),
    	(7,'JS'),
    	(8,'Bootstrap'),
    	(9,'Mysql'),
    	(9,'Mongodb'))
    LIKE_CHOICES = (
    	(1,'comment_like'),
    	(2,'comment_dislike'),
    	(3,'comment_reply_like'),
    	(4,'comment_reply_dislike'))
    comment = models.TextField()
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    comment_category = models.SmallIntegerField(choices=COMMENT_CATEGORY)
    user = models.ForeignKey(User_Registration_Model,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

class Comment_Reply(models.Model):
    reply_comment = models.TextField()
    comment = models.ForeignKey(Comments,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ManyToManyField(User_Registration_Model)

    def __str__(self):
        return self.reply_comment

class Chatting(models.Model):
    user = models.ForeignKey(User_Registration_Model,on_delete=models.CASCADE,null=True)
    chat = models.CharField(max_length=100)

    def __str__(self):
        return self.chat