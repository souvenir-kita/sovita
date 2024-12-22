import json

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
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
        request,
        "forum_post.html",
        {"user": request.user, "post": post, "replies": replies},
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


def get_posts_flutter(request, product_id):
    posts = (
        Post.objects.filter(product_id=product_id)
        .select_related("user")
        .prefetch_related(
            Prefetch(
                'reply_set',
                queryset=Reply.objects.order_by('-created_at')
            )
        )
        .order_by("-created_at")
    )

    posts_data = []
    for post in posts:
        post_data = {
            "id": str(post.id),
            "user": post.user.username,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "replies": [
                {
                    "id": str(reply.id),
                    "user": reply.user.username,
                    "content": reply.content,
                    "created_at": reply.created_at,
                    "updated_at": reply.updated_at,
                }
                for reply in post.reply_set.all()
            ],
        }
        posts_data.append(post_data)

    return JsonResponse(
        {"status": 200, "message": "success", "data": {"posts": posts_data}}
    )


def get_post_flutter(request, product_id, post_id):
    post = (
        Post.objects.select_related("user")
        .prefetch_related(
            Prefetch(
                'reply_set',
                queryset=Reply.objects.order_by('-created_at')
            )
        )
        .order_by("-created_at")
        .get(pk=post_id)
    )

    post_data = {
        "id": str(post.id),
        "user": post.user.username,
        "title": post.title,
        "content": post.content,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "replies": [
            {
                "id": str(reply.id),
                "user": reply.user.username,
                "content": reply.content,
                "created_at": reply.created_at,
                "updated_at": reply.updated_at,
            }
            for reply in post.reply_set.all()
        ],
    }

    return JsonResponse(
        {"status": 200, "message": "success", "data": {"post": post_data}}
    )


@csrf_exempt
def create_post_flutter(request, product_id):
    if request.method == "POST":
        data = json.loads(request.body)

        product = Product.objects.get(pk=product_id)
        new_post = Post.objects.create(
            user=request.user,
            product=product,
            title=data["title"],
            content=data["content"],
        )

        try:
            new_post.save()
            return JsonResponse(
                {"status": "success", "message": "post saved", "data": {}},
                status=200
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "failed",
                    "message": str(e),
                    "data": {},
                },
                status=500,
            )


@csrf_exempt
def update_post_flutter(request, product_id, post_id):
    if request.method == "POST":
        data = json.loads(request.body)

        post = Post.objects.get(pk=post_id)
        post.title = data["title"]
        post.content = data["content"]

        try:
            post.save()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "post updated succesfully",
                    "data": {},
                },
                status=201,
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "failed",
                    "message": str(e),
                    "data": {},
                },
                status=500,
            )


@csrf_exempt
def delete_post_flutter(request, product_id, post_id):
    if request.method == "POST":
        post = Post.objects.get(pk=post_id)
        try:
            post.delete()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "post deleted succesfully",
                    "data": {},
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
def create_reply_flutter(request, product_id, post_id):
    if request.method == "POST":
        data = json.loads(request.body)

        post = Post.objects.get(pk=post_id)
        new_reply = Reply.objects.create(
            user=request.user,
            post=post,
            content=data["content"],
        )

        try:
            new_reply.save()
            return JsonResponse(
                {"status": "success", "message": "reply saved", "data": {}},
                status=200
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "failed",
                    "message": str(e),
                    "data": {},
                },
                status=500,
            )


@csrf_exempt
def update_reply_flutter(request, product_id, post_id, reply_id):
    if request.method == "POST":
        data = json.loads(request.body)

        reply = Reply.objects.get(pk=reply_id)
        reply.content = data["content"]

        try:
            reply.save()
            return JsonResponse(
                {"status": "success", "message": "reply updated", "data": {}},
                status=200
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "failed",
                    "message": str(e),
                    "data": {},
                },
                status=500,
            )


@csrf_exempt
def delete_reply_flutter(request, product_id, post_id, reply_id):
    if request.method == "POST":
        reply = Reply.objects.get(pk=reply_id)
        try:
            reply.delete()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "reply deleted succesfully",
                    "data": {},
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
