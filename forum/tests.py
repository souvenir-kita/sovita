import json
import uuid

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import NoReverseMatch, reverse

from adminview.models import Product
from forum.models import Post, Reply

User = get_user_model()


class ForumViewsTest(TestCase):
    def setUp(self):
        # Create test client
        self.client = Client()

        # Create test user
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        # Create second test user for authorization tests
        self.other_user = User.objects.create_user(username="otheruser", password="testpass123")

        # Create test product with price
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=100000,  # Adding the required price field
        )

        # Create test post
        self.post = Post.objects.create(
            title="Test Post", content="Test Content", user=self.user, product=self.product
        )

        # Create test reply
        self.reply = Reply.objects.create(content="Test Reply", user=self.user, post=self.post)

        # Login the test user
        self.client.login(username="testuser", password="testpass123")

    def test_get_forum_posts_list(self):
        """Test getting forum posts list for a product"""
        # Create additional post for testing
        Post.objects.create(
            title="Second Post", content="Second Content", user=self.user, product=self.product
        )

        response = self.client.get(
            reverse("forum:forum_posts", kwargs={"product_id": self.product.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forum_posts.html")
        self.assertEqual(len(response.context["posts"]), 2)

    def test_get_single_forum_post(self):
        """Test getting a single forum post with its replies"""
        # Create additional reply
        Reply.objects.create(content="Second Reply", user=self.user, post=self.post)

        response = self.client.get(
            reverse(
                "forum:forum_post", kwargs={"product_id": self.product.id, "post_id": self.post.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forum_post.html")
        self.assertEqual(len(response.context["replies"]), 2)

    def test_create_forum_post_success(self):
        """Test successful forum post creation"""
        post_data = {"title": "New Test Post", "content": "New Test Content"}
        response = self.client.post(
            reverse("forum:create_forum_post", kwargs={"product_id": self.product.id}), post_data
        )
        self.assertEqual(response.status_code, 302)  # Redirect on success
        new_post = Post.objects.get(title="New Test Post")
        self.assertEqual(new_post.user, self.user)
        self.assertEqual(new_post.product, self.product)

    def test_create_reply_with_invalid_post_id(self):
        """Test creating reply for non-existent post"""
        invalid_post_id = uuid.uuid4()
        reply_data = {"content": "Test Reply Content"}
        response = self.client.post(
            reverse(
                "forum:create_forum_post_reply",
                kwargs={"product_id": self.product.id, "post_id": invalid_post_id},
            ),
            reply_data,
        )
        self.assertEqual(response.status_code, 404)

    def test_create_reply_with_empty_content(self):
        """Test creating reply with empty content"""
        reply_data = {"content": ""}
        response = self.client.post(
            reverse(
                "forum:create_forum_post_reply",
                kwargs={"product_id": self.product.id, "post_id": self.post.id},
            ),
            reply_data,
        )
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data["message"], "Content cannot be empty.")

    def test_delete_post_cascade(self):
        """Test that deleting a post also deletes associated replies"""
        reply_id = self.reply.id
        response = self.client.post(
            reverse(
                "forum:delete_forum_post",
                kwargs={"product_id": self.product.id, "post_id": self.post.id},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Reply.objects.filter(id=reply_id).exists())

    def test_create_post_without_product(self):
        """Test creating post with invalid product ID"""
        invalid_product_id = uuid.uuid4()
        post_data = {"title": "Test Post", "content": "Test Content"}
        response = self.client.post(
            reverse("forum:create_forum_post", kwargs={"product_id": invalid_product_id}),
            post_data,
        )
        self.assertEqual(response.status_code, 404)
