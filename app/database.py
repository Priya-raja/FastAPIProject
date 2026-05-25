"""Module providing a database methods."""
import sqlite3
from typing import Any
from contextlib import contextmanager

from schemas import ShipmentCreate, ShipmentUpdate


class Database:
    """Manage SQLite operations for shipment records."""

    def __init__(self) -> None:
        """Initialize database attributes before opening a connection."""
        self.conn: sqlite3.Connection | None = None
        self.cur: sqlite3.Cursor | None = None

    def connect_to_db(self) -> None:
        """Open the SQLite connection and store a cursor for reuse."""
        # Make connection with database
        if self.conn is not None:
            self.conn.close()
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        # Get cursor to execute queries and fetch data
        self.cur = self.conn.cursor()
        print("connected to sqlite.db ...")

    def create_table(self) -> None:
        """Create the shipment table and migrate older schemas when needed."""
        # Create a table with columns
        assert self.cur is not None
        assert self.conn is not None
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS shipment (
                id INTEGER PRIMARY KEY,
                content TEXT,
                weight REAL,
                status TEXT,
                destination INTEGER
            )
            """
        )
        self._migrate_shipment_table()
        self.conn.commit()

    def _migrate_shipment_table(self) -> None:
        """Add missing columns required by the current shipment schema."""
        assert self.cur is not None
        self.cur.execute("PRAGMA table_info(shipment)")
        columns = {row[1] for row in self.cur.fetchall()}

        if "destination" not in columns:
            self.cur.execute(
                """
                ALTER TABLE shipment
                ADD COLUMN destination INTEGER NOT NULL DEFAULT 0
                """
            )

    def create(self, shipment: ShipmentCreate) -> int:
        """Insert a shipment row and return the new identifier."""
        # Find a new id
        assert self.cur is not None
        self.cur.execute("SELECT MAX(id) FROM shipment")
        result = self.cur.fetchone()

        new_id = (result[0] or 0) + 1

        # Insert values in the table
        self.cur.execute(
            """
            INSERT INTO shipment (id, content, weight, status, destination)
            VALUES (:id, :content, :weight, :status, :destination)
            """,
            {
                "id": new_id,
                **shipment.model_dump(),
                "status": "placed",
            },
        )
        # Commit the change to the database
        assert self.conn is not None
        self.conn.commit()

        return new_id

    def get(self, shipment_id: int) -> dict[str, Any] | None:
        """Fetch a shipment row by identifier."""
        assert self.cur is not None
        self.cur.execute(
            """
            SELECT * FROM shipment
            WHERE id = ?
            """,
            (shipment_id,),
        )
        row = self.cur.fetchone()

        return (
            {
                "id": row[0],
                "content": row[1],
                "weight": row[2],
                "status": row[3],
                "destination": row[4],
            }
            if row
            else None
        )

    def update(self, shipment_id: int, shipment: ShipmentUpdate) -> dict[str, Any] | None:
        """Update a shipment row and return the refreshed record."""
        assert self.cur is not None
        assert self.conn is not None
        self.cur.execute(
            """
            UPDATE shipment SET status = :status
            WHERE id = :id
            """,
            {
                "id": shipment_id,
                **shipment.model_dump(),
            },
        )
        self.conn.commit()

        return self.get(shipment_id)

    def delete(self, shipment_id: int) -> None:
        """Delete a shipment row by identifier."""
        assert self.cur is not None
        assert self.conn is not None
        self.cur.execute(
            """
            DELETE FROM shipment
            WHERE id = ?
            """,
            (shipment_id,),
        )
        self.conn.commit()

    def close(self) -> None:
        """Close the open database connection."""
        print("...connection closed")
        if self.conn is not None:
            self.conn.close()


    # def __enter__(self):
    #     """Enable use of the database as a context manager."""
    #     print("...entering context manager")
    #     self.connect_to_db()
    #     self.create_table()
    #     return self
    # def __exit__(self, *args):
    #     """Ensure the database connection is closed when exiting a context."""
    #     print("...exiting context manager")
    #     self.close()

# Use the @decorator instead of the above function 
# write main function to test the context manager

if __name__ == "__main__":
    @contextmanager
    def manage_database():
        """Provide a context manager for database operations."""
        db = Database()
    
        print("...entering context manager")
        db.connect_to_db()
        db.create_table()
        yield db    
        
        print("...exiting context manager")
        db.close()

    # usage example
    with manage_database() as db:
        print(db.get(12701))

