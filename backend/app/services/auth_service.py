from app.db.supabase import get_supabase
from pydantic import EmailStr

class AuthService:
    def signup(self, email: EmailStr, password: str, metadata: dict | None = None):
        supabase = get_supabase()
        resp = supabase.auth.sign_up(
            {
                "email": email,
                "password": password,
                "options": {"data": metadata or {}}
            }
        )
        if not resp.user:
            raise ValueError("Signup failed: No user returned")
        
        return resp
    
    def login(self, email: EmailStr, password: str):
        supabase = get_supabase()
        try:
            resp = supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            return resp
        except Exception as e:
            raise ValueError(f"Authentication failed: {str(e)}")

    def get_user_by_token(self, token: str):
        supabase = get_supabase()
        try:
            resp = supabase.auth.get_user(token)
            if not resp.user:
                raise ValueError("User not found")
            return resp.user
        except Exception as e:
            raise ValueError(f"Failed to get user by token: {str(e)}")


auth_service = AuthService()