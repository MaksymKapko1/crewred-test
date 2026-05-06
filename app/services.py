import httpx
from fastapi import HTTPException, status

from app.core.config import settings


async def validate_artwork(external_id: int):
    url = f"{settings.ARTIC_BASE_URL}/artworks/{external_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Artwork ID {external_id} not found in Chicago Art API"
            )
        return response.json()["data"]