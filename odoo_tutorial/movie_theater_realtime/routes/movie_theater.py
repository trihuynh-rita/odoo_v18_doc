"""
name: movie_theater.py
description: API routes for managing movies in the theater system using FastAPI.
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from models.movie_theater import Movie
from infra.mongo_client import mongo_client

router = APIRouter(prefix="/movies", tags=["Movies"])

# Database reference
db = mongo_client.get_database("cinema_db")
collection = db.get_collection("movies")

@router.get("/", response_model=List[Movie])
async def get_movies():
    """
    Retrieve all movies from the collection.
    
    Returns:
        List[Movie]: A list of all movies in the database.
    """
    try:
        # Retrieve all documents
        movies_cursor = collection.find({})
        movies_list = list(movies_cursor)
        return movies_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching movies: {str(e)}"
        )

@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
async def create_movie(movie: Movie):
    """
    Insert a new movie into the collection.
    
    Args:
        movie (Movie): The movie data to insert.
        
    Returns:
        Movie: The inserted movie record with its unique ID.
    """
    try:
        # Convert Pydantic model to dictionary for MongoDB
        # We exclude unset values to avoid overwriting defaults we want MongoDB to handle
        movie_dict = movie.model_dump(by_alias=True, exclude={"id"})
        
        # Insert into collection
        result = collection.insert_one(movie_dict)
        
        # Attach the newly generated ObjectId string to the response object
        movie.id = str(result.inserted_id)
        
        return movie
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding movie: {str(e)}"
        )
