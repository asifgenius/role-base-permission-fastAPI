import unittest

from authorization import Authorization, Comment, Post, Role, User


class AuthorizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.super_admin = User(id=1, role=Role.SUPER_ADMIN)
        self.moderator = User(id=2, role=Role.MODERATOR)
        self.user_a = User(id=3, role=Role.REGULAR_USER)
        self.user_b = User(id=4, role=Role.REGULAR_USER)
        self.user_c = User(id=5, role=Role.REGULAR_USER)
        self.guest = User(id=6, role=Role.GUEST)

        self.post_by_a = Post(id=10, author_id=self.user_a.id, title="t", body="b")
        self.post_by_b = Post(id=11, author_id=self.user_b.id, title="t", body="b")
        self.comment_by_b_on_a = Comment(
            id=20,
            author_id=self.user_b.id,
            post_id=self.post_by_a.id,
            body="hello",
        )

    def test_super_admin_has_full_delete_access_and_user_management(self) -> None:
        self.assertTrue(Authorization.can_manage_users(self.super_admin))
        self.assertTrue(Authorization.can_delete_post(self.super_admin, self.post_by_a))
        self.assertFalse(Authorization.can_create_post(self.super_admin))
        self.assertFalse(Authorization.can_create_comment(self.super_admin, self.post_by_a))
        self.assertFalse(Authorization.can_update_post(self.super_admin, self.post_by_a))
        self.assertTrue(
            Authorization.can_delete_comment(
                self.super_admin,
                self.post_by_a,
                self.comment_by_b_on_a,
            )
        )

    def test_moderator_can_delete_posts_and_comments_but_not_manage_users(self) -> None:
        self.assertFalse(Authorization.can_manage_users(self.moderator))
        self.assertTrue(Authorization.can_delete_post(self.moderator, self.post_by_a))
        self.assertFalse(Authorization.can_create_post(self.moderator))
        self.assertFalse(Authorization.can_create_comment(self.moderator, self.post_by_a))
        self.assertFalse(Authorization.can_update_post(self.moderator, self.post_by_a))
        self.assertTrue(
            Authorization.can_delete_comment(
                self.moderator,
                self.post_by_a,
                self.comment_by_b_on_a,
            )
        )

    def test_regular_user_can_create_posts_and_only_change_their_own_posts(self) -> None:
        self.assertTrue(Authorization.can_create_post(self.user_a))
        self.assertTrue(Authorization.can_update_post(self.user_a, self.post_by_a))
        self.assertTrue(Authorization.can_delete_post(self.user_a, self.post_by_a))
        self.assertFalse(Authorization.can_update_post(self.user_a, self.post_by_b))
        self.assertFalse(Authorization.can_delete_post(self.user_a, self.post_by_b))

    def test_guest_can_only_read(self) -> None:
        self.assertTrue(Authorization.can_read(self.guest))
        self.assertFalse(Authorization.can_manage_users(self.guest))
        self.assertFalse(Authorization.can_create_post(self.guest))
        self.assertFalse(Authorization.can_create_comment(self.guest, self.post_by_a))
        self.assertFalse(Authorization.can_delete_post(self.guest, self.post_by_a))
        self.assertFalse(
            Authorization.can_delete_comment(
                self.guest,
                self.post_by_a,
                self.comment_by_b_on_a,
            )
        )

    def test_user_b_can_comment_on_user_as_post(self) -> None:
        self.assertTrue(Authorization.can_create_comment(self.user_b, self.post_by_a))

    def test_post_owner_can_delete_other_users_comments_on_their_post(self) -> None:
        self.assertTrue(
            Authorization.can_delete_comment(
                self.user_a,
                self.post_by_a,
                self.comment_by_b_on_a,
            )
        )

    def test_comment_owner_can_delete_their_own_comment(self) -> None:
        self.assertTrue(
            Authorization.can_delete_comment(
                self.user_b,
                self.post_by_a,
                self.comment_by_b_on_a,
            )
        )

    def test_other_regular_users_cannot_delete_someone_elses_comment(self) -> None:
        self.assertFalse(
            Authorization.can_delete_comment(
                self.user_c,
                self.post_by_a,
                self.comment_by_b_on_a,
            )
        )

    def test_comment_must_belong_to_the_post_context(self) -> None:
        wrong_post = Post(id=999, author_id=self.user_a.id, title="x", body="y")
        self.assertFalse(
            Authorization.can_delete_comment(
                self.user_a,
                wrong_post,
                self.comment_by_b_on_a,
            )
        )


if __name__ == "__main__":
    unittest.main()
