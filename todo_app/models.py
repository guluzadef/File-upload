from django.db import models
from base_user.models import MyUser
from todo.settings import DATE_FORMAT

User = MyUser


# Create your models here.
class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    img = models.ImageField(upload_to='fileimage')
    create_date = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f'{self.name} {self.create_date}'


class See(models.Model):
    see_file = models.ForeignKey(File, related_name="files", on_delete=models.CASCADE)
    see_user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_nocomment = models.BooleanField(default=False)
    access_comment = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.see_file} {self.see_file_id}'

