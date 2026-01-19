"""
Authentication API Documentation
Separate file for Swagger documentation definitions
"""

from fastapi import Body
from ..modules.auth.schemas import Login

# Farmer Login Documentation
FARMER_LOGIN_DOCS = {
    "summary": "Farmer Login",
    "description": """
    Authenticate a farmer user and receive JWT tokens.
    
    **Process:**
    1. Validate credentials against database
    2. Generate access and refresh tokens
    3. Set refresh token in HTTP-only cookies
    4. Return user information
    
    **Security:**
    - Passwords are hashed with bcrypt
    - Access tokens expire in 30 seconds
    - Refresh tokens expire in 3 days
    - Cookies are HTTP-only and secure
    """,
    "responses": {
        200: {
            "description": "Login successful",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Login successful",
                        "data": {
                            "farmer_id": "123e4567-e89b-12d3-a456-426614174000",
                            "username": "john_doe"
                        }
                    }
                }
            }
        },
        401: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Login failed"
                    }
                }
            }
        }
    }
}

farmer_login_example = Body(
    ..., 
    description="Farmer login credentials",
    example={
        "username": "john_doe",
        "password": "SecurePass123!"
    }
)

# Farmer Registration Documentation
FARMER_SIGNUP_DOCS = {
    "summary": "Farmer Registration",
    "description": """
    Register a new farmer account.
    
    **Process:**
    1. Validate input data
    2. Hash password securely
    3. Create user in database
    4. Generate authentication tokens
    5. Set tokens in cookies
    6. Return user information
    
    **Requirements:**
    - Username must be unique
    - Password minimum 8 characters
    - Email format validation
    """,
    "responses": {
        200: {
            "description": "Registration successful",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Farmer created successfully",
                        "data": {
                            "farmer_id": "123e4567-e89b-12d3-a456-426614174000",
                            "username": "john_doe"
                        }
                    }
                }
            }
        },
        400: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Username already exists"
                    }
                }
            }
        }
    }
}

farmer_signup_example = Body(
    ..., 
    description="Farmer registration data",
    example={
        "username": "john_doe",
        "password": "SecurePass123!"
    }
)

# Admin Login Documentation
ADMIN_LOGIN_DOCS = {
    "summary": "Admin Login",
    "description": """
    Authenticate an admin user and receive JWT tokens.
    
    **Process:**
    1. Validate admin credentials
    2. Generate access and refresh tokens
    3. Set refresh token in HTTP-only cookies
    4. Return admin information
    
    **Security:**
    - Admin credentials are stored separately
    - Enhanced security for admin access
    - Same token management as farmers
    """,
    "responses": {
        200: {
            "description": "Admin login successful",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Login successful",
                        "data": {
                            "admin_id": "123e4567-e89b-12d3-a456-426614174000",
                            "username": "admin_user"
                        }
                    }
                }
            }
        },
        401: {
            "description": "Invalid admin credentials",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Login failed"
                    }
                }
            }
        }
    }
}

admin_login_example = Body(
    ..., 
    description="Admin login credentials",
    example={
        "username": "admin_user",
        "password": "AdminSecurePass123!"
    }
)

