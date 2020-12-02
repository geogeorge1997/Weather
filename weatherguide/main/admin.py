from django.contrib import admin
from .models import  CurrentAttributes,Hour24Attributes,WeeklyAttributes

# Register your models here.

# Me : To manage the models by admin,it should register


admin.site.register(CurrentAttributes)
admin.site.register(Hour24Attributes)
admin.site.register(WeeklyAttributes)

