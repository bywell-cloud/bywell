from django.contrib import admin
from .models import *


# Register your models here.

admin.site.register(User)

class ListAdmin(admin.ModelAdmin):
   # list_display= ['']
   list_filter = ['status','close']
   prepopulated_fields = {'p_slug':['p_name']}
   exclude= ('p_period',)   

admin.site.register(List , ListAdmin)  
#admin.site.register(Category)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name']}


admin.site.register(Whistlistx)
admin.site.register(Comment)
