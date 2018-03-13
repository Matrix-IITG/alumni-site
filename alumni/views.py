from django.shortcuts import render ,get_object_or_404 ,redirect
from django.template.defaultfilters import length
from django.utils import timezone
from .models import Post,Comment,Alumni
from .forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required,permission_required
from django.db.models import Q

########### alumni view start

@login_required
def alumni_list(request):
    alumnis=Alumni.objects.all()
    unapprovedposts = Post.objects.filter(approved_post=False).order_by('created_date')
    unpublishedposts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    if len(unapprovedposts) - len(unpublishedposts) >= 0:
        approvalpending = len(unapprovedposts) - len(unpublishedposts)
    else:
        approvalpending = 0
    # search request result
    query = request.GET.get("q")
    if query:
        alumnis=alumnis.filter(
            Q(name__icontains=query)
            ).distinct()
        return render(request, 'alumni/alumni_list.html', {'alumnis': alumnis, 'approvalpending': approvalpending})
    return render(request, 'alumni/alumni_list.html', {'alumnis': alumnis, 'approvalpending': approvalpending})

@login_required
def alumni_detail(request ,pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    unapprovedposts = Post.objects.filter(approved_post=False).order_by('created_date')
    unpublishedposts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    if len(unapprovedposts) - len(unpublishedposts) >= 0:
        approvalpending = len(unapprovedposts) - len(unpublishedposts)
    else:
        approvalpending = 0
    return render(request, 'alumni/alumni_details.html', {'alumni': alumni, 'approvalpending': approvalpending, })
# alumni view end

############ post view start

@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('created_date')
    posts=posts[::-1]#for reversing the array
    unapprovedposts = Post.objects.filter(approved_post=False).order_by('created_date')
    unpublishedposts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.author=request.user
            comment.post=get_object_or_404(Post,pk=request.POST["butt"])
            comment.save()
            return redirect('alumni:post_list')
    else:
        form=CommentForm()        
    if len(unapprovedposts)-len(unpublishedposts)>=0:
        approvalpending=len(unapprovedposts)-len(unpublishedposts)
    else:
        approvalpending=0
    return render(request, 'post/post_list.html', {'form':form,'posts': posts,'approvalpending':approvalpending})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            post.save()
            posts = Post.objects.all()
            return redirect('alumni:post_detail', pk=post.pk)
    else:
        form = PostForm()
    unapprovedposts = Post.objects.filter(approved_post=False).order_by('created_date')
    unpublishedposts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    if len(unapprovedposts) - len(unpublishedposts) >= 0:
        approvalpending = len(unapprovedposts) - len(unpublishedposts)
    else:
        approvalpending = 0
    return render(request, 'post/post_edit.html', {'form': form,'approvalpending':approvalpending,})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user_all_post=Post.objects.filter(author=request.user)
    if post in user_all_post:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                # post.published_date = timezone.now()
                post.save()
                unapprovedposts = Post.objects.filter(approved_post=False).order_by('created_date')
                return redirect('alumni:post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        unapprovedposts = Post.objects.filter(approved_post=False).order_by('created_date')
        unpublishedposts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
        if len(unapprovedposts) - len(unpublishedposts) >= 0:
            approvalpending = len(unapprovedposts) - len(unpublishedposts)
        else:
            approvalpending = 0
        return render(request, 'post/post_edit.html', {'form': form,'approvalpending':approvalpending,})
    else:
        return render(request,'post/error.html')    

@login_required
def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    user_all_post=Post.objects.filter(author=request.user)
    user_post=0
    if(post in user_all_post):user_post=1
    unapprovedposts = Post.objects.filter(approved_post=False).order_by('created_date')
    unpublishedposts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    if len(unapprovedposts) - len(unpublishedposts) >= 0:
        approvalpending = len(unapprovedposts) - len(unpublishedposts)
    else:
        approvalpending = 0
    return render(request, 'post/post_details.html', {'post': post,'approvalpending':approvalpending,'user_post':user_post,})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    posts = posts.filter(author = request.user)
    unapprovedposts = Post.objects.filter(approved_post=False).order_by('created_date')
    unpublishedposts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    if len(unapprovedposts) - len(unpublishedposts) >= 0:
        approvalpending = len(unapprovedposts) - len(unpublishedposts)
    else:
        approvalpending = 0
    return render(request, 'post/post_draft_list.html', {'posts': posts,'approvalpending':approvalpending,})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('alumni:post_detail',pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('alumni:post_list')

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('alumni:post_detail' ,pk=post.pk)
    else:
        form = CommentForm()
    unapprovedposts = Post.objects.filter(approved_post=False).order_by('created_date')
    unpublishedposts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    if len(unapprovedposts) - len(unpublishedposts) >= 0:
        approvalpending = len(unapprovedposts) - len(unpublishedposts)
    else:
        approvalpending = 0
    return render(request, 'post/add_comment_to_post.html', {'form': form,'approvalpending':approvalpending,})

@login_required
@permission_required('polls.can_vote')
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('alumni:post_detail', pk=comment.post.pk)

@login_required
@permission_required('polls.can_vote')
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('alumni:post_detail' ,pk=comment.post.pk)

@login_required
@permission_required('polls.can_vote')
def post_approval(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('created_date')
    unapprovedposts = Post.objects.filter(approved_post=False).order_by('created_date')
    unpublishedposts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    if len(unapprovedposts) - len(unpublishedposts) >= 0:
        approvalpending = len(unapprovedposts) - len(unpublishedposts)
    else:
        approvalpending = 0
    return render(request, 'post/post_approval.html', {'posts': posts,'approvalpending':approvalpending,})

@login_required
@permission_required('polls.can_vote')
def post_approve(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.approve()
    posts = Post.objects.filter(published_date__isnull=False).order_by('created_date')
    unapprovedposts = Post.objects.filter(approved_post=False).order_by('created_date')
    unpublishedposts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    if len(unapprovedposts) - len(unpublishedposts) >= 0:
        approvalpending = len(unapprovedposts) - len(unpublishedposts)
    else:
        approvalpending = 0
    return render(request, 'post/post_list.html', {'posts': posts,'approvalpending':approvalpending,})


@login_required
@permission_required('polls.can_vote')
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    posts = Post.objects.filter(published_date__isnull=False).order_by('created_date')
    unapprovedposts = Post.objects.filter(approved_post=False).order_by('created_date')
    unpublishedposts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    if len(unapprovedposts) - len(unpublishedposts) >= 0:
        approvalpending = len(unapprovedposts) - len(unpublishedposts)
    else:
        approvalpending = 0
    return render(request, 'post/post_list.html', {'posts': posts,'approvalpending':approvalpending})


#post view end


