from cProfile import Profile
from django.contrib import admin


from loginPage.models import SchoolUser

# Register your models here.
admin.site.register(SchoolUser)
