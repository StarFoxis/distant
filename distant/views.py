from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import CreateView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy 

from django.core.exceptions import ObjectDoesNotExist

from .models import assignment_dates, homework
from .forms import TasksForm

class TasksListView(ListView):
    model = assignment_dates
    context_object_name = 'dates'
    template_name = 'distant/tasks_list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        tasks = self.request.GET.get('id', None)
        if tasks:
            data['tasks'] = homework.objects.filter(date=tasks)
        else:
            data['tasks'] = homework.objects.filter(date=assignment_dates.objects.first())
        return data

    def get_queryset(self):
        dates = assignment_dates.objects.all()
        # Отбираем первые 10 статей
        paginator = Paginator(dates, 6)
        page = self.request.GET.get('page')
        try:
            dates = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            dates = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            dates = paginator.page(paginator.num_pages)
        return dates

class CreateTaskView(CreateView):
    model = homework
    form_class = TasksForm
    # fields = ['date', 'num_task', 'text_task', 'answer_task']
    template_name = 'distant/create_task.html'
    success_url = 'tasks' # Паскуда

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        if request.user.is_staff:
            return render(request, self.template_name, self.get_context_data())
        return redirect('/')

        def form_valid(self, form):
            homework.objects.create(**form.cleaned_data)
            suc = self.get_success_url()
            return redirect(suc)
        
        def get_success_url(self):  # Тварина. Я на тебя потратил 2 часа времени
            return reverse_lazy('tasks')

class UpdateTaskView(UpdateView):
    model = homework
    fields = ['num_task', 'text_task', 'answer_task']
    template_name = 'distant/update_task.html'
    success_url = 'tasks'
        
    def get_success_url(self):
        return reverse_lazy('tasks')
    
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        if request.user.is_staff:
            return render(request, self.template_name, self.get_context_data())
        return redirect('/')

class DeleteTaskView(DeleteView):
    model = homework
    context_object_name = 'task'
    template_name = 'distant/delete_task.html'
    success_url = reverse_lazy('tasks')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        if request.user.is_staff:
            return render(request, self.template_name, self.get_context_data())
        return redirect('/')

class CreateDateView(CreateView):
    model = assignment_dates
    fields = ['date']
    template_name = 'distant/create_date.html'
    success_url = 'create'

    def post(self, request, *argv, **kwargs):
        response = super().post(request, *argv, **kwargs)
        print(request.POST)
        return response

    def get_success_url(self):  
            return reverse_lazy('create')

class DeleteDateView(DeleteView):
    model = assignment_dates
    context_object_name = 'date'
    template_name = 'distant/delete_date.html'
    success_url = reverse_lazy('tasks')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        if request.user.is_staff:
            return render(request, self.template_name, self.get_context_data())
        return redirect('/')

def get_info(request):
    if request.method == 'POST':
        try:
            style = Style.objects.get(id=request.user.style.id) 
            style.style = not style.style
            style.save()
        except:
            Style.objects.create(user_id=request.user.id, style=True).save()

        return redirect(request.path)
    return render(request, 'distant/info.html', {})