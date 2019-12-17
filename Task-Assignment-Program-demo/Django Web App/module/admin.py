from django.contrib import admin
from .models import RecordedTask, advisor, task

admin.site.register(RecordedTask)
admin.site.register(advisor)
admin.site.register(task)
admin.site.site_header = "Frontdesk Helper Admin"
admin.site.index_title = "Frontdesk Helper Admin"
admin.site.site_title = ""
admin.site.site_title = ""