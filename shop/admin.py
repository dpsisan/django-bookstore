from django.contrib import admin

# Register your models here.
from .models import Contact
admin.site.register(Contact)

from .models import Book

admin.site.register(Book)