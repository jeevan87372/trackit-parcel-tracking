"""
=============================================================================
TrackIt — Parcel Tracking System (DevOps Laboratory Project)
Module 3: Admin Operations, Authentication & Complete Shipment Management (CRUD)
=============================================================================

This file is the main Flask application entry point.
In Module 3:
- Introduces Session-Based Admin Authentication (/login, /logout, @admin_required).
- Adds Admin Operations Dashboard (/admin) with KPI statistics.
- Implements Full CRUD Operations for Shipments:
  * Create: Parcel intake registration (/admin/shipments/new)
  * Read: Search parcel & view inventory
  * Update: Advance parcel milestone, location, & log timeline checkpoints (/admin/shipments/<id>/update)
  * Delete: Remove parcel & cascade timeline history (/admin/shipments/<id>/delete)
- Maintains Public Tracking Engine at / with SQLite database integration.
"""

from functools import wraps
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)
import database

# Initialize the Flask application
app = Flask(__name__)

# Secret key for encrypting session cookies (Required for session & flash messaging)
app.secret_key = "trackit-devops-lab-module3-secret-key-2026"

# Auto-initialize SQLite database schema and seeds on startup
database.init_db()


# ---------------------------------------------------------------------------
# Authentication Helper / Route Protection Decorator
# ---------------------------------------------------------------------------
def admin_required(f):
    """
    Decorator to protect administrative endpoints.
    Verifies that the user has an active session before granting access.
    Redirects unauthenticated users to the /login page with a flash notice.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Please sign in with administrator credentials to access the console.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# ---------------------------------------------------------------------------
# Public Routes (Homepage & Tracking Engine)
# ---------------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Public Homepage & Live Parcel Tracking Engine.
    Queries SQLite database via parameterized statements.
    """
    searched_id = None
    search_status = None
    searched_shipment = None
    shipment_events = []
    error_message = None

    if request.method == "POST":
        searched_id = request.form.get("tracking_id", "").strip()
    elif request.method == "GET" and request.args.get("tracking_id"):
        searched_id = request.args.get("tracking_id", "").strip()

    if searched_id:
        searched_shipment = database.get_shipment_by_tracking_id(searched_id)

        if searched_shipment:
            search_status = "found"
            shipment_events = database.get_shipment_updates(searched_shipment["id"])
        else:
            search_status = "not_found"
            error_message = (
                f"No shipment found matching tracking ID '{searched_id}'. "
                "Please verify the code or try one of the demonstration IDs below."
            )

    all_shipments = database.get_all_shipments()

    return render_template(
        "index.html",
        sample_shipments=all_shipments,
        searched_id=searched_id,
        search_status=search_status,
        shipment=searched_shipment,
        shipment_events=shipment_events,
        error_message=error_message,
        module_version="Module 4 — Docker Containerization & CI/CD Pipelines",
    )


@app.route("/health")
def health():
    """
    Container & DevOps Service Healthcheck Endpoint.
    Returns HTTP 200 JSON payload for container monitoring and pipeline smoke tests.
    """
    stats = database.get_kpi_stats()
    return {
        "status": "healthy",
        "service": "TrackIt Parcel Tracking System",
        "module": 4,
        "database": "SQLite (Connected)",
        "active_shipments": stats["active"],
        "total_shipments": stats["total"],
    }, 200


@app.route("/favicon.ico")
def favicon():
    """Return empty response with 204 No Content for favicon requests."""
    return "", 204


# ---------------------------------------------------------------------------
# Admin Authentication Routes
# ---------------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Administrator Sign-In Portal.
    Demonstrates session management and credential verification.
    """
    if session.get("logged_in"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        # Demo Credentials for DevOps Lab evaluation
        if username == "admin" and password == "admin123":
            session["logged_in"] = True
            session["admin_user"] = username
            flash("Welcome to TrackIt Operations & Dispatch Console.", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid credentials. Please enter valid admin credentials (admin / admin123).", "error")

    return render_template("admin/login.html")


@app.route("/logout")
def logout():
    """
    Clears administrator session and redirects to sign-in page.
    """
    session.clear()
    flash("You have been signed out of the admin console.", "info")
    return redirect(url_for("login"))


# ---------------------------------------------------------------------------
# Admin Dashboard & CRUD Operations
# ---------------------------------------------------------------------------
@app.route("/admin")
@admin_required
def admin_dashboard():
    """
    Admin Dashboard: Displays KPI counters and management table of all parcels.
    """
    shipments = database.get_all_shipments()
    stats = database.get_kpi_stats()
    return render_template("admin/dashboard.html", shipments=shipments, stats=stats)


@app.route("/admin/shipments/new", methods=["GET", "POST"])
@admin_required
def new_shipment():
    """
    Parcel Intake: Registers a new consignment into SQLite.
    """
    if request.method == "POST":
        tracking_id = request.form.get("tracking_id", "").strip().upper()
        item_name = request.form.get("item_name", "").strip()
        sender_name = request.form.get("sender_name", "").strip()
        receiver_name = request.form.get("receiver_name", "").strip()
        origin = request.form.get("origin", "").strip()
        destination = request.form.get("destination", "").strip()
        status = request.form.get("status", "Shipped").strip()
        carrier = request.form.get("carrier", "Express Cargo").strip()
        estimated_delivery = request.form.get("estimated_delivery", "").strip()
        current_location = request.form.get("current_location", "").strip()

        success, msg, _ = database.create_shipment(
            tracking_id,
            item_name,
            sender_name,
            receiver_name,
            origin,
            destination,
            status,
            carrier,
            estimated_delivery,
            current_location,
        )

        if success:
            flash(f"Consignment '{tracking_id}' registered successfully into database.", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash(msg, "error")

    return render_template("admin/new_shipment.html")


@app.route("/admin/shipments/<int:id>/update", methods=["GET", "POST"])
@admin_required
def update_shipment(id):
    """
    Shipment Update: Advances status, updates location, and logs checkpoint.
    """
    shipment = database.get_shipment_by_id(id)
    if not shipment:
        flash("Shipment record not found.", "error")
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        new_status = request.form.get("status", shipment["status"]).strip()
        carrier = request.form.get("carrier", shipment["carrier"]).strip()
        estimated_delivery = request.form.get("estimated_delivery", shipment["estimated_delivery"]).strip()
        current_location = request.form.get("current_location", shipment["current_location"]).strip()
        checkpoint_desc = request.form.get("checkpoint_desc", "").strip()

        database.update_shipment_status(
            id,
            new_status,
            carrier,
            estimated_delivery,
            current_location,
            checkpoint_desc,
        )

        flash(f"Shipment '{shipment['tracking_id']}' status updated to '{new_status}' and logged to timeline.", "success")
        return redirect(url_for("admin_dashboard"))

    updates = database.get_shipment_updates(id)
    return render_template("admin/update_shipment.html", shipment=shipment, updates=updates)


@app.route("/admin/shipments/<int:id>/delete", methods=["POST"])
@admin_required
def delete_shipment(id):
    """
    Shipment Deletion: Removes record from database.
    """
    success, msg = database.delete_shipment(id)
    if success:
        flash(msg, "success")
    else:
        flash(msg, "error")
    return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
