from django.shortcuts import render, get_object_or_404, redirect
from .models import Post,Comment, Reply
from .forms import PostForm, ReplyForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    context = {
       'post': post, 
       'comments': comments
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_details', post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        comments = CommentForm(request.POST)
        if comments.is_valid():
            comment = comments.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comments = CommentForm()
    return render(request, 'blog/add_comment.html', {'comments': comments})    

def add_reply(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.author = request.user
            reply.save()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = ReplyForm()
    return render(request, 'blog/add_reply.html', {'form': form})
@login_required
def delete_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', comment.post.pk)
    
@login_required   
def delete_reply(request, reply_pk):
    reply = get_object_or_404(Reply, pk=reply_pk)
    if request.method == 'POST':
        reply.delete()
        return redirect('post_detail', pk=reply.comment.post.pk)