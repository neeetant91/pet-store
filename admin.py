from django.contrib import admin
from petapp.models import Petstore,Cart,Buy
# Register your models here.
admin.site.register(Petstore)
admin.site.register(Cart)
admin.site.register(Buy)


from django.contrib.sessions.models import Session

admin.site.register(Session)