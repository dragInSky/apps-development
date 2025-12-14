from unittest.mock import AsyncMock, Mock

import pytest

from LR3.repositories.order_repository import OrderRepository
from LR3.repositories.product_repository import ProductRepository
from LR3.repositories.user_repository import UserRepository
from LR3.services.order_service import OrderService


class TestOrderService:
    @pytest.mark.asyncio
    async def test_create_order_success(self):
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)

        mock_user_repo.get_by_id.return_value = Mock(id=1, email="mockuser@gmail.com")
        mock_product_repo.get_by_id.return_value = Mock(
            id=1, name="Test Product", price=100.0, stock_quantity=5
        )
        mock_order_repo.create.return_value = Mock(
            id=1, user_id=1, total_amount=200.0, status="pending", items=[]
        )

        order_service = OrderService(
            order_repository=mock_order_repo,
            product_repository=mock_product_repo,
            user_repository=mock_user_repo,
        )

        order_data = {
            "user_id": 1,
            "items": [{"product_id": 1, "quantity": 2}],
        }

        result = await order_service.create_order(order_data)

        assert result is not None
        assert result.total_amount == 200.0
        mock_order_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_order_insufficient_stock(self):
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)

        mock_user_repo.get_by_id.return_value = Mock(id=1)
        mock_product_repo.get_by_id.return_value = Mock(
            id=1, name="Test Product", price=100.0, stock_quantity=1
        )

        order_service = OrderService(
            order_repository=mock_order_repo,
            product_repository=mock_product_repo,
            user_repository=mock_user_repo,
        )

        order_data = {
            "user_id": 1,
            "items": [{"product_id": 1, "quantity": 5}],
        }

        with pytest.raises(ValueError, match="Insufficient stock"):
            await order_service.create_order(order_data)

    @pytest.mark.asyncio
    async def test_create_order_missing_user(self):
        mock_order_repo = AsyncMock(spec=OrderRepository)
        mock_product_repo = AsyncMock(spec=ProductRepository)
        mock_user_repo = AsyncMock(spec=UserRepository)

        mock_user_repo.get_by_id.return_value = None

        order_service = OrderService(
            order_repository=mock_order_repo,
            product_repository=mock_product_repo,
            user_repository=mock_user_repo,
        )

        order_data = {"user_id": 99, "items": [{"product_id": 1, "quantity": 1}]}

        with pytest.raises(ValueError, match="User not found"):
            await order_service.create_order(order_data)
