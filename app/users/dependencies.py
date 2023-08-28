from datetime import datetime
from jose import jwt, JWTError
from fastapi import Depends,  Request

from app.config import settings
from app.exceptions import IncorrectTokenFormatException, TokenAbsentException, TokenExpiredException, UserInNotPresentException
from app.users.dao import UsersDAO


# Получение jwt-токена из запроса пользователя
def get_token(request:Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token
    

# Парсинг токена и получение  юзера из БД
async def get_current_user(token: str = Depends(get_token)):
    # Проверяем, что в куках jwt-токен, а не что-то другое
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException
    
    # Проверка времени действия токена
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()): 
        raise TokenExpiredException
    
    # Проверка в данных токена параметра sub, в который записывали id юзера
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserInNotPresentException
    
    # Запрос в БД по id юзера и возврат юзера из БД
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserInNotPresentException
    
    return user