"""
=============================================================================
TrackIt — Parcel Tracking System (DevOps Laboratory Project)
Module 4: Automated Testing Suite — Flask HTTP Endpoints & Auth Tests
=============================================================================

Validates web routes, session security, authentication guards, and CRUD workflows
via Flask's test client.
"""

import pytest
from app import app
import database


@pytest.fixture
def client():
    """Create a configured Flask test client."""
    app.config["TESTING"] = True
    database.init_db()
    with app.test_client() as client:
        yield client


def test_public_homepage_renders(client):
    """Verify that the public homepage responds with HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"TrackIt" in response.data
    assert b"Parcel Tracking System" in response.data


def test_public_search_valid_parcel(client):
    """Verify searching for a valid parcel renders live record."""
    response = client.post("/", data={"tracking_id": "TRK-849201"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"LIVE DATABASE RECORD FOUND" in response.data
    assert b"TRK-849201" in response.data


def test_public_search_invalid_parcel(client):
    """Verify searching for an unknown tracking ID displays error notice."""
    response = client.post("/", data={"tracking_id": "TRK-UNKNOWN-404"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Shipment Not Found in Database" in response.data


def test_favicon_endpoint(client):
    """Verify favicon route returns 204 No Content."""
    response = client.get("/favicon.ico")
    assert response.status_code == 204


def test_health_endpoint(client):
    """Verify container healthcheck endpoint returns JSON status 200."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["module"] == 4


def test_admin_route_unauthenticated_redirect(client):
    """Verify unauthenticated user cannot access /admin and is redirected to /login."""
    response = client.get("/admin", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_admin_login_failure(client):
    """Verify invalid credentials fail authentication and stay on login page."""
    response = client.post(
        "/login",
        data={"username": "wronguser", "password": "wrongpassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid credentials" in response.data


def test_admin_login_success_and_logout(client):
    """Verify valid admin login grants session access and logout clears it."""
    # 1. Login
    response = client.post(
        "/login",
        data={"username": "admin", "password": "admin123"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Shipment Management Center" in response.data

    # 2. Access dashboard
    dash_response = client.get("/admin")
    assert dash_response.status_code == 200

    # 3. Logout
    logout_response = client.get("/logout", follow_redirects=True)
    assert logout_response.status_code == 200
    assert b"Admin Authentication" in logout_response.data

    # 4. Attempting dashboard access again redirects
    dash_after = client.get("/admin")
    assert dash_after.status_code == 302


def test_admin_crud_workflow(client):
    """End-to-end integration test: Admin signs in, creates a parcel, updates it, and deletes it."""
    # Authenticate
    client.post("/login", data={"username": "admin", "password": "admin123"})

    test_id = "TRK-CI-778899"

    # 1. Create parcel via Admin form
    create_resp = client.post(
        "/admin/shipments/new",
        data={
            "tracking_id": test_id,
            "item_name": "CI Test Deployment Package",
            "sender_name": "Jenkins Worker Node",
            "receiver_name": "Staging Server Target",
            "origin": "Build Agent",
            "destination": "Production Cluster",
            "status": "Order Placed",
            "carrier": "DevOps Express",
            "estimated_delivery": "Today, 5:00 PM",
            "current_location": "CI Pipeline Runner",
        },
        follow_redirects=True,
    )
    assert create_resp.status_code == 200
    assert b"registered successfully" in create_resp.data

    # Verify parcel exists in DB
    shipment = database.get_shipment_by_tracking_id(test_id)
    assert shipment is not None
    s_id = shipment["id"]

    # 2. Update parcel
    update_resp = client.post(
        f"/admin/shipments/{s_id}/update",
        data={
            "status": "In Transit",
            "carrier": "DevOps Express",
            "estimated_delivery": "Today, 6:00 PM",
            "current_location": "Quality Gate 1",
            "checkpoint_desc": "Passed automated security audit",
        },
        follow_redirects=True,
    )
    assert update_resp.status_code == 200
    assert b"status updated" in update_resp.data

    # Verify update in DB
    updated_shipment = database.get_shipment_by_id(s_id)
    assert updated_shipment["status"] == "In Transit"

    # 3. Delete parcel
    delete_resp = client.post(f"/admin/shipments/{s_id}/delete", follow_redirects=True)
    assert delete_resp.status_code == 200
    assert b"deleted successfully" in delete_resp.data
    assert database.get_shipment_by_id(s_id) is None
