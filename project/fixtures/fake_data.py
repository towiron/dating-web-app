from django.contrib.auth import get_user_model
from user_app.models import Profile
from django.core.files.uploadedfile import UploadedFile
import os
import random
from faker import Faker
fake = Faker()


boys_path = "/Users/batyrshirmatov/Documents/images/boys"
girls_path = "/Users/batyrshirmatov/Documents/images/girls"

boys_files=os.listdir(boys_path)
girls_files=os.listdir(girls_path)

for i in range(1, 300):
	f_name = fake.first_name()
	l_name = fake.last_name()
	user = get_user_model().objects.create_user(
        username=f'{f_name}_{i}',
        password=f'{fake.last_name()}{random.randrange(1236487, 1234012934219)}{fake.first_name()}',
        first_name=f_name,
        last_name=l_name,
    )
	profile = Profile.objects.get(id = i)
	profile.age = random.randrange(18, 30)
	profile.sex = random.choice(['M', 'F'])
	profile.seeking = random.choice(['M', 'F'])
	profile.about = fake.text()
	profile.city = f'{fake.city()} {fake.country()}'
	profile.last_name = fake.last_name()
	if profile.sex == 'M':
		profile.first_name = fake.first_name_male()
		profile.profile_pic.save('profile_pic.png', UploadedFile(file=open(f'{boys_path}/{random.choice(boys_files)}', 'rb'), content_type='image/png'))
	else:
		profile.first_name = fake.first_name_female()
		profile.profile_pic.save('profile_pic.png', UploadedFile(file=open(f'{girls_path}/{random.choice(girls_files)}', 'rb'), content_type='image/png'))








# from user_app.models import Profile
# from django.core.files.uploadedfile import UploadedFile
# import os
# import random
# from faker import Faker
# fake = Faker()


# profile = Profile.objects.get(user_id = 100)
# profile.age = random.randrange(18, 30)
# profile.about = fake.text()
# profile.city = f'{fake.city()} {fake.country()}'
# profile.last_name = fake.last_name()
# profile.save()

