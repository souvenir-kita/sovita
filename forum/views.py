from django.shortcuts import get_object_or_404, redirect, render

from display.models import Product
from forum.forms import PostForm, ReplyForm
from forum.models import Post, Reply


def get_forum_posts(request, product_id):
    posts = Post.objects.filter(product=product_id)
    return render(request, "forum_posts.html", {"product_id": product_id, "posts": posts})


def get_forum_post(request, product_id, post_id):
    post = Post.objects.get(pk=post_id)
    replies = Reply.objects.filter(post=post_id)
    return render(request, "forum_post.html", {"post": post, "replies": replies})


def create_forum_post(request, product_id):
    post_form = PostForm(request.POST or None)
    if post_form.is_valid() and request.method == "POST":
        post = post_form.save(commit=False)
        post.user = request.user
        post.product = get_object_or_404(Product, pk=product_id)
        post.save()
        return redirect("forum:forum_posts", product_id=product_id)
    return render(request, "create_forum_post.html", {"form": post_form})


def update_forum_post(request, product_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_form = PostForm(request.POST or None, instance=post)
    if post_form.is_valid() and request.method == "POST":
        post_form.save()
        return redirect("forum:forum_posts", product_id=product_id)
    return render(request, "edit_forum_post.html", {"form": post_form})


def delete_forum_post(request, product_id, post_id):
    get_object_or_404(Post, pk=post_id).delete()
    return redirect("forum:forum_posts", product_id=product_id)


def create_forum_post_reply(request, product_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    replies = Reply.objects.filter(post=post_id)
    reply_form = ReplyForm(request.POST or None)
    if reply_form.is_valid() and request.method == "POST":
        reply = reply_form.save(commit=False)
        reply.user = request.user
        reply.post = post
        reply.save()
        return redirect("forum:forum_post", product_id=product_id, post_id=post_id)
    return render(
        request,
        "create_forum_post_reply.html",
        {"form": reply_form, "post": post, "replies": replies},
    )


def update_forum_post_reply(request, product_id, post_id, reply_id):
    post = get_object_or_404(Post, pk=post_id)
    reply = get_object_or_404(Reply, pk=reply_id)
    replies = Reply.objects.filter(post=post_id)
    reply_form = ReplyForm(request.POST or None, instance=reply)
    if reply_form.is_valid() and request.method == "POST":
        reply_form.save()
        return redirect("forum:forum_post", product_id=product_id, post_id=post_id)
    return render(
        request,
        "edit_forum_post_reply.html",
        {"form": reply_form, "post": post, "replies": replies},
    )


def delete_forum_post_reply(request, product_id, post_id, reply_id):
    get_object_or_404(Reply, pk=reply_id).delete()
    print("executed")
    return redirect("forum:forum_post", product_id=product_id, post_id=post_id)
