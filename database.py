"""
=============================================================================
TrackIt — Parcel Tracking System (DevOps Laboratory Project)
Module 2: SQLite Database Layer & Tracking Engine
=============================================================================

This module manages all database operations for TrackIt using Python's
built-in sqlite3 library.

Key DevOps & Software Engineering Concepts:
1. Zero-Configuration: SQLite requires no separate server process, making it
   ideal for lightweight microservices, laboratory demos, and initial builds.
2. Parameterized Queries: All lookups use '?' placeholders to completely prevent
   SQL Injection vulnerabilities.
3. sqlite3.Row Factory: Allows accessing query columns by name (like dictionaries),
   making template rendering clean and readable.
4. Auto-Seeding: The database initializes schema and seed records automatically
   if it does not yet exist.
"""

import sqlite3
import os

# Path to the SQLite database file (supports TRACKIT_DB_PATH environment variable for Docker)
DB_FILE = os.environ.get("TRACKIT_DB_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "trackit.db"))


def get_db_connection():
    """
    Establishes and returns a connection to the SQLite database.
    Configures row_factory = sqlite3.Row for dictionary-like column access.
    """
    global DB_FILE
    db_dir = os.path.dirname(os.path.abspath(DB_FILE))
    if db_dir and not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir, exist_ok=True)
        except OSError:
            # Fallback to local working directory if volume path is not writable
            DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trackit.db")

    try:
        conn = sqlite3.connect(DB_FILE)
    except sqlite3.OperationalError:
        # Fallback to local directory if configured path failed
        DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trackit.db")
        conn = sqlite3.connect(DB_FILE)

    conn.row_factory = sqlite3.Row
    # Enable foreign key constraint enforcement in SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """
    Initializes the database schema and seeds initial parcel demonstration data.
    Called automatically on application startup.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Create 'shipments' table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_id TEXT UNIQUE NOT NULL,
            item_name TEXT NOT NULL,
            sender_name TEXT NOT NULL,
            receiver_name TEXT NOT NULL,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            status TEXT NOT NULL,
            status_class TEXT NOT NULL,
            carrier TEXT NOT NULL,
            estimated_delivery TEXT NOT NULL,
            current_location TEXT NOT NULL,
            progress_step INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 2. Create 'tracking_updates' table for tracking timeline / history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracking_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shipment_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            location TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (shipment_id) REFERENCES shipments (id) ON DELETE CASCADE
        );
    """)

    # 3. Check if table already has records; if empty, seed initial records
    cursor.execute("SELECT COUNT(*) FROM shipments;")
    count = cursor.fetchone()[0]

    if count == 0:
        # Seed initial parcels for demonstration in Module 2
        initial_shipments = [
            (
                "TRK-849201",
                "Electronics - Laboratory Equipment",
                "Prof. R. Sharma (IIT Bombay Hub)",
                "DevOps Lab In-Charge (Tech Campus)",
                "Mumbai Central Hub",
                "Bengaluru Tech Park",
                "In Transit",
                "in-transit",
                "Express Cargo",
                "Tomorrow, 6:00 PM",
                "Pune Highway Sorting Facility",
                3,
            ),
            (
                "TRK-552194",
                "DevOps Lab Manuals & Study Kits",
                "Academic Publications Ltd",
                "Central Library Department",
                "New Delhi Dispatch Hub",
                "Hyderabad Logistics Centre",
                "Shipped",
                "shipped",
                "BlueDart Logistics",
                "In 3 Days (Oct 17, 2026)",
                "Dispatched from Origin Sorting Facility",
                2,
            ),
            (
                "TRK-319402",
                "IoT Sensors & Microcontrollers",
                "Precision Hardware Hub",
                "Embedded Systems Lab Store",
                "Chennai Port Logistics",
                "Coimbatore Campus Store",
                "Delivered",
                "delivered",
                "SafeX Couriers",
                "Delivered on Oct 11, 2026, 2:45 PM",
                "Delivered to Campus Store Dept (Signed: Labs In-Charge)",
                5,
            ),
            (
                "TRK-109283",
                "Server Network Rack Components",
                "Datacenter Infrastructure Supplies",
                "Network Admin Office",
                "Pune Logistics Park",
                "Bengaluru Tech Park",
                "Out for Delivery",
                "in-transit",
                "SpeedPost Express",
                "Today, by 4:00 PM",
                "Out with Delivery Executive (Agent: Vijay K.)",
                4,
            ),
        ]

        for s in initial_shipments:
            cursor.execute("""
                INSERT INTO shipments (
                    tracking_id, item_name, sender_name, receiver_name,
                    origin, destination, status, status_class, carrier,
                    estimated_delivery, current_location, progress_step
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, s)

            shipment_id = cursor.lastrowid
            tracking_code = s[0]

            # Seed chronological timeline events for each shipment
            if tracking_code == "TRK-849201":
                updates = [
                    (shipment_id, "Order Placed", "Mumbai Central Hub", "Oct 11, 09:30 AM", "Package manifest created and electronic info received."),
                    (shipment_id, "Shipped", "Mumbai Central Sorting Centre", "Oct 12, 02:15 PM", "Parcel packed, scanned, and cleared through origin gateway."),
                    (shipment_id, "In Transit", "Pune Highway Sorting Facility", "Oct 13, 08:45 AM", "Arrived at regional transit hub; departed for destination tech park."),
                ]
            elif tracking_code == "TRK-552194":
                updates = [
                    (shipment_id, "Order Placed", "New Delhi Dispatch Hub", "Oct 12, 11:00 AM", "Shipment registered by Academic Publications Ltd."),
                    (shipment_id, "Shipped", "New Delhi Sorting Facility", "Oct 12, 06:30 PM", "Dispatched in line-haul freight towards Hyderabad."),
                ]
            elif tracking_code == "TRK-319402":
                updates = [
                    (shipment_id, "Order Placed", "Chennai Port Logistics", "Oct 09, 10:00 AM", "Pickup requested from Precision Hardware Hub."),
                    (shipment_id, "Shipped", "Chennai Port Logistics", "Oct 09, 05:40 PM", "Handed over to carrier network."),
                    (shipment_id, "In Transit", "Madurai Regional Hub", "Oct 10, 01:20 PM", "Processed through intermediate logistics facility."),
                    (shipment_id, "Out for Delivery", "Coimbatore Delivery Station", "Oct 11, 09:00 AM", "Loaded into local delivery vehicle."),
                    (shipment_id, "Delivered", "Coimbatore Campus Store", "Oct 11, 02:45 PM", "Package handed over and signed by Labs In-Charge."),
                ]
            elif tracking_code == "TRK-109283":
                updates = [
                    (shipment_id, "Order Placed", "Pune Logistics Park", "Oct 11, 08:00 AM", "Shipment booking confirmed."),
                    (shipment_id, "Shipped", "Pune Airport Facility", "Oct 11, 07:00 PM", "Air freight dispatch confirmed."),
                    (shipment_id, "In Transit", "Bengaluru Airport Hub", "Oct 12, 09:15 AM", "Sorted at destination air gateway."),
                    (shipment_id, "Out for Delivery", "Bengaluru Tech Park Station", "Oct 13, 08:30 AM", "Out for delivery with executive Vijay K."),
                ]
            else:
                updates = []

            for u in updates:
                cursor.execute("""
                    INSERT INTO tracking_updates (
                        shipment_id, status, location, timestamp, description
                    ) VALUES (?, ?, ?, ?, ?);
                """, u)

        conn.commit()

    conn.close()


