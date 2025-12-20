# Application Entry Point
from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config.from_object("config.Config")

# CORS
CORS(
    app,
    origins=["http://localhost:5173", "https://your-frontend.vercel.app"],
    supports_credentials=True
)

# Initialize extensions
from src.extensions import init_extensions
init_extensions(app)

# Import models
from src import models

# Import controllers
from src.controllers import (
    AuthController,
    DoctorController,
    PatientController,
    AppointmentController,
    AvailabilityController
)
from src.utils.decorators import role_required


# ============================================================================
# HEALTH CHECK
# ============================================================================
@app.route("/health", methods=["GET"])
def health_check():
    return {"status": "ok"}


# ============================================================================
# AUTH ROUTES
# ============================================================================
@app.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    return AuthController.register(
        name=data.get("name"),
        email=data.get("email"),
        password=data.get("password"),
        role=data.get("role"),
        invitation_code=data.get("invitation_code")
    )


@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    return AuthController.login(
        email=data.get("email"),
        password=data.get("password")
    )


@app.route("/auth/me", methods=["GET"])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    return AuthController.get_current_user(user_id)


# ============================================================================
# DOCTOR ROUTES
# ============================================================================
@app.route("/doctor/dashboard", methods=["GET"])
@jwt_required()
@role_required("doctor")
def doctor_dashboard():
    return DoctorController.get_dashboard()


@app.route("/doctor/profile", methods=["GET"])
@jwt_required()
@role_required("doctor")
def get_doctor_profile():
    user_id = int(get_jwt_identity())
    return DoctorController.get_profile(user_id)


@app.route("/doctor/profile", methods=["POST"])
@jwt_required()
@role_required("doctor")
def update_doctor_profile():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    return DoctorController.update_profile(
        user_id=user_id,
        designation=data.get("designation"),
        specialization=data.get("specialization")
    )


@app.route("/doctor/account", methods=["DELETE"])
@jwt_required()
@role_required("doctor")
def delete_doctor_account():
    user_id = int(get_jwt_identity())
    return DoctorController.delete_account(user_id)


# ============================================================================
# PATIENT ROUTES
# ============================================================================
@app.route("/patient/dashboard", methods=["GET"])
@jwt_required()
@role_required("patient")
def patient_dashboard():
    return PatientController.get_dashboard()


@app.route("/patient/doctors", methods=["GET"])
@jwt_required()
@role_required("patient")
def list_doctors():
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    return PatientController.list_doctors(page=page, limit=limit)


@app.route("/patient/doctors/<int:doctor_id>/availability", methods=["GET"])
@jwt_required()
@role_required("patient")
def doctor_availability(doctor_id):
    return PatientController.get_doctor_availability(doctor_id)


# ============================================================================
# AVAILABILITY ROUTES
# ============================================================================
@app.route("/doctor/availability", methods=["POST"])
@jwt_required()
@role_required("doctor")
def create_availability():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    return AvailabilityController.create_slot(
        user_id=user_id,
        date_str=data.get("date"),
        start_time_str=data.get("start_time"),
        end_time_str=data.get("end_time")
    )


# ============================================================================
# APPOINTMENT ROUTES
# ============================================================================
@app.route("/appointments", methods=["POST"])
@jwt_required()
@role_required("patient")
def book_appointment():
    patient_id = int(get_jwt_identity())
    data = request.get_json()
    return AppointmentController.book_appointment(
        patient_id=patient_id,
        slot_id=data.get("slot_id")
    )


@app.route("/appointments/my", methods=["GET"])
@jwt_required()
@role_required("patient")
def my_appointments():
    patient_id = int(get_jwt_identity())
    return AppointmentController.get_patient_appointments(patient_id)


@app.route("/appointments/doctor", methods=["GET"])
@jwt_required()
@role_required("doctor")
def doctor_appointments():
    user_id = int(get_jwt_identity())
    return AppointmentController.get_doctor_appointments(user_id)


@app.route("/appointments/<int:appointment_id>/cancel", methods=["POST"])
@jwt_required()
def cancel_appointment(appointment_id):
    user_id = int(get_jwt_identity())
    claims = get_jwt()
    return AppointmentController.cancel_appointment(
        appointment_id=appointment_id,
        user_id=user_id,
        role=claims.get("role")
    )


# ============================================================================
# RUN APP
# ============================================================================
if __name__ == "__main__":
    app.run(debug=True)

