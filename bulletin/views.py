from django.views.generic import ListView, DetailView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Bulletin, Response
from .forms import BulletinForm, ResponseForm
from django.db.models import Q
from django.views.generic import View, DeleteView, UpdateView
from django.urls import reverse
from .tasks import send_response_notification, send_response_accepted_notification


class BulletinListView(ListView):
    """Список всех объявлений"""
    model = Bulletin
    template_name = 'bulletin/bulletin_list.html'
    context_object_name = 'bulletins'
    paginate_by = 10
    ordering = ['-created_at']

class BulletinDetailView(DetailView):
    model = Bulletin
    template_name = 'bulletin/bulletin_detail.html'
    context_object_name = 'bulletin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['response_form'] = ResponseForm()
        return context

class BulletinCreateView(LoginRequiredMixin, CreateView):
    """Создание нового объявления"""
    model = Bulletin
    form_class = BulletinForm
    template_name = 'bulletin/bulletin_form.html'
    success_url = reverse_lazy('bulletin_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BulletinUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование объявления (только автор)"""
    model = Bulletin
    form_class = BulletinForm
    template_name = 'bulletin/bulletin_form.html'
    
    def test_func(self):
        bulletin = self.get_object()
        return bulletin.author == self.request.user
    
    def get_success_url(self):
        return reverse_lazy('bulletin_detail', kwargs={'pk': self.object.pk})
    
class ResponseCreateView(LoginRequiredMixin, CreateView):
    """Создание отклика на объявление"""
    model = Response
    form_class = ResponseForm
    template_name = 'bulletin/response_form.html'
    
    def form_valid(self, form):
        bulletin = get_object_or_404(Bulletin, pk=self.kwargs['pk'])
        form.instance.bulletin = bulletin
        form.instance.author = self.request.user
        response = form.save()  # сохраняем и получаем объект
    
        # Теперь отправляем задачу с ID сохранённого объекта
        send_response_notification.delay(response.id)
    
        messages.success(self.request, 'Отклик успешно отправлен!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('bulletin_detail', kwargs={'pk': self.kwargs['pk']})
    
class MyResponsesView(LoginRequiredMixin, ListView):
    """Страница с откликами на объявления текущего пользователя"""
    model = Response
    template_name = 'bulletin/my_responses.html'
    context_object_name = 'responses'
    paginate_by = 20
    
    def get_queryset(self):
        # Показываем отклики только на объявления текущего пользователя
        return Response.objects.filter(bulletin__author=self.request.user).select_related('bulletin', 'author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаём список объявлений пользователя для фильтрации
        context['my_bulletins'] = Bulletin.objects.filter(author=self.request.user)
        return context
    
class ResponseAcceptView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Принятие отклика"""
    def test_func(self):
        response = get_object_or_404(Response, pk=self.kwargs['pk'])
        return response.bulletin.author == self.request.user
    
    def post(self, request, *args, **kwargs):
        response = get_object_or_404(Response, pk=self.kwargs['pk'])
        response.accepted = True
        response.save()
        send_response_accepted_notification.delay(response.id)
        messages.success(request, 'Отклик принят')
        return redirect('my_responses')
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ResponseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление отклика"""
    model = Response
    template_name = 'bulletin/response_confirm_delete.html'
    
    def test_func(self):
        response = self.get_object()
        return response.bulletin.author == self.request.user
    
    def get_success_url(self):
        messages.success(self.request, 'Отклик удалён')
        return reverse('my_responses')
