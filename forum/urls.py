from django.urls import path

from forum.views import (
    create_forum_post,
    create_forum_post_reply,
    create_post_flutter,
    delete_forum_post,
    delete_forum_post_reply,
    delete_post_flutter,
    get_forum_post,
    get_forum_posts,
    get_posts_flutter,
    update_forum_post,
    update_forum_post_reply,
    update_post_flutter,
)

app_name = "forum"

urlpatterns = [
    # CRUD POST
    path(
        "<uuid:product_id>",
        get_forum_posts,
        name="forum_posts"
    ),
    path(
        "<uuid:product_id>/<uuid:post_id>",
        get_forum_post,
        name="forum_post"
    ),
    path(
        "<uuid:product_id>/create",
        create_forum_post,
        name="create_forum_post"
    ),
    path(
        "<uuid:product_id>/edit/<uuid:post_id>",
        update_forum_post,
        name="edit_forum_post",
    ),
    path(
        "<uuid:product_id>/delete/<uuid:post_id>",
        delete_forum_post,
        name="delete_forum_post",
    ),
    # CRUD POST REPLY
    path(
        "<uuid:product_id>/<uuid:post_id>/create",
        create_forum_post_reply,
        name="create_forum_post_reply",
    ),
    path(
        "<uuid:product_id>/<uuid:post_id>/edit/<uuid:reply_id>",
        update_forum_post_reply,
        name="edit_forum_post_reply",
    ),
    path(
        "<uuid:product_id>/<uuid:post_id>/delete/<uuid:reply_id>",
        delete_forum_post_reply,
        name="delete_forum_post_reply",
    ),
    # FLUTTER
    path(
        "flutter/<uuid:product_id>",
        get_posts_flutter,
        name="get_posts_flutter"
    ),
    path(
        "flutter/<uuid:product_id>/create",
        create_post_flutter,
        name="create_post_flutter",
    ),
    path(
        "flutter/<uuid:product_id>/<uuid:post_id>/update",
        update_post_flutter,
        name="update_post_flutter",
    ),
    path(
        "flutter/<uuid:product_id>/<uuid:post_id>/delete",
        delete_post_flutter,
        name="delete_post_flutter",
    ),
]
