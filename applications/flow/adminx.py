import xadmin
from .models import Process, Category


class ProcessAdmin(object):
    list_display = ['id', 'name', 'description', 'run_type']
    list_filter = ['id', 'name', 'description']
    search_fields = ['id', 'name', 'description']
    list_editable = ['name', 'description']
    list_display_links = ['id']
    model_icon = 'fa fa-user-circle-o'


class CategoryAdmin(object):
    list_display = ['id', 'name']
    list_filter = ['name']
    search_fields = ['id', 'name']
    list_editable = ['name']
    list_display_links = ['id']
    model_icon = 'fa fa-user-circle-o'


xadmin.site.register(Process, ProcessAdmin)
xadmin.site.register(Category, CategoryAdmin)
