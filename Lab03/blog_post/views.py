from django.shortcuts import render,redirect
from .forms import PostForm,BlockForm
from .models import Post,BlogUser,Block
# Create your views here.


def posts(request):
    blocked_users = Block.objects.filter(blocker__user=request.user).values_list("blocked__user", flat=True)
    visible_posts = Post.objects.get_queryset().exclude(author__user__in=blocked_users)
    context = {"posts":visible_posts}

    return render(request,"posts.html",context)


def add_post(request):
        if request.method == "POST":
            form_data = PostForm(data=request.POST, files=request.FILES)
            if form_data.is_valid():
                post = form_data.save(commit=False)
                post.author = BlogUser.objects.get(user=request.user)
                post.img = form_data.cleaned_data['img']
                post.save()
                return redirect("posts")

        return render(request, "add_post.html", context={"form":PostForm})


def profile(request):
    current_user = BlogUser.objects.get(user=request.user)
    visible_posts = Post.objects.filter(author=current_user)
    context={"posts":visible_posts,"user":current_user}

    return render(request,"profile.html",context)

def blockedUsers(request):
    if request.method == "POST":
        form_data = BlockForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            block = form_data.save(commit=False)
            block.blocker = BlogUser.objects.get(user=request.user)
            block.save()
            return redirect("blockedUsers")

    blocks = Block.objects.filter(blocker__user=request.user)
    blocked_users = BlogUser.objects.filter(user__in=blocks.values_list("blocked__user", flat=True))

    return render(request, "blockedUsers.html", {"form": BlockForm, "blockedUsers": blocked_users})

    return render(request,"blockedUsers.html")

