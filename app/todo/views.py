from todo.models import Task
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import FormView

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView


from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    fields = '__all__'
    template_name = 'todo/login.html'

    def get_success_url(self):
        return reverse_lazy('todo:index') 


class UserRegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'todo/register.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('todo:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super(UserRegisterView, self).form_valid(form)


class TasksListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'todo/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(TasksListView, self).get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(user=self.request.user)
        context["count"] = len(Task.objects.filter(user=self.request.user, complete=0))
       
        search_input = self.request.GET.get("search-area") or ""

        if search_input:
            context["tasks"] = Task.objects.filter(title__startswith=search_input)

        context["search_input"] = search_input
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description", "complete"]
    template_name = 'todo/create.html'
    context_object_name = 'form'
    success_url = reverse_lazy('todo:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskEditView(LoginRequiredMixin, UpdateView):
    model = Task 
    fields = ["title", "description", "complete"]
    template_name = 'todo/edit.html'
    success_url = reverse_lazy('todo:index')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task 
    template_name = 'todo/delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('todo:index') 