def get_all_shipments():
    """
    Retrieves all shipments from the SQLite database.
    Used to render the demonstration/inventory cards on the homepage.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM shipments ORDER BY id ASC;
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_shipment_by_tracking_id(tracking_id):
    """
    Queries SQLite for a specific shipment by tracking ID (case-insensitive).
    Uses parameterized query '?' to eliminate SQL Injection risks.
    Returns a dictionary of shipment fields, or None if not found.
    """
    if not tracking_id:
        return None

    clean_id = tracking_id.strip()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM shipments 
        WHERE UPPER(tracking_id) = UPPER(?);
    """, (clean_id,))

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def get_shipment_updates(shipment_id):
    """
    Fetches the chronological event history for a shipment.
    Returns a list of event dictionaries ordered by event ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM tracking_updates 
        WHERE shipment_id = ? 
        ORDER BY id ASC;
    """, (shipment_id,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# =============================================================================
# MODULE 3: SHIPMENT MANAGEMENT & CRUD OPERATIONS
# =============================================================================

def get_shipment_by_id(shipment_id):
    """
    Retrieves a single shipment by its primary key ID.
    Returns a dictionary or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shipments WHERE id = ?;", (shipment_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_status_metadata(status):
    """
    Helper function to determine the CSS class and stepper milestone (1-5)
    based on the shipment's current status string.
    """
    clean_status = status.strip()
    mapping = {
        "Placed": ("shipped", 1),
        "Order Placed": ("shipped", 1),
        "Shipped": ("shipped", 2),
        "In Transit": ("in-transit", 3),
        "Out for Delivery": ("in-transit", 4),
        "Delivered": ("delivered", 5),
    }
    return mapping.get(clean_status, ("in-transit", 3))


def create_shipment(
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
):
    """
    Inserts a new shipment record into the database and adds the initial
    checkpoint milestone to tracking_updates.
    Returns (success: bool, message: str, shipment_id: int | None).
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if tracking_id already exists
    cursor.execute(
        "SELECT id FROM shipments WHERE UPPER(tracking_id) = UPPER(?);",
        (tracking_id.strip(),),
    )
    if cursor.fetchone():
        conn.close()
        return False, f"Tracking ID '{tracking_id}' already exists in the system.", None

    status_class, progress_step = get_status_metadata(status)

    cursor.execute(
        """
        INSERT INTO shipments (
            tracking_id, item_name, sender_name, receiver_name,
            origin, destination, status, status_class, carrier,
            estimated_delivery, current_location, progress_step
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """,
        (
            tracking_id.strip(),
            item_name.strip(),
            sender_name.strip(),
            receiver_name.strip(),
            origin.strip(),
            destination.strip(),
            status.strip(),
            status_class,
            carrier.strip(),
            estimated_delivery.strip(),
            current_location.strip(),
            progress_step,
        ),
    )

    shipment_id = cursor.lastrowid

    # Automatically log initial timeline checkpoint
    cursor.execute(
        """
        INSERT INTO tracking_updates (
            shipment_id, status, location, timestamp, description
        ) VALUES (?, ?, ?, datetime('now', 'localtime'), ?);
    """,
        (
            shipment_id,
            status.strip(),
            origin.strip(),
            f"Shipment registered and intake confirmed at {origin.strip()}.",
        ),
    )

    conn.commit()
    conn.close()
    return True, f"Shipment '{tracking_id}' registered successfully.", shipment_id


def update_shipment_status(
    shipment_id,
    new_status,
    carrier,
    estimated_delivery,
    current_location,
    checkpoint_description=None,
):
    """
    Updates an existing shipment's status, carrier, location, and timeline.
    Automatically calculates the progress milestone and inserts a new event
    into the tracking_updates table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    status_class, progress_step = get_status_metadata(new_status)

    cursor.execute(
        """
        UPDATE shipments 
        SET status = ?, 
            status_class = ?, 
            carrier = ?, 
            estimated_delivery = ?, 
            current_location = ?, 
            progress_step = ?
        WHERE id = ?;
    """,
        (
            new_status.strip(),
            status_class,
            carrier.strip(),
            estimated_delivery.strip(),
            current_location.strip(),
            progress_step,
            shipment_id,
        ),
    )

    # If checkpoint description is provided, append milestone to timeline
    desc = checkpoint_description.strip() if checkpoint_description else f"Status updated to '{new_status}' at {current_location}."
    cursor.execute(
        """
        INSERT INTO tracking_updates (
            shipment_id, status, location, timestamp, description
        ) VALUES (?, ?, ?, datetime('now', 'localtime'), ?);
    """,
        (shipment_id, new_status.strip(), current_location.strip(), desc),
    )

    conn.commit()
    conn.close()
    return True, f"Shipment status updated to '{new_status}' successfully."


def delete_shipment(shipment_id):
    """
    Deletes a shipment from the database.
    Because of ON DELETE CASCADE, child tracking_updates records are also deleted.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT tracking_id FROM shipments WHERE id = ?;", (shipment_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, "Shipment not found."

    tracking_id = row["tracking_id"]

    # Delete child updates first (explicitly for maximum SQLite portability)
    cursor.execute("DELETE FROM tracking_updates WHERE shipment_id = ?;", (shipment_id,))
    cursor.execute("DELETE FROM shipments WHERE id = ?;", (shipment_id,))

    conn.commit()
    conn.close()
    return True, f"Shipment '{tracking_id}' was deleted successfully."


def get_kpi_stats():
    """
    Calculates summary KPIs for the admin dashboard:
    - Total shipments
    - In Transit count
    - Shipped count
    - Out for Delivery count
    - Delivered count
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM shipments;")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM shipments WHERE status = 'In Transit';")
    in_transit = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM shipments WHERE status = 'Shipped';")
    shipped = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM shipments WHERE status = 'Out for Delivery';")
    out_for_delivery = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM shipments WHERE status = 'Delivered';")
    delivered = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "in_transit": in_transit,
        "shipped": shipped,
        "out_for_delivery": out_for_delivery,
        "delivered": delivered,
        "active": in_transit + shipped + out_for_delivery,
    }
