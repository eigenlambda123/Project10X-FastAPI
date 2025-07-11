from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from typing import List
from app.db import async_session
from app.models import BlogPost, Tag, Comment
from app.schemas import BlogPostCreate, BlogPostRead, BlogPostReadNoComments

router = APIRouter(prefix="/posts", tags=["Posts"])


async def get_session() -> AsyncSession:
    """
    Get an async session for database operations
    """
    async with async_session() as session:
        yield session



@router.post("/", response_model=BlogPostRead)
async def create_post(post: BlogPostCreate, session: AsyncSession = Depends(get_session)):
    """ 
    POST endpoint to create a new blog post
    Args:
        post (BlogPostCreate): The blog post data to create
        session (AsyncSession): The database session
    """
    db_post = BlogPost(title=post.title, content=post.content)

    # if there are tags, attach them via the relationship
    if post.tag_ids:
        tags = await session.exec(select(Tag).where(Tag.id.in_(post.tag_ids)))
        db_post.tags = tags.all()
    
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post, attribute_names=["tags"])
    return db_post



@router.get("/", response_model=List[BlogPostReadNoComments])
async def read_posts( 
    tag: str | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session)
):
    """
    GET endpoint to read all blog posts
    Args:
        tag (str | None): Optional tag to filter posts by
        limit (int): Maximum number of posts to return
        offset (int): Offset for pagination
        session (AsyncSession): The database session
    """

    # base query
    base_stmt = select(BlogPost).options(
        selectinload(BlogPost.tags)
    )

    # If a tag is provided, filter posts by that tag
    # If no tag is provided, it will skip this filter
    if tag:
        base_stmt = base_stmt.join(BlogPost.tags).where(Tag.name == tag)
    
    # Count total posts for pagination using base_stmt
    count_result = await session.exec(base_stmt)
    total = len(count_result.all())

    # Apply pagination to the base statement using offset and limit
    paginated_stmt = base_stmt.offset(offset).limit(limit)
    result = await session.exec(paginated_stmt)
    posts = result.all()

    items = [BlogPostReadNoComments.model_validate(post).model_dump() for post in posts]

    # Return paginated response
    # use jsonable_encoder for serializing the datetime fields
    return JSONResponse(
    content=jsonable_encoder({
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items
    })
)






@router.get("/{post_id}", response_model=BlogPostRead)
async def read_post(post_id: int, session: AsyncSession = Depends(get_session)):
    """
    GET endpoint to read a single blog post by ID
    Args:
        post_id (int): The ID of the blog post to read
        session (AsyncSession): The database session
    """
    # Use selectinload to eagerly load tags for the specific blog post
    result = await session.exec(
        select(BlogPost).options(selectinload(BlogPost.tags), selectinload(BlogPost.comments)).where(BlogPost.id == post_id)
    )

    # get the single result or None if not found
    # Using one_or_none to avoid exceptions if no post is found
    post = result.one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return BlogPostRead.model_validate(post)



@router.put("/{post_id}", response_model=BlogPostRead)
async def update_post(post_id: int, data: BlogPostCreate, session: AsyncSession = Depends(get_session)):
    """
    PUT endpoint to update an existing blog post by ID
    Args:
        post_id (int): The ID of the blog post to update
        data (BlogPostCreate): The updated blog post data
        session (AsyncSession): The database session
    """
 
    # retrieve an existing post via its ID
    result = await session.exec(
        select(BlogPost).options(selectinload(BlogPost.tags)).where(BlogPost.id == post_id)
    )

    # Use scalar_one_or_none to get a single result or None if not found
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Update the post's title and content
    # Pydantic v2+ allows direct assignment to model attributes
    post.title = data.title
    post.content = data.content

    # If there are tags, update them via the relationship
    if data.tag_ids:
        tags = await session.exec(select(Tag).where(Tag.id.in_(data.tag_ids)))
        post.tags = tags.all()
    
    await session.commit()
    await session.refresh(post, attribute_names=["tags"])

    return BlogPostRead.model_validate(post)



@router.delete("/{post_id}")
async def delete_post(post_id: int, session: AsyncSession = Depends(get_session)):
    """
    DELETE endpoint to delete a blog post by ID
    Args:
        post_id (int): The ID of the blog post to delete
        session (AsyncSession): The database session
    """

    post = await session.get(BlogPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await session.delete(post)
    await session.commit()
    return {"detail": "Post deleted"}