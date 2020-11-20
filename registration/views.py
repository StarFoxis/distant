from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy 

from .models import Profile, Style
from .forms import ProfileEditForm, UserEditForm

@login_required
def profile(request):
    try:
        if request.method == 'POST':
            try:
                style = Style.objects.get(id=request.user.style.id) 
                style.style = not style.style
                style.save()
            except:
                Style.objects.create(user_id=request.user.id, style=True).save()
            return redirect(request.path)
        return render(request, 'profile.html', {'profile': request.user.profile})
    except:
        Profile.objects.create(user=request.user).save()
        return redirect(request.path)

@login_required
def edit(request):
    try:
        if request.method == 'POST':
            if 'user' in request.POST:
                try:
                    style = Style.objects.get(id=request.user.style.id) 
                    style.style = not style.style
                    style.save()
                except:
                    Style.objects.create(user_id=request.user.id, style=True).save()
                return redirect(request.path)
            else:
                user_form = UserEditForm(instance=request.user, data=request.POST)
                profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
                if user_form.is_valid() and profile_form.is_valid():
                    print(dir(profile_form.cleaned_data['avatar']))
                    user_form.save()
                    profile_form.save()
                return redirect('/')
        else:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
            return render(request,
                        'edit.html',
                        {'user_form': user_form,
                        'profile_form': profile_form})       
    except:
        Profile.objects.create(user=request.user).save()
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                    'edit.html',
                    {'user_form': user_form,
                    'profile_form': profile_form})    
         

class UserListView(ListView):
    model = User
    template_name = 'users.html'

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        if request.user.is_staff:
            return render(request, self.template_name, self.get_context_data())
        return redirect('/')

    def post(self, request, *args, **kwargs):
        try:
            style = Style.objects.get(id=request.user.style.id) 
            style.style = not style.style
            style.save()
        except:
            Style.objects.create(user_id=request.user.id, style=True).save()
        return redirect(request.path)

class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'person'

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        if request.user.is_staff:
            return render(request, self.template_name, self.get_context_data())
        return redirect('/')

    def post(self, request, *args, **kwargs):
        try:
            style = Style.objects.get(id=request.user.style.id) 
            style.style = not style.style
            style.save()
        except:
            Style.objects.create(user_id=request.user.id, style=True).save()
        return redirect(request.path)