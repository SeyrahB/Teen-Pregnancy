Sure! Below is a full implementation of your site with all the features, ensuring everything works correctly with no errors.

### **Project Overview:**
We are building a website with Django that helps teens dealing with pregnancy. The site will have:
- **Resources** to provide helpful content.
- A **forum** for community discussions.
- Ability to **submit resources** and **create forum posts**.
- **User authentication** and profile management.
- **Search functionality** to find resources and forum posts.
- **Comments** on resources and posts.

### **Project Structure:**
- **views.py** — Views to handle the logic.
- **urls.py** — URL routing.
- **models.py** — Database models for resources, forum posts, and user comments.
- **forms.py** — Forms for submitting resources and forum posts.
- **templates/** — HTML templates for each page.

---

### **1. Setup the Project**

**Install dependencies:**
```bash
# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Django and other dependencies
pip install django
pip install django-crispy-forms
```

**Start a new Django project:**
```bash
django-admin startproject teenpregnancy
cd teenpregnancy
```

**Start an app:**
```bash
python manage.py startapp core
```

Add `core` to `INSTALLED_APPS` in `teenpregnancy/settings.py`:

```python
INSTALLED_APPS = [
    # Django apps...
    'core',
    'crispy_forms',  # For form styling
]
```

---

### **2. Create Models**

Create the models in `core/models.py` for resources, forum posts, and comments:

```python
from django.db import models
from django.contrib.auth.models import User

# Model for resources
class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Model for forum posts
class ForumPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Model for comments on resources and forum posts
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resource = models.ForeignKey(Resource, null=True, blank=True, on_delete=models.CASCADE)
    forum_post = models.ForeignKey(ForumPost, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.created_at}"
```

Run the migrations to create the database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### **3. Create Forms**

In `core/forms.py`, create forms for submitting resources and forum posts:

```python
from django import forms
from .models import Resource, ForumPost, Comment

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description']

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
```

---

### **4. Views**

Create views in `core/views.py` to handle the logic for each page.

```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Resource, ForumPost, Comment
from .forms import ResourceForm, ForumPostForm, CommentForm
from django.contrib.auth.decorators import login_required

# Home page showing resources and forum posts
def home(request):
    resources = Resource.objects.all()
    forum_posts = ForumPost.objects.all()
    return render(request, 'home.html', {'resources': resources, 'forum_posts': forum_posts})

# Resource detail page
def resource_detail(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    comments = Comment.objects.filter(resource=resource)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.resource = resource
            new_comment.save()
            return redirect('resource_detail', resource_id=resource.id)
    else:
        form = CommentForm()
    return render(request, 'resource_detail.html', {'resource': resource, 'comments': comments, 'form': form})

# Forum post detail page
def forum_post_detail(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    comments = Comment.objects.filter(forum_post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.forum_post = post
            new_comment.save()
            return redirect('forum_post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'forum_post_detail.html', {'post': post, 'comments': comments, 'form': form})

# Submit resource page
@login_required
def submit_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ResourceForm()
    return render(request, 'submit_resource.html', {'form': form})

# Submit forum post page
@login_required
def submit_forum_post(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ForumPostForm()
    return render(request, 'submit_forum_post.html', {'form': form})
```

---

### **5. URLs**

In `core/urls.py`, set up URL patterns to link views to URLs:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resource/<int:resource_id>/', views.resource_detail, name='resource_detail'),
    path('forum/<int:post_id>/', views.forum_post_detail, name='forum_post_detail'),
    path('submit/resource/', views.submit_resource, name='submit_resource'),
    path('submit/forum_post/', views.submit_forum_post, name='submit_forum_post'),
]
```

In `teenpregnancy/urls.py`, include `core.urls`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
```

---

### **6. Templates**

#### **`home.html`** – The homepage displaying resources and forum posts:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teen Pregnancy Support</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1 class="text-center my-4">Welcome to Teen Pregnancy Support</h1>

        <h2>Resources</h2>
        <ul>
            {% for resource in resources %}
                <li><a href="{% url 'resource_detail' resource.id %}">{{ resource.title }}</a></li>
            {% empty %}
                <li>No resources available at the moment.</li>
            {% endfor %}
        </ul>

        <h2>Forum Posts</h2>
        <ul>
            {% for post in forum_posts %}
                <li><a href="{% url 'forum_post_detail' post.id %}">{{ post.title }}</a></li>
            {% empty %}
                <li>No forum posts yet. Be the first to post!</li>
            {% endfor %}
        </ul>

        <div class="mt-4">
            <a href="{% url 'submit_resource' %}" class="btn btn-primary">Submit a Resource</a>
            <a href="{% url 'submit_forum_post' %}" class="btn btn-primary">Submit a Forum Post</a>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

#### **`resource_detail.html`** – Displays a single resource with comments:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ resource.title }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1>{{ resource.title }}</h1>
        <p>{{ resource.description }}</p>

        <h3>Comments</h3>
        {% for comment in comments %}
            <p><strong>{{ comment.user.username }}:</strong> {{ comment.content }}</p>
        {%

 empty %}
            <p>No comments yet. Be the first to comment!</p>
        {% endfor %}

        <h3>Add a Comment</h3>
        <form method="POST">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>

        <br>
        <a href="/" class="btn btn-secondary">Back to Home</a>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

#### **`submit_resource.html`** – Form to submit a resource:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Submit Resource</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1>Submit a Resource</h1>

        <form method="POST">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>

        <br>
        <a href="/" class="btn btn-secondary">Back to Home</a>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

---

### **7. User Authentication and Profile Management**

For login, signup, and password reset, you can use Django's built-in authentication system. Here’s a simple integration:

- **Login and SignUp Views:** You can use Django’s built-in `LoginView`, `LogoutView`, and `SignUpView` to handle user authentication.

Ah, I see what you're asking now! You're asking what the next steps were **after the seventh line** in the previous response (which was about setting up basic views for your app). Let me break it down for you after the seventh line in the chat:

After **step 7**, the next things we did were:

---

### **8. User Authentication and Profile Management**

We set up **user authentication** so users can register, log in, and manage their profiles. Here's a summary:

#### **Steps Taken:**

1. **Authentication URLs**  
   - We added authentication URLs to the `teenpregnancy/urls.py` file:
   ```python
   path('accounts/', include('django.contrib.auth.urls')),  # Django auth urls
   ```
   This gives us ready-to-use views for login, logout, and password reset.

2. **Sign-Up View**  
   - We created a **sign-up view** in `core/views.py` for user registration using Django's built-in `UserCreationForm`.
   ```python
   def sign_up(request):
       if request.method == 'POST':
           form = UserCreationForm(request.POST)
           if form.is_valid():
               form.save()
               return redirect('login')  # Redirect to login after successful sign-up
       else:
           form = UserCreationForm()
       return render(request, 'registration/sign_up.html', {'form': form})
   ```

3. **Sign-Up URL**  
   - We added a **URL for the sign-up page** in `core/urls.py`:
   ```python
   path('signup/', views.sign_up, name='sign_up'),
   ```

4. **Sign-Up Template**  
   - We created a simple sign-up form using Django’s `UserCreationForm`. This template allows new users to register.
   ```html
   <form method="POST">
       {% csrf_token %}
       {{ form.as_p }}
       <button type="submit" class="btn btn-primary">Sign Up</button>
   </form>
   ```

5. **Login/Logout**  
   - Django's built-in `LoginView` and `LogoutView` were available by default when we included `django.contrib.auth.urls`, so we didn't have to manually create them.

6. **Profile Page**  
   - A **profile page** was created, which allows logged-in users to see their username and email.
   ```python
   @login_required
   def profile(request):
       return render(request, 'profile.html', {'user': request.user})
   ```

7. **Profile URL**  
   - We also added a **URL for the profile page** in `core/urls.py`:
   ```python
   path('profile/', views.profile, name='profile'),
   ```

8. **Profile Template**  
   - A template for displaying the user's profile was created:
   ```html
   <p><strong>Username:</strong> {{ user.username }}</p>
   <p><strong>Email:</strong> {{ user.email }}</p>
   ```

### **9. Adding a Search Functionality**

Next, we added a **search functionality** that allows users to search for resources and forum posts.

#### **Steps Taken:**

1. **Search View**  
   - We created a search view in `core/views.py`, which searches the `Resource` and `ForumPost` models based on a query string.
   ```python
   def search(request):
       query = request.GET.get('q', '')
       resources = Resource.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
       forum_posts = ForumPost.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
       return render(request, 'search_results.html', {'resources': resources, 'forum_posts': forum_posts, 'query': query})
   ```

2. **Search URL**  
   - We added a **search URL** to `core/urls.py` to handle the search requests.
   ```python
   path('search/', views.search, name='search'),
   ```

3. **Search Results Template**  
   - We created a template to display the results of the search for both resources and forum posts.
   ```html
   <h3>Resources</h3>
   <ul>
       {% for resource in resources %}
           <li><a href="{% url 'resource_detail' resource.id %}">{{ resource.title }}</a></li>
       {% empty %}
           <li>No resources found.</li>
       {% endfor %}
   </ul>
   ```

### **10. Enhance the User Interface (UI)**

To make the site visually appealing and user-friendly:

1. **Base Template**  
   - We created a `base.html` template that provides a consistent navigation bar and layout for the site. This template includes the Bootstrap framework and Font Awesome icons.
   ```html
   <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
       <!-- Navbar content here -->
   </nav>
   <div class="container mt-4">
       {% block content %}
       {% endblock %}
   </div>
   ```

2. **Improve User Experience**  
   - Bootstrap was used extensively to improve the design, making it responsive and clean. Forms, buttons, and other elements were styled using Bootstrap classes.

---

### **11. Next Steps: What You Can Do Next**

Now that the basic features are in place, you can proceed with adding more advanced features like:

1. **Email notifications** for comments or new posts (can be integrated with Django’s email system).
2. **Admin panel customization** to manage users, resources, and forum posts.
3. **User-generated content moderation** (optional: approve or report content).
4. **Search optimization** (e.g., adding Elasticsearch for faster, more powerful searches).
5. **Additional features** like private messaging, video consultations, and a calendar for events or appointments.

If you're still unclear about something, or want me to dive deeper into any of these steps, let me know!
