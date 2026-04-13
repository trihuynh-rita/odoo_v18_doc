"""
name: movie_theater.py
description: Model schema for Movies, including categories, ratings, and scoring.
"""
from typing import List, Optional, Annotated
from pydantic import BaseModel, Field, BeforeValidator
from bson import ObjectId

# Type helper for handling MongoDB ObjectId in Pydantic
PyObjectId = Annotated[str, BeforeValidator(str)]

class Movie(BaseModel):
    """
    Schema representing a Movie record in MongoDB.
    
    Fields:
        id: Unique identifier from MongoDB (ObjectId hex string).
        name: Name of the movie.
        category: Genre choice, one of [('sci_fi', 'Sci-fi'), ('thriller', 'thriller'), ('action', 'Action'), ('comedy', 'Comedy')].
        price: Price of the movie listed as a string (e.g., "$10.00").
        rating: Age rating, one of [('g_rating', 'G'), ('pg_rating', 'PG'), ('pg12_rating', 'PG-13'), ('r_rating', 'R'), ('nc17_rating', 'NC-17')].
        review_ids: List of associated review IDs.
        average_score: Mean calculated score based on reviews.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(..., description="Movie title")
    
    # Enum-like category choices
    category: str = Field(..., description="Category choices: sci_fi, thriller, action, comedy")
    
    price: str = Field(..., description="Price of the movie")
    
    # Enum-like rating choices
    rating: str = Field(..., description="Rating choices: g_rating, pg_rating, pg12_rating, r_rating, nc17_rating")
    
    review_ids: List[PyObjectId] = Field(default_factory=list, description="List of ObjectIds of associated reviews")
    average_score: float = Field(default=0.0, description="Calculated average score from reviews")

    class Config:
        """
        Pydantic model configuration to handle ObjectId and serialization.
        """
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "name": "Interstellar",
                "category": "sci_fi",
                "price": "15.00",
                "rating": "pg12_rating",
                "review_ids": [],
                "average_score": 9.5
            }
        }
