
# auth routes
from flask import Blueprint, request, current_app
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models import User, Doctor
from app.utils.security import hash_password, verify_password
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# register endpoint
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")
    invitation_code = data.get("invitation_code")

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

    if User.query.filter_by(email=email).first():
        return {"error": "Email already exists"}, 409

    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        role=role,
    )

    db.session.add(user)
    db.session.commit()

    # If registering as doctor, also create doctor profile
    if role == "doctor":
        doctor = Doctor(
            user_id=user.id,
            specialization="General Practitioner"  # Default specialization
        )
        db.session.add(doctor)
        db.session.commit()

    return {"message": "User registered successfully"}, 201

# login endpoint
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"error": "Email and password required"}, 400

    user = User.query.filter_by(email=email).first()

    if not user or not verify_password(user.password_hash, password):
        return {"error": "Invalid credentials"}, 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    return {"access_token": token}, 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {"error": "User not found"}, 404
        
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
    }

