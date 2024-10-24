from django.urls import path

from forum.views import (
    create_forum_post,
    create_forum_post_reply,
    delete_forum_post,
    delete_forum_post_reply,
    get_forum_post,
    get_forum_posts,
    update_forum_post,
    update_forum_post_reply,
)

app_name = "forum"

urlpatterns = [
    # CRUD POST
    path("<uuid:product_id>", get_forum_posts, name="forum_posts"),
    path("<uuid:product_id>/<uuid:post_id>", get_forum_post, name="forum_post"),
    path("<uuid:product_id>/create", create_forum_post, name="create_forum_post"),
    path("<uuid:product_id>/edit/<uuid:post_id>", update_forum_post, name="edit_forum_post"),
    path("<uuid:product_id>/delete/<uuid:post_id>", delete_forum_post, name="delete_forum_post"),
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
]
