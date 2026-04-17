
# LLM-P

Серверное приложение на FastAPI, предоставляющее защищённый API для взаимодействия с большой языковой моделью (LLM) через сервис OpenRouter.

## Требования

- Python 3.10+
- Установленный менеджер пакетов [uv](https://docs.astral.sh/uv/)

## Установка и запуск

1. Склонируйте репозиторий.
2. Скопируйте `.env.example` в Ваш новый файл `.env` и заполните необходимые переменные.
3. Установите зависимости и запустите приложение, следуя следующим инструкциям:

uv sync
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000Откройте http://localhost:8000/docs для доступа к Swagger-документации.

4. Использование:
Зарегистрируйтесь через POST /auth/register.
Войдите через POST /auth/login (форма OAuth2), получите JWT токен.
Нажмите кнопку Authorize в Swagger, вставьте токен.
Используйте эндпоинты /chat для общения с LLM.

## Демонстрация работы:
Регистрация:
<img width="2852" height="2154" alt="Регистрация" src="https://github.com/user-attachments/assets/b032c30b-f76d-4bf6-9ddc-a313d38e7cd2" />
Вход через POST /auth/login :
<img width="2828" height="2228" alt="Вход" src="https://github.com/user-attachments/assets/eeb8c615-0bd0-454e-8f49-90b34b92d776" />
Прохождение авторизации:
<img width="1326" height="964" alt="Прохождение авторизации" src="https://github.com/user-attachments/assets/d4f456fa-8549-44ed-b34e-b3e2a3431044" />
Получение профиля текущего пользователя:
<img width="2854" height="2222" alt="Получение профиля текущего пользователя" src="https://github.com/user-attachments/assets/d978e241-272c-4026-81ef-620d8e60dd80" />
Общение с LLM:
<img width="3484" height="2460" alt="Общение с моделью запрос" src="https://github.com/user-attachments/assets/3a1469b6-6547-4ebc-bf66-665bd610b662" />
<img width="3490" height="2448" alt="Общение с моделью ответ" src="https://github.com/user-attachments/assets/858478d9-a949-4759-9b28-a1a011fa50f3" />
Получение истории чатов:
<img width="2856" height="2264" alt="Получение истории чатов" src="https://github.com/user-attachments/assets/45bd75a0-9934-4660-82f1-84806ae88e71" />
Удаление истории чатов:
<img width="2592" height="1626" alt="Удаление истории чатов" src="https://github.com/user-attachments/assets/88dd23bd-c7d8-474e-8e22-34fbbb1c6e2d" />
Подтверждение удаленной истории:
<img width="2612" height="1518" alt="Подтверждение удаленной истории" src="https://github.com/user-attachments/assets/ee6949aa-c11b-477f-8b32-0711eae016d1" />


