from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
import datetime

# Create your models here.

class FakeLeg(models.Model):
	stateChoice = (
		('NSW', 'New South Wales'),
		('VIC', 'Victoria'),
		('QLD', 'Queensland'),
		('TAS', 'Tasmania'),
		('SA', 'South Australia'),
		('WA', 'Western Australia'),
		('ACT', 'Australian Capital Territory'),
		('NT', 'Northern Territory'),
	)
	UID = models.IntegerField()
	suburb = models.CharField(max_length=50)
	state = models.CharField(max_length=3, choices=stateChoice)
	st_name = models.CharField(max_length=20, null=True)
	st_number = models.IntegerField(null=True)
	tenant_num = models.IntegerField()
	price = models.IntegerField()
	house_type = models.CharField(max_length=20, null=True)
	pet = models.BooleanField(null=True)
	wifi = models.BooleanField(null=True)
	kitchen = models.BooleanField(null=True)
	laundry = models.BooleanField(null=True)
	park_lot = models.BooleanField(null=True)
	brief_intro = models.CharField(max_length=500, null=True)
	img_url = models.ImageField(upload_to='img', null=True)

class Date(models.Model):
	RID = models.ForeignKey('Guest', on_delete=models.CASCADE, default=1)
	PID = models.ForeignKey('FakeLeg', on_delete=models.CASCADE, default=1)
	booked_date = models.CharField(max_length=20)
	
	class Meta:
		unique_together = ('booked_date', 'PID',)
	
class Guest(models.Model):
	stateChoice = (
		('NSW', 'New South Wales'),
		('VIC', 'Victoria'),
		('QLD', 'Queensland'),
		('TAS', 'Tasmania'),
		('SA', 'South Australia'),
		('WA', 'Western Australia'),
		('ACT', 'Australian Capital Territory'),
		('NT', 'Northern Territory'),
	)
	UID = models.IntegerField(default=1)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	mobile = models.BigIntegerField()
	email = models.EmailField()
	start_date = models.CharField(max_length=20)
	duration = models.IntegerField()
	ID_number = models.IntegerField()
	st_number = models.IntegerField()
	st_name = models.CharField(max_length=20)
	suburb = models.CharField(max_length=50)
	state = models.CharField(max_length=3, choices=stateChoice)
	card_number = models.BigIntegerField()
	PID = models.ForeignKey('FakeLeg', on_delete=models.CASCADE)
	
	class Meta:
		unique_together = ('UID', 'start_date',)
	
class Img(models.Model):
	img_url = models.ImageField(upload_to='img')
	PID = models.ForeignKey('FakeLeg', on_delete=models.CASCADE)

class Comment(models.Model):
	content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	text = models.TextField()
	comment_time = models.DateTimeField(auto_now_add=True, null=True)
	user = models.ForeignKey(User, related_name="comments", on_delete=models.DO_NOTHING)
	# establish the parent node of the original comment. Prepare for the reply function.
	# this is a tree structure to control the reply function
	root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.DO_NOTHING)
	parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.DO_NOTHING)
	reply_to = models.ForeignKey(User, related_name="reply", null=True, on_delete=models.DO_NOTHING)

	def __str__(self):
		return self.text

	class Meta:
		ordering = ['-comment_time']