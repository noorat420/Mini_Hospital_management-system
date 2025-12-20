# Auth Controller - Business logic for authentication
from flask import current_app
from flask_jwt_extended import create_access_token

from src.repositories import UserRepository, DoctorRepository
from src.utils.security import hash_password, verify_password


class AuthController:
    @staticmethod
    def register(name: str, email: str, password: str, role: str, invitation_code: str = None):
        # Validate required fields
        if not all([name, email, password, role]):
            return {"error": "Missing required fields"}, 400

        if role not in ["doctor", "patient"]:
            return {"error": "Invalid role"}, 400

        # Validate doctor invitation code
        if role == "doctor":
            if not invitation_code:
                return {"error": "Invitation code is required for doctor registration"}, 400
            valid_code = current_app.config.get("DOCTOR_INVITATION_CODE", "DOC2024SECRET")
            if invitation_code != valid_code:
                return {"error": "Invalid invitation code"}, 403

        # Check if email exists
        if UserRepository.email_exists(email):
            return {"error": "Email already exists"}, 409

        # Create user
        user = UserRepository.create(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role=role
        )

        # Create doctor profile if registering as doctor
        if role == "doctor":
            DoctorRepository.create(
                user_id=user.id,
                designation="Dr.",
                specialization="General Practitioner"
            )

        return {"message": "User registered successfully"}, 201

    @staticmethod
    def login(email: str, password: str):
        if not email or not password:
            return {"error": "Email and password required"}, 400

        user = UserRepository.get_by_email(email)

        if not user or not verify_password(user.password_hash, password):
            return {"error": "Invalid credentials"}, 401

        token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role}
        )

        return {"access_token": token}, 200

    @staticmethod
    def get_current_user(user_id: int):
        user = UserRepository.get_by_id(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        }, 200

