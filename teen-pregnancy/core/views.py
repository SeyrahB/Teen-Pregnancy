from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Resource, ForumPost, Resource, ForumPost
from .forms import ResourceForm, ForumPostForm, CommentForm, SignUpForm, SearchForm,LoginForm
from django.contrib.auth import login, authenticate


# Home page view
def home(request):
    resources = Resource.objects.all()
    forum_posts = ForumPost.objects.all()
    return render(request, 'home.html', {'resources': resources, 'forum_posts': forum_posts})

# Resource detail view
def resource_detail(request, resource_id):
    resource = Resource.objects.get(id=resource_id)
    return render(request, 'resource_detail.html', {'resource': resource})

# Forum post detail view
def forum_post_detail(request, post_id):
    post = ForumPost.objects.get(id=post_id)
    return render(request, 'forum_post_detail.html', {'post': post})

# View to submit a new resource
def submit_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ResourceForm()
    return render(request, 'submit_resource.html', {'form': form})

# View to submit a new forum post
def submit_forum_post(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ForumPostForm()
    return render(request, 'submit_forum_post.html', {'form': form})

def forum_post_detail(request, post_id):
    post = ForumPost.objects.get(id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user  # Automatically associate with logged-in user
            new_comment.post = post
            new_comment.save()
            return redirect('forum_post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'forum_post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def search(request):
    form = SearchForm(request.GET)
    resources = Resource.objects.none()
    forum_posts = ForumPost.objects.none()

    if form.is_valid():
        query = form.cleaned_data['query']
        resources = Resource.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        forum_posts = ForumPost.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))

    return render(request, 'search_results.html', {
        'form': form,
        'resources': resources,
        'forum_posts': forum_posts
    })

# User registration view
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# User login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the homepage after successful login
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# User logout view
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')

# User registration view
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# User login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the homepage after successful login
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# User logout view
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')

# core/views.py

def search(request):
    query = request.GET.get('q', '')
    resources = Resource.objects.filter(title__icontains=query)
    forum_posts = ForumPost.objects.filter(title__icontains=query)
    return render(request, 'search_results.html', {'resources': resources, 'forum_posts': forum_posts, 'query': query})
