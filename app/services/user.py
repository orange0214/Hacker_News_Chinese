"""
User service for business logic
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.core.exceptions import ConflictException, NotFoundException
from app.models.user import User
from app.repositories.user import user_repository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """
    Service for user business logic
    """
    def __init__(self):
        self.repository = user_repository
    
    async def get_user(self, db: AsyncSession, user_id: int) -> User:
        """Get user by ID"""
        user = await self.repository.get(db, user_id)
        if not user:
            raise NotFoundException(f"User with id {user_id} not found")
        return user
    
    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        return await self.repository.get_by_email(db, email=email)
    
    async def get_user_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        """Get user by username"""
        return await self.repository.get_by_username(db, username=username)
    
    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        """Create a new user"""
        # Check if user already exists
        existing_user = await self.get_user_by_email(db, user_in.email)
        if existing_user:
            raise ConflictException("Email already registered")
        
        existing_user = await self.get_user_by_username(db, user_in.username)
        if existing_user:
            raise ConflictException("Username already taken")
        
        # Hash password
        user_data = user_in.model_dump()
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
        
        # Create user
        user = await self.repository.create(db, obj_in=UserCreate(**user_data))
        return user
    
    async def update_user(
        self,
        db: AsyncSession,
        user_id: int,
        user_in: UserUpdate
    ) -> User:
        """Update user"""
        user = await self.get_user(db, user_id)
        
        # Check email uniqueness if changed
        if user_in.email and user_in.email != user.email:
            existing_user = await self.get_user_by_email(db, user_in.email)
            if existing_user:
                raise ConflictException("Email already registered")
        
        # Check username uniqueness if changed
        if user_in.username and user_in.username != user.username:
            existing_user = await self.get_user_by_username(db, user_in.username)
            if existing_user:
                raise ConflictException("Username already taken")
        
        # Hash password if provided
        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        user = await self.repository.update(db, db_obj=user, obj_in=update_data)
        return user
    
    async def delete_user(self, db: AsyncSession, user_id: int) -> User:
        """Delete user"""
        user = await self.get_user(db, user_id)
        await self.repository.delete(db, id=user_id)
        return user
    
    async def authenticate(
        self,
        db: AsyncSession,
        email: str,
        password: str
    ) -> Optional[User]:
        """Authenticate user"""
        user = await self.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


# Create a singleton instance
user_service = UserService()

