
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from .validators import validate_file_size

def user_directory_path(instance, filename):
    # Файлы загрузятся в MEDIA_ROOT/user_images/username/<filename>
    return 'user_images/{0}/{1}'.format(instance.user.username, filename)

class Profile(models.Model):
    class SexOptions(models.TextChoices):
        MALE = 'M', ('Male')
        FEMALE = 'F', ('Female')
    

    class ThemeOptions(models.TextChoices):
        LIGHT = 'L', ('Light')
        DARK = 'D', ('Dark')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    profile_pic = models.ImageField(default='ava.jpg', upload_to=user_directory_path, blank=True, validators=[validate_file_size])
    banner = models.ImageField(default='banner.jpg', upload_to=user_directory_path, blank=True, validators=[validate_file_size])
    age = models.PositiveIntegerField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SexOptions.choices, blank=True, null=True) 
    seeking = models.CharField(max_length=1, choices=SexOptions.choices, blank=True, null=True) 
    about = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    online_status = models.BooleanField(null=True, blank=True, default=False)
    theme = models.CharField(max_length=1, choices=ThemeOptions.choices, blank=True, null=True) 
    def __str__(self):
        return self.user.username
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 700 or img.width > 700:
            output_size = (700, 700)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)
        
        img = Image.open(self.banner.path)

        if img.height > 1200 or img.width > 1200:
            output_size = (1200, 1200)
            img.thumbnail(output_size)
            img.save(self.banner.path)