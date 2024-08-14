import uuid
from typing import Literal, TypeAlias, List

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.schema import Product
from src.services import ProductService, UserService, OrderService
from src.api.schema.order import CreateOrderDTO
from src.api.schema.product import CreateProduct
from src.main.config import settings
from src.bot.app.main.config import dev_config
from src.bot.app.bot.keyboards import inline
from src.utils import json_text_getter


_SortLiteral: TypeAlias = Literal["purchase_count", "price_lower", "price_higher"] 

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    route_class=DishkaRoute
)


@router.get('/', response_model=List[Product])
async def get_products(
    product_service: FromDishka[ProductService], sort: _SortLiteral,
) -> List[Product]:
    products = await product_service.get_products()

    if products:
        match sort:
            case 'purchase_count':
                products.sort(key=lambda product: product.purchase_count, reverse=True)
            case 'price_higher':
                products.sort(key=lambda product: product.price)
            case 'price_lower':
                products.sort(key=lambda product: product.price, reverse=True)
            case _:
                return JSONResponse(
                    status_code=400,
                    content="`sort` param doesn't match any available options. Available options: 'purchase_count', 'price_higher', 'price_lower'"
                )
    return products


@router.get('/{product_id}', response_model=Product)
async def get_products(
    product_id: int,
    product_service: FromDishka[ProductService],
) -> Product:
    product = await product_service.get_one_product(id=product_id)
    if not product:
        return JSONResponse(
            status_code=404,
            content='Product not found.',
        )
    
    return product


@router.post('/{product_id}/purchase')
async def purchase_product(
    order_data: CreateOrderDTO,
    product_service: FromDishka[ProductService],
    user_service: FromDishka[UserService],
    order_service: FromDishka[OrderService],
) -> JSONResponse:
    user = await user_service.get_one_user(user_id=order_data.user_id)
    product = await product_service.get_one_product(id=order_data.product_id)

    if not product:
        return JSONResponse(status_code=404, content='Product not found.')
    elif not user:
        return JSONResponse(status_code=404, content='User not found.')
    elif user.balance < product.price:
        return JSONResponse(
            status_code=409,
            content=dict(
                description='Insufficient funds on user balance',
                user_balance=float(user.balance),
                top_up_amount=float(product.price - user.balance),
            )
        )
    
    order_id = uuid.uuid4()
    await order_service.add_order(
        id=order_id,
        user_id=order_data.user_id,
        product_id=order_data.product_id,
        name=product.name,
        price=product.price,
        additional_data=order_data.additional_data.model_dump_json(),
    )
    await user_service.update_user(user_id=order_data.user_id, balance=user.balance - product.price)

    try:
        bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        admins = dev_config.admin.admins

        for user_id in admins:
            await bot.send_message(
                chat_id=user_id,
                text=json_text_getter.get_order_info_text(
                    order_id=order_id,
                    order_data=order_data,
                    product=product,
                ),
                reply_markup=inline.order_confirmation_kb_markup(user_id=order_data.user_id)
            )
            return JSONResponse(status_code=200, content=dict(message="success"))
    except Exception as ex:
        print(ex)
    finally:
        await bot.session.close()


@router.post("/create")
async def create_product(
    data: CreateProduct,
    product_service: FromDishka[ProductService],
) -> JSONResponse:
    await product_service.create_product(
        id=data.id,
        name=data.name,
        description=data.description,
        price=data.price,
        instruction=data.instruction,
        purchase_count=data.purchase_count,
    )

    return JSONResponse(status_code=200, content=dict(message='success'))
