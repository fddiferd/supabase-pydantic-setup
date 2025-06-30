import os
from supabase import create_client, Client


def get_client() -> Client:
    url: str | None = os.environ.get("SUPABASE_URL")
    key: str | None = os.environ.get("SUPABASE_KEY")

    if url is None or key is None:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY environment variables must be set")

    return create_client(url, key)

if __name__ == "__main__":
    client: Client = get_client()
    print(client)