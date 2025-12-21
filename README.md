# 🏥 Doctor Appointment Booking System

A **full-stack, production-ready doctor appointment booking system** that enables patients to book appointments based on doctor availability and allows doctors to manage and cancel appointments.  
The system includes **secure authentication**, **role-based access control**, **transaction-safe booking**, and **automated email notifications** using a custom domain.

This project is built and deployed end-to-end with real-world architecture and cloud services.

---

## 🌐 Live Demo

- **Frontend:** https://www.docappointments.in  
- **Backend API:** https://api.docappointments.in  

---

## 🛠 Tech Stack

### Frontend
- React (Vite)
- Bootstrap
- Axios
- React Router

### Backend
- Python (Flask)
- Flask-JWT-Extended (Authentication)
- Flask-SQLAlchemy (ORM)
- Flask-Migrate (Database migrations)
- Flask-CORS (CORS handling)

### Database
- PostgreSQL (Neon – serverless cloud database)

### Infrastructure & Services
- Frontend Hosting: **Vercel**
- Backend Hosting: **Render**
- Database: **Neon**
- Email Service: **Resend** (custom domain verified)
- Domain & DNS: **GoDaddy**

---

## ✨ Features

### 🔐 Authentication & Security
- JWT-based authentication
- Role-based access control (Patient / Doctor)
- Protected frontend routes
- Secure backend authorization and ownership checks
- CORS configured for production domains
- HTTPS enabled across frontend, backend, and API

---

### 👩‍⚕️ Patient Features
- View doctors with pagination
- View real-time doctor availability
- Book appointments safely (prevents double booking)
- Receive email confirmation on successful booking
- View all booked and cancelled appointments
- Cancel appointments from the dashboard
- Receive email notification on cancellation

---

### 👨‍⚕️ Doctor Features
- View all appointments assigned to the doctor
- Cancel appointments when unavailable
- Automatic slot reopening on cancellation
- Patients are notified via email on cancellation
-  Update profile (designation & specialization)
-  Delete account (for non-practicing doctors)
-  invitaion code based register for doctors 

---

### ⚙️ System-Level Features
- Appointments are **never deleted** (status-based lifecycle: `booked`, `cancelled`)
- Transaction-safe booking to handle race conditions
- Email notifications implemented as **side-effects** (do not block core logic)
- Cloud database with persistent storage
- Custom domain setup for frontend, backend, and email


