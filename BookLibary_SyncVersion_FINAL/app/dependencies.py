from fastapi import Query
from typing import Dict

def pagination(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return")
) -> Dict[str, int]:
    """Reusable pagination dependency"""
    return {"skip": skip, "limit": limit}


def book_filters(
    title: str | None = Query(None, description="Filter by title"),
    author: str | None = Query(None, description="Filter by author"),
    published_year: int | None = Query(None, description="Filter by published year"),
    min_year: int | None = Query(None, ge=1500),
    max_year: int | None = Query(None, le=2026)
) -> dict:
    """Reusable book filtering dependency"""
    return {
        "title": title,
        "author": author,
        "published_year": published_year,
        "min_year": min_year,
        "max_year": max_year
    }