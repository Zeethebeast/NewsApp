from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from absotv.models import Post
from .forms import PostForm

# Helper function: restrict access to staff only
def staff_required(user):
    return user.is_staff


def staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # safer
        password = request.POST.get('password')  # safer

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('dashboard_home')

        # Optional: return an error message
        return render(request, 'dashboard/login.html', {
            'error': 'Invalid credentials or not a staff member.'
        })

    return render(request, 'dashboard/login.html')


@login_required(login_url='staff_login')
@user_passes_test(staff_required, login_url='staff_login')
def dashboard_home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'dashboard/dashboard.html', {'posts': posts})


@login_required(login_url='staff_login')
@user_passes_test(staff_required, login_url='staff_login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('dashboard_home')
    else:
        form = PostForm()
    return render(request, 'dashboard/post_create.html', {'form': form})


@login_required(login_url='staff_login')
@user_passes_test(staff_required, login_url='staff_login')
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard_home')

    return render(request, 'dashboard/post_edit.html', {'form': form, 'post': post})


@login_required(login_url='staff_login')
@user_passes_test(staff_required, login_url='staff_login')
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('dashboard_home')

    return render(request, 'dashboard/post_confirm_delete.html', {'post': post})
