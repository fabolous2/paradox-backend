from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from dependency_injector.wiring import inject, Provide

from src.services import SupercellAuthService
from src.api.schema.supercell import SupercellAuthDTO
from src.main.ioc import Container

router = APIRouter(
    prefix="/supercell",
    tags=["Supercell Auth"],
)

import requests
from typing import Dict


class SupercellCode:
    def __init__(self, email: str, game: str):
        user_agent: str = f"scid/4543 (Android; {game}-prod)"
        self.email = email
        self.game = game
        self.headers: Dict[str, str] = {
            "User-Agent": user_agent,
            "Authorization": "",  # Здесь можно добавить токен, если он будет получен
        }
        self.login_data: Dict[str, str] = {
            "lang": "ru",
            "email": email,
            "remember": "true",
            "game": game,
            "env": "prod",
        }

    def code(self) -> None:
        try:
            # Выполняем POST запрос
            response = requests.post(
                url="https://id.supercell.com/api/ingame/account/login",
                data=self.login_data,
                headers=self.headers
            )
            # Обработка ответа
            self._process_response(self.game, self.email, response)

        except requests.exceptions.RequestException as e:
            print(f"Произошла ошибка при выполнении запроса: {e}")

    def _process_response(self, game, email, response: requests.Response) -> None:
        print(response.json())
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("ok"):
                print(f"{email} {game} Done")
            else:
                print(f"{email} {game} Error: {response_data.get('error')}")
        else:
            print(f"{email} {game} HTTP error: {response.status_code}")
            print(f"{email} {game} Answer: {response.text}")



@router.post("/login")
# @inject
async def login(
    data: SupercellAuthDTO,
    # supercell_service: SupercellAuthService = Depends(Provide[Container.supercell_service]),
) -> JSONResponse:
    supercell_code = SupercellCode(data.email, data.game)
    supercell_code.code()
    # supercell_service.login(email=data.email, game=data.game)
    
    return JSONResponse(status_code=200, content=dict(message='success'))