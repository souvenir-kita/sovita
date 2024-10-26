from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from adminview.models import Product
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


@csrf_exempt
@require_http_methods(["POST"])
def create_forum_post_reply(request, product_id, post_id):
    post = get_object_or_404(Post, pk=post_id)
    reply = Reply(content=request.POST.get("content"), user=request.user, post=post)
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
def update_forum_post_reply(request, product_id, post_id, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    reply.content = request.POST.get("content")
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
