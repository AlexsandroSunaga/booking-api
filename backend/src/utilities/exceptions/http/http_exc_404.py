from fastapi import HTTPException, status


def raise_not_found(detail: str = "Resource not found") -> None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
