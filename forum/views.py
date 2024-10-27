from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from adminview.models import Product
from forum.forms import PostForm
from forum.models import Post, Reply


def get_forum_posts(request, product_id):
    product = Product.objects.get(pk=product_id)
    posts = Post.objects.filter(product=product_id)
    return render(
        request,
        "forum_posts.html",
        {"user": request.user, "product": product, "posts": posts},
    )


def get_forum_post(request, product_id, post_id):
    post = Post.objects.get(pk=post_id)
    replies = Reply.objects.filter(post=post_id)
    return render(
        request, "forum_post.html", {"user": request.user, "post": post, "replies": replies}
    )


@login_required(login_url="authentication:login")
def create_forum_post(request, product_id):
    post_form = PostForm(request.POST or None)
    if post_form.is_valid() and request.method == "POST":
        post = post_form.save(commit=False)
        post.user = request.user
        post.product = get_object_or_404(Product, pk=product_id)
        post.save()
        return redirect("forum:forum_posts", product_id=product_id)
    return render(request, "create_forum_post.html", {"form": post_form})


@login_required(login_url="authentication:login")
def update_forum_post(request, product_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_form = PostForm(request.POST or None, instance=post)
    if post_form.is_valid() and request.method == "POST":
        post_form.save()
        return redirect("forum:forum_posts", product_id=product_id)
    return render(request, "edit_forum_post.html", {"form": post_form})


@login_required(login_url="authentication:login")
def delete_forum_post(request, product_id, post_id):
    get_object_or_404(Post, pk=post_id).delete()
    return redirect("forum:forum_posts", product_id=product_id)


@csrf_exempt
@require_http_methods(["POST"])
@login_required(login_url="authentication:login")
def create_forum_post_reply(request, product_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    content = request.POST.get("content")
    if not content or content.strip() == "":
        return JsonResponse(
            {
                "status": "failed",
                "message": "Content cannot be empty.",
            },
            status=400,
        )
    reply = Reply(content=content, user=request.user, post=post)
    try:
        reply.save()
        return JsonResponse(
            {
                "status": "success",
                "message": "reply created succesfully",
                "data": {
                    "id": reply.id,
                    "content": reply.content,
                    "created_at": reply.created_at,
                    "updated_at": reply.updated_at,
                    "user": reply.user.username,
                },
            },
            status=201,
        )
    except Exception as e:
        return JsonResponse(
            {
                "status": "failed",
                "message": str(e),
            },
            status=500,
        )


@csrf_exempt
@require_http_methods(["POST"])
@login_required(login_url="authentication:login")
def update_forum_post_reply(request, product_id, post_id, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    content = request.POST.get("content")
    if not content or content.strip() == "":
        return JsonResponse(
            {
                "status": "failed",
                "message": "Content cannot be empty.",
            },
            status=400,
        )
    reply.content = content
    try:
        reply.save()
        return JsonResponse(
            {
                "status": "success",
                "message": "reply updated succesfully",
                "data": {
                    "id": reply.id,
                    "content": reply.content,
                    "created_at": reply.created_at,
                    "updated_at": reply.updated_at,
                    "user": reply.user.username,
                },
            },
            status=201,
        )
    except Exception as e:
        return JsonResponse(
            {
                "status": "failed",
                "message": str(e),
            },
            status=500,
        )


@csrf_exempt
@require_http_methods(["DELETE"])
@login_required(login_url="authentication:login")
def delete_forum_post_reply(request, product_id, post_id, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    try:
        reply.delete()
        return JsonResponse(
            {
                "status": "success",
                "message": "reply deleted succesfully",
                "data": {
                    "id": reply.id,
                },
            },
            status=201,
        )
    except Exception as e:
        return JsonResponse(
            {
                "status": "failed",
                "message": str(e),
            },
            status=500,
        )
