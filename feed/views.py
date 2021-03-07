# from django.shortcuts import render
from django.contrib import messages
from django.views.generic import TemplateView, DetailView, FormView
from .models import Post
from .forms import PostForm


# Create your views here.

class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):  # see ccbv (google) -> TemplateView class
        context = super().get_context_data(**kwargs)  # super will go to the "TemplateView"
        context['posts'] = Post.objects.all().order_by('-id')  # We are looping through all of our objects
        return context


class PostDetailView(DetailView):
    template_name = "detail.html"
    model = Post


# FormView will allows us to upload stuff


class AddPostView(FormView):
    template_name = "new_post.html"
    form_class = PostForm
    success_url = "/"  # homepage

    def dispatch(self, request, *args, **kwargs):
        self.request = request    # We need request for messages in form_valid below --> see FormView in ccbv
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        #  print(form.cleaned_data['text'])
        #  print(form.cleaned_data['image'])    cleaned_data means form was validated, text/image from forms

        #  Create New Post
        new_object = Post.objects.create(
            # imported from .models.py, creating new object with elements as def. in .models.py
            text=form.cleaned_data['text'],
            image=form.cleaned_data['image']
        )
        messages.add_message(self.request, messages.SUCCESS, 'Your post was successful') # this will display only temporary, after refresh it disappears
        return super().form_valid(form)
