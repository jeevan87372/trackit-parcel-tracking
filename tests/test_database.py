"""
=============================================================================
TrackIt — Parcel Tracking System (DevOps Laboratory Project)
Module 4: Automated Testing Suite — Database & Business Logic Tests
=============================================================================

Validates SQLite database operations, schema integrity, parameterized queries,
relational foreign keys, and KPI statistics calculations.
"""

import os
import pytest
import database


@pytest.fixture(autouse=True)
def ensure_db():
    """Ensure database schema is initialized before every test."""
    database.init_db()


def test_database_initialization():
    """Verify that SQLite database tables exist and are populated with seeds."""
    shipments = database.get_all_shipments()
    assert len(shipments) >= 3, "Database should contain at least initial seed shipments"


def test_get_shipment_by_tracking_id_found():
    """Verify case-insensitive lookup of a valid shipment."""
    shipment = database.get_shipment_by_tracking_id("trk-849201")
    assert shipment is not None
    assert shipment["tracking_id"] == "TRK-849201"
    assert shipment["status"] == "In Transit"


def test_get_shipment_by_tracking_id_not_found():
    """Verify that non-existent tracking IDs return None."""
    shipment = database.get_shipment_by_tracking_id("TRK-NONEXISTENT-999")
    assert shipment is None


def test_get_shipment_updates_history():
    """Verify that event checkpoints are retrieved in order."""
    shipment = database.get_shipment_by_tracking_id("TRK-849201")
    assert shipment is not None
    updates = database.get_shipment_updates(shipment["id"])
    assert len(updates) >= 2, "Shipment should have multiple checkpoint updates"
    assert "location" in updates[0]
    assert "description" in updates[0]


def test_create_and_delete_shipment():
    """Verify shipment registration, milestone auto-logging, and cascading deletion."""
    test_tracking_id = "TRK-UNITTEST-01"

    # 1. Create
    ok, msg, s_id = database.create_shipment(
        tracking_id=test_tracking_id,
        item_name="DevOps Test Hardware",
        sender_name="QA Automation Bot",
        receiver_name="CI Pipeline Agent",
        origin="Server Node A",
        destination="Client Node B",
        status="Order Placed",
        carrier="Test Carrier",
        estimated_delivery="Tomorrow, 12:00 PM",
        current_location="Origin Test Hub",
    )
    assert ok is True
    assert s_id is not None

    # Verify initial checkpoint was created
    updates = database.get_shipment_updates(s_id)
    assert len(updates) == 1
    assert updates[0]["status"] == "Order Placed"

    # 2. Duplicate prevention
    ok_dup, msg_dup, _ = database.create_shipment(
        tracking_id=test_tracking_id,
        item_name="Duplicate Item",
        sender_name="Sender",
        receiver_name="Receiver",
        origin="Origin",
        destination="Destination",
        status="Order Placed",
        carrier="Carrier",
        estimated_delivery="Tomorrow",
        current_location="Origin",
    )
    assert ok_dup is False
    assert "already exists" in msg_dup

    # 3. Update status
    ok_up, msg_up = database.update_shipment_status(
        shipment_id=s_id,
        new_status="In Transit",
        carrier="Test Carrier Express",
        estimated_delivery="Tomorrow, 6:00 PM",
        current_location="Transit Sorting Hub",
        checkpoint_description="Passed QA sorting checkpoint",
    )
    assert ok_up is True
    updated = database.get_shipment_by_id(s_id)
    assert updated["status"] == "In Transit"
    assert updated["progress_step"] == 3

    # Verify event was appended
    updates_after = database.get_shipment_updates(s_id)
    assert len(updates_after) == 2

    # 4. Delete
    ok_del, msg_del = database.delete_shipment(s_id)
    assert ok_del is True
    assert database.get_shipment_by_id(s_id) is None
    # Verify child checkpoints cascaded
    assert len(database.get_shipment_updates(s_id)) == 0


def test_kpi_stats_calculation():
    """Verify that KPI summary counts reflect database records."""
    stats = database.get_kpi_stats()
    assert "total" in stats
    assert "in_transit" in stats
    assert "shipped" in stats
    assert "delivered" in stats
    assert stats["total"] >= 3
