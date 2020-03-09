from django.contrib import admin
from Quests.models import Quest
# Register your models here.

class QuestAdmin(admin.ModelAdmin):
    list_display=("name","company","genre","stock")
admin.site.register(Quest,QuestAdmin)