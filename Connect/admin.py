from django.contrib import admin

from .models import *

admin.site.register(UserDatabase)
admin.site.register(Connections)
admin.site.register(Company_Model)
admin.site.register(Blogs_Model)
admin.site.register(BlogLikes)
