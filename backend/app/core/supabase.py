from functools import lru_cache

from supabase import Client, create_client

from app.core.config import settings


@lru_cache
def get_supabase_client() -> Client:
    """
    Crea y reutiliza el cliente de Supabase para el backend.
    """

    if not settings.supabase_url:
        raise RuntimeError("Falta configurar SUPABASE_URL en el archivo .env")

    if not settings.supabase_secret_key:
        raise RuntimeError("Falta configurar SUPABASE_SECRET_KEY en el archivo .env")

    secret_key = settings.supabase_secret_key.get_secret_value()

    return create_client(
        settings.supabase_url,
        secret_key,
    )
