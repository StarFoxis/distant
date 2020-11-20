from django.contrib import admin
from .models import assignment_dates, homework

# admin.site.register(assignment_dates)

class HomeworkInline(admin.TabularInline):
    model = homework
    extra = 0

@admin.register(assignment_dates)
class assignment_datesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date')
    inlines = [HomeworkInline]

@admin.register(homework)
class homeworkAdmin(admin.ModelAdmin):
    list_display = ('num_task', 'date')
    fields = [('num_task', 'date'), 'text_task', 'answer_task']