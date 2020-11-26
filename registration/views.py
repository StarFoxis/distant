from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView

from django.core.exceptions import ObjectDoesNotExist

from .models import Profile, Style
from .forms import ProfileEditForm, UserEditForm

class StyleView(TemplateView):
    template_name = 'style.html'

    def get(self, request, *argv):
        return redirect('/')
    
    def post(self, request, *args, **kwargs):
        try:
            style = Style.objects.get(id=request.user.style.id) 
            style.style = not style.style
            style.save()
        except ObjectDoesNotExist:
            Style.objects.create(user_id=request.user.id, style=True).save()
        return redirect(request.POST.get('late_path'))         

class UserListView(ListView):
    model = User
    template_name = 'users.html'

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        if request.user.is_staff:
            return render(request, self.template_name, self.get_context_data())
        return redirect('/')

class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'person'

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        if request.user.is_staff:
            return render(request, self.template_name, self.get_context_data())
        return redirect('/')

class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get(self, request, *argv, **kwargs):
        try:    
            super().get(request, *argv, **kwargs)
        except ObjectDoesNotExist:
            Profile.objects.create(user=request.user).save()
        return render(request, self.template_name, self.get_context_data())

    def get_context_data(self, *argv, **kwargs):
        context = super().get_context_data(*argv, **kwargs)
        context['profile'] = self.request.user.profile
        return context

def edit(request):
    try:
        if request.method == 'POST':
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