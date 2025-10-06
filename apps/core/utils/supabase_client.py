"""
Supabase client singleton for Django.
"""
from supabase import create_client, Client
from django.conf import settings
from functools import lru_cache


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    """
    Get Supabase client singleton.

    Returns:
        Client: Supabase client instance
    """
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_KEY
    )


@lru_cache(maxsize=1)
def get_supabase_admin_client() -> Client:
    """
    Get Supabase admin client with service role key.

    Returns:
        Client: Supabase admin client instance
    """
    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_SERVICE_KEY
    )
