from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView
from django.http import HttpResponse, Http404
from django.views.generic import View
from django.views.generic.base import TemplateView, TemplateResponseMixin, ContextMixin
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Book
from .forms import BookForm


class MultipleObjectMixin(object):
    def get_object(self, queryset=None, *args, **kwargs):
        slug = self.kwargs.get("slug")
        if slug:
            try:
                obj = self.model.objects.get(slug=slug)
            except self.model.MultipleObjectsReturned:
                obj = self.get.queryset().first()
            except:
                raise Http404
        return obj
    raise Http404

class BookDeleteView(DeleteView):
    model = Book

    def get_success_url(self):
        return reverse("book_list")

class BookCreateView(CreateView):
    # model = Book
    template_name = "forms.html"
    form_class = BookForm
    # success_url = "/"
    def form_valid(self, form):
        form.instance.added_by = self.request.user
        # form.instance.last_edited_by = self.request.user
        return super(BookCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("book_list")
    
class BookUpdateView(MultipleObjectMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "forms.html"

class BookDetail(DetailView):
    model = Book

    def get_object(self, queryset=None, *args, **kwargs):
        slug = self.kwargs.get("slug")
        if slug:
            try:
                obj = self.model.objects.get(slug=slug)
            except self.model.MultipleObjectsReturned:
                obj = self.get.queryset().first()
            except:
                obj = None
            return obj
        return None

class BookListView(ListView):
    model = Book
    #
    # def get_queryset(self, *args, **kwargs):
    #     qs = super(BookListView, self).get_queryset(*args, **kwargs).order_by("-id")
    #     # print(qs)
    #     # return qs

    # def get_context_data(self, *args, **kwargs):
    #     context = super(BookDetail, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)

class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "about.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data(*args, **kwargs)
        context["title"] = "This is about us"
        return context

class MyView(LoginRequiredMixin, ContextMixin, TemplateResponseMixin, View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["title"] = "Some other title"
        return self.render_to_response(context)
    #
    # @method_decorator(login_required)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(MyView, self).dispatch(request, *args, **kwargs)
