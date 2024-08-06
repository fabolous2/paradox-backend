import uuid
from typing import Literal, TypeAlias, List

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute

from src.schema import Product
from src.schema.order import OrderStatus
from src.services import ProductService, UserService, OrderService
from src.api.schema.order import CreateOrderDTO

_SortLiteral: TypeAlias = Literal["purchase_count", "price_lower", "price_higher"] 

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    route_class=DishkaRoute
)


@router.get('/', response_model=List[Product])
async def get_products(
    product_service: FromDishka[ProductService], sort: _SortLiteral,
) -> JSONResponse:
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
    return JSONResponse(
        status_code=200, content=dict(products=products)
    )


@router.get('/{product_id}', response_model=Product)
async def get_products(
    product_id: int,
    product_service: FromDishka[ProductService],
) -> JSONResponse:
    product = await product_service.get_one_product(id=product_id)
    if not product:
        return JSONResponse(
            status_code=404,
            content='Product not found.',
        )
    
    return JSONResponse(
        status_code=200,
        content=dict(product=product)
    )


@router.get('/{product_id}/purchase')
async def purchase_product(
    order_data: CreateOrderDTO,
    product_service: FromDishka[ProductService],
    user_service: FromDishka[UserService],
    order_service: FromDishka[OrderService],
) -> JSONResponse:
    user = await user_service.get_one_user(user_id=order_data.user_id)
    product = await product_service.get_one_product(id=order_data.product_id)

    if not product:
        return JSONResponse(
            status_code=404,
            content='Product not found.',
        )
    elif not user:
        return JSONResponse(
            status_code=404,
            content='Product not found.',
        )
    elif user.balance < product.price:
        return JSONResponse(
            status_code=409,
            content=dict(
                description='Insufficient funds on user balance',
                user_balance=user.balance,
                top_up_amount=product.price - user.balance,
            )
        )
    
    await order_service.add_order(
        id=uuid.uuid4(),
        user_id=order_data.user_id,
        product_id=order_data.product_id,
        name=product.name,
        price=product.price,
        additional_data=order_data.additional_data.model_dump_json(),
    )

    return JSONResponse(status_code=200, content=dict(message="success"))
    # return JSONResponse(
    #     status_code=200,
    #     content=dict(product=product)
    # )


# @router.post('/{product_id}/purchase.order')
# async def supercell_product_order(
#     product_id: int,
#     user_id: int,
    # order_data: SupercellOrderDTO,
#     product_service: FromDishka[ProductService],
    # order_service: FromDishka[OrderService],
#     user_service: FromDishka[UserService],
# ) -> JSONResponse:
#     user = await user_service.get_one_user(user_id=user_id)
#     product = await product_service.get_one_product(id=product_id)

#     if not product:
#         return JSONResponse(
#             status_code=404,
#             content='Product not found.',
#         )
#     elif not user:
#         return JSONResponse(
#             status_code=404,
#             content='User not found.',
#         )
    
#     await order_service.add_order(
#         id=uuid.uuid4(),
#         user_id=user_id,
#         product_id=product_id,
#         name=product.name,
#         price=product.price,
#         additional_data=order_data.model_dump_json(),
#     )

#     return JSONResponse(status_code=200, content=dict(message="success"))
