import pytest

from LR3.repositories.user_repository import UserRepository


class TestUserRepository:
    @pytest.mark.asyncio
    async def test_create_user(self, user_repository: UserRepository):
        user = await user_repository.create(
            email="ivan.petrov@gmail.com",
            username="ivan_petrov",
            first_name="Ivan",
            last_name="Petrov",
        )

        assert user.id is not None
        assert user.email == "ivan.petrov@gmail.com"
        assert user.username == "ivan_petrov"
        assert user.first_name == "Ivan"
        assert user.last_name == "Petrov"

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, user_repository: UserRepository):
        created = await user_repository.create(
            email="nina.kuznetsova@gmail.com",
            username="nina_kuz",
            first_name="Nina",
            last_name="Kuznetsova",
        )

        found = await user_repository.get_by_email("nina.kuznetsova@gmail.com")

        assert found is not None
        assert found.id == created.id
        assert found.email == created.email

    @pytest.mark.asyncio
    async def test_update_user(self, user_repository: UserRepository):
        user = await user_repository.create(
            email="stepan.update@gmail.com",
            username="stepan_upd",
            first_name="Stepan",
            last_name="Kolesov",
        )

        updated = await user_repository.update(user.id, first_name="Stephen")

        assert updated.username == "stepan_upd"
        assert updated.first_name == "Stephen"
        assert updated.last_name == "Kolesov"

    @pytest.mark.asyncio
    async def test_delete_user(self, user_repository: UserRepository):
        user = await user_repository.create(
            email="delete.me@gmail.com",
            username="delete_me",
            first_name="Delete",
            last_name="Me",
        )

        deleted = await user_repository.delete(user.id)
        missing = await user_repository.get_by_id(user.id)

        assert deleted is True
        assert missing is None

    @pytest.mark.asyncio
    async def test_list_users(self, user_repository: UserRepository):
        await user_repository.create(
            email="alice.list@gmail.com",
            username="list_user1",
            first_name="Alice",
            last_name="List",
        )
        await user_repository.create(
            email="bob.list@gmail.com",
            username="list_user2",
            first_name="Bob",
            last_name="List",
        )

        users = await user_repository.get_all()

        assert len(users) >= 2
