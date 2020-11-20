from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy 

from .models import assignment_dates, homework
from registration.models import Style

class TasksListView(ListView):
    model = assignment_dates
    context_object_name = 'dates'
    template_name = 'distant/tasks_list.html'

    def post(self, request, *args, **kwargs):
        try:
            style = Style.objects.get(id=request.user.style.id) 
            style.style = not style.style
            style.save()
        except:
            Style.objects.create(user_id=request.user.id, style=True).save()
        return redirect(request.path)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        tasks = self.request.GET.get('id', None)
        if tasks:
            data['tasks'] = homework.objects.filter(date=tasks)
        else:
            data['tasks'] = homework.objects.filter(date=1)
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
    fields = ['date', 'num_task', 'text_task', 'answer_task']
    template_name = 'distant/create_task.html'
    success_url = 'tasks' # Паскуда

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        if request.user.is_staff:
            return render(request, self.template_name, self.get_context_data())
        return redirect('/')

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        if 'user' in request.POST:
            try:
                style = Style.objects.get(id=request.user.style.id) 
                style.style = not style.style
                style.save()
            except:
                Style.objects.create(user_id=request.user.id, style=True).save()
            return redirect(request.path)
        return redirect('tasks')

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

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        if 'admin' in request.POST:
            try:
                style = Style.objects.get(id=request.user.style.id) 
                style.style = not style.style
                style.save()
            except:
                Style.objects.create(user_id=request.user.id, style=True).save()
            return redirect(request.path)
        return redirect('tasks')

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

    def post(self, request, *args, **kwargs):
        # super().post(request, *args, **kwargs)
        if 'admin' in request.POST:
            try:
                style = Style.objects.get(id=request.user.style.id) 
                style.style = not style.style
                style.save()
            except:
                Style.objects.create(user_id=request.user.id, style=True).save()
            return redirect(request.path)
        else:
            return self.delete(request, *args, **kwargs)
        return redirect('tasks')

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