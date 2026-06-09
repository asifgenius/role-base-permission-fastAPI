import unittest

from fastapi.testclient import TestClient

from app.database.base import reset_state
from app.main import app
from app.repositories.comment_repository import CommentRepository
from app.repositories.post_repository import PostRepository


class PostsApiTests(unittest.TestCase):
    def setUp(self) -> None:
        reset_state()
        PostRepository.create_post(author_id=4, title="Second post", body="Hello again")
        self.client = TestClient(app)
        self.credentials_by_user = {
            3: {"email": "usera@example.com", "password": "usera123"},
            4: {"email": "userb@example.com", "password": "userb123"},
            5: {"email": "userc@example.com", "password": "userc123"},
            6: {"email": "guest@example.com", "password": "guest123"},
        }
        self.headers_by_user = {
            user_id: {"Authorization": f"Bearer {self._issue_token(user_id)}"}
            for user_id in self.credentials_by_user
        }

    def _issue_token(self, user_id: int) -> str:
        response = self.client.post("/api/v1/auth/login", json=self.credentials_by_user[user_id])
        self.assertEqual(response.status_code, 200)
        return response.json()["access_token"]

    def test_regular_user_can_read_all_posts(self) -> None:
        response = self.client.get("/api/v1/posts", headers=self.headers_by_user[5])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_guest_can_read_all_posts(self) -> None:
        response = self.client.get("/api/v1/posts", headers=self.headers_by_user[6])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_comment_list_is_filtered_by_requesting_user(self) -> None:
        CommentRepository.create_comment(post_id=1, author_id=4, body="Nice post")
        own_comment = CommentRepository.create_comment(post_id=1, author_id=3, body="My comment")

        response = self.client.get("/api/v1/posts/1/comments", headers=self.headers_by_user[3])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    "id": own_comment.id,
                    "post_id": 1,
                    "author_id": 3,
                    "body": "My comment",
                }
            ],
        )

    def test_unrelated_regular_user_gets_forbidden_even_if_comment_id_does_not_exist(self) -> None:
        response = self.client.delete("/api/v1/posts/1/comments/3", headers=self.headers_by_user[5])

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"detail": "Forbidden"})

    def test_post_owner_gets_not_found_for_missing_comment(self) -> None:
        response = self.client.delete("/api/v1/posts/1/comments/3", headers=self.headers_by_user[3])

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Comment not found"})

    def test_comment_owner_can_delete_their_own_comment_on_another_users_post(self) -> None:
        create_response = self.client.post(
            "/api/v1/posts/1/comments",
            json={"body": "Nice post"},
            headers=self.headers_by_user[4],
        )

        self.assertEqual(create_response.status_code, 201)
        comment_id = create_response.json()["id"]

        delete_response = self.client.delete(
            f"/api/v1/posts/1/comments/{comment_id}",
            headers=self.headers_by_user[4],
        )

        self.assertEqual(delete_response.status_code, 204)
        self.assertIsNone(CommentRepository.find_comment(comment_id))

    def test_missing_authorization_header_is_rejected(self) -> None:
        response = self.client.get("/api/v1/posts")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Missing Authorization header"})

    def test_login_rejects_invalid_password(self) -> None:
        response = self.client.post(
            "/api/v1/auth/login",
            json={"email": "usera@example.com", "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Invalid credentials"})


if __name__ == "__main__":
    unittest.main()
