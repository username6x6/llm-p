class AppError(Exception):
    """Базовое исключение приложения."""
    pass


class ConflictError(AppError):
    """Конфликт данных (например, email уже существует)."""
    pass


class UnauthorizedError(AppError):
    """Ошибка аутентификации (неверный пароль или токен)."""
    pass


class ForbiddenError(AppError):
    """Доступ запрещён."""
    pass


class NotFoundError(AppError):
    """Объект не найден."""
    pass


class ExternalServiceError(AppError):
    """Ошибка при обращении к внешнему сервису (OpenRouter)."""
    pass