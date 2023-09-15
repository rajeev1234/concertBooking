from django.contrib.auth.decorators import login_required #the login_required decorator
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from booking.models import User
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from .forms import UserSignUpForm, ArtistSignUpForm
from booking.decorators import artist_required, user_required
from booking.models import *
from django.contrib.admin.widgets import AdminDateWidget

# Create your views here.



class SignUpView(TemplateView):
    template_name = 'registration/signup.html'
    

def home(request):
    if request.user.is_authenticated:
        if request.user.is_artist:
            return redirect('concert_change_list')
        else:
            return redirect('user_concert_list')
    context = {'concert':Concert.objects.all()}
    return render(request, 'home.html',context)


class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'user'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('user_concert_list')
    

class ArtistSignUpView(CreateView):
    model = User
    form_class = ArtistSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'artist'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('concert_change_list')
    

@method_decorator([login_required, artist_required], name='dispatch')
class ConcertListView(ListView):
    model = Concert
    ordering = ('title', )
    context_object_name = 'concert'
    template_name = 'template/artist/concert_change_list.html'



@method_decorator([login_required, artist_required], name='dispatch')
class ConcertCreateView(CreateView):
    model = Concert
    fields = ['title','description','location','run_length', 'trailer','image','concert_date','seat']
    template_name = 'template/artist/concert_add_form.html'
    
    def get_form(self, form_class=None):
        form = super(ConcertCreateView, self).get_form(form_class)
        form.fields['concert_date'].widget = AdminDateWidget(attrs={'type': 'date'})
        return form

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.concert = self.request.user
        quiz.save()
        for a in form.cleaned_data['seat']:
             quiz.seat.add(a)
             quiz.save()
        messages.success(self.request, 'The Concert was created with success! Hurray.')
        return redirect('home')
    


@method_decorator([login_required, artist_required], name='dispatch')
class ConcertUpdateView(UpdateView):
    model = Concert
    fields = ['title','description','location','run_length', 'trailer','image','concert_date','seat']
    context_object_name = 'concert'
    template_name = 'template/artist/concert_change_form.html'

    def get_success_url(self):
        return reverse('concert_change_list')
    

@method_decorator([login_required, artist_required], name='dispatch')
class ConcertDeleteView(DeleteView):
    model = Concert
    context_object_name = 'concert'
    template_name = 'template/artist/concert_delete_confirm.html'
    success_url = reverse_lazy('concert_change_list')

    def delete(self, request, *args, **kwargs):
        concert = self.get_object()
        messages.success(request, 'The concert %s was deleted with success!' % concert.title)
        return super().delete(request, *args, **kwargs)
    

class UserConcertListView(ListView):
    model = Concert
    ordering = ('title', )
    context_object_name = 'concert'
    template_name = 'template/user/user_concert_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking = Booking.objects.filter(paid_by = self.request.user)
        context['booking'] = booking  # this line added
        return context


