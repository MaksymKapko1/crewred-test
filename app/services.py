import httpx
from fastapi import HTTPException, status

_cache: dict[int, dict] = {}

async def validate_artwork(external_id: int) -> dict:
    if external_id in _cache:
        return _cache[external_id]

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.artic.edu/api/v1/artworks/{external_id}",
            params={"fields": "id,title"}
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Artwork ID {external_id} not found in Chicago Art API"
            )
        data = response.json()["data"]
        _cache[external_id] = data
        return data