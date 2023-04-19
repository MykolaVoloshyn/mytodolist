from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task


class CustomLoginView(LoginView):
    template_name = 'todolist/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('main')


class RegisterPage(FormView):
    template_name = 'todolist/registration.html'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse_lazy('main')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todolist/all_tasks.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search_form') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(Q(title__icontains=search_input) | Q(description__icontains=search_input))
        context['search_input'] = search_input
        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description']
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('main')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'todolist/task_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('main')
