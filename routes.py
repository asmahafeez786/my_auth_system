from flask import request, jsonify
from flask_jwt_extended import (create_access_token,jwt_required,get_jwt_identity, get_jwt)

from datetime import datetime, timedelta
import secrets

from models import db, User, bcrypt
from services import send_email


def register_routes(app):
    @app.route("/signup", methods=["POST"])
    def signup():
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"message": "All fields are required"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email already exists"}), 409

        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Signup successful"}), 201

    @app.route("/login", methods=["POST"])
    def login():

        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"message": "Invalid email or password"}), 401

        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({"message": "Invalid email or password"}), 401

        token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "token_version": user.token_version
            }
        )

        return jsonify({
            "message": "Login successful",
            "access_token": token
        }), 200

    # PROTECTED ROUTE
    @app.route("/protected", methods=["GET"])
    @jwt_required()
    def protected():

        user = get_current_user()

        if not user:
            return jsonify({"message": "Invalid or expired session"}), 401

        return jsonify({
            "message": "You accessed the protected route",
            "name": user.name,
            "email": user.email
        }), 200

    
    @app.route("/forgot-password", methods=["POST"])
    def forgot_password():

        data = request.get_json()

        email = data.get("email")

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({
                "message": "If the account exists, an OTP can be sent"
            }), 200

        otp = str(secrets.randbelow(900000) + 100000)

        user.otp = bcrypt.generate_password_hash(
            otp
        ).decode("utf-8")

        user.otp_expiry = datetime.utcnow() + timedelta(minutes=5)

        db.session.commit()

        try:
            send_email(email, otp)

        except Exception:
            app.logger.exception("OTP email could not be sent")

            user.otp = None
            user.otp_expiry = None

            db.session.commit()

            return jsonify({
                "message": "Email could not be sent. Try again."
            }), 500

        return jsonify({
            "message": "If the account exists, an OTP can be sent"
        }), 200

    # RESET PASSWORD USING OTP
    @app.route("/reset-password", methods=["POST"])
    def reset_password():

        data = request.get_json()

        email = data.get("email")
        otp = data.get("otp")
        new_password = data.get("new_password")

        if not email or not otp or not new_password:
            return jsonify({"message": "All fields are required"}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not user.otp or not user.otp_expiry:
            return jsonify({"message": "Invalid or expired OTP"}), 400

        if datetime.utcnow() >= user.otp_expiry:
            user.otp = None
            user.otp_expiry = None
            db.session.commit()

            return jsonify({"message": "OTP expired"}), 400

        if not bcrypt.check_password_hash(user.otp, otp):
            return jsonify({"message": "Invalid OTP"}), 400

        user.password = bcrypt.generate_password_hash(
            new_password
        ).decode("utf-8")

        user.token_version += 1

        user.otp = None
        user.otp_expiry = None

        db.session.commit()

        return jsonify({
            "message": "Password reset successful. Please login again."
        }), 200

    # CHANGE PASSWORD
    @app.route("/change-password", methods=["PUT"])
    @jwt_required()
    def change_password():

        user = get_current_user()

        if not user:
            return jsonify({"message": "Invalid or expired session"}), 401

        data = request.get_json()

        old_password = data.get("old_password")
        new_password = data.get("new_password")

        if not old_password or not new_password:
            return jsonify({"message": "Both passwords are required"}), 400

        if not bcrypt.check_password_hash(user.password, old_password):
            return jsonify({"message": "Old password is incorrect"}), 400

        user.password = bcrypt.generate_password_hash(
            new_password
        ).decode("utf-8")

        user.token_version += 1

        db.session.commit()

        new_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "token_version": user.token_version
            }
        )

        return jsonify({
            "message": "Password changed successfully",
            "access_token": new_token
        }), 200


    # FIND THE CURRENT USER AND CHECK TOKEN VERSION
    def get_current_user():

        user_id = get_jwt_identity()

        user = db.session.get(User, int(user_id))

        if not user:
            return None

        token_version = get_jwt().get("token_version")

        if token_version != user.token_version:
            return None

        return user