import sqlite3
from pathlib import Path


DATABASE_PATH = Path("backend/healthtriage.db")


def get_connection():
    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # =========================================================
    # CASES TABLE
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cases (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            case_id TEXT UNIQUE NOT NULL,

            patient_name TEXT,

            age INTEGER,

            gender TEXT,

            existing_conditions TEXT,

            symptoms TEXT,

            triage_level TEXT,

            confidence REAL,

            summary TEXT,

            reasoning TEXT,

            human_review_required INTEGER,

            final_decision TEXT,

            status TEXT DEFAULT 'WAITING',

            image_filename TEXT,

            image_stored_as TEXT,

            image_file_type TEXT,

            voice_transcript TEXT,

            detected_factors TEXT,

            report_analysis TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # =========================================================
    # DATABASE MIGRATIONS
    # =========================================================
    #
    # These checks make sure older databases receive
    # columns that were added after the initial version.
    # =========================================================

    cursor.execute("PRAGMA table_info(cases)")

    existing_columns = {
        column[1]
        for column in cursor.fetchall()
    }

    # Add status column if an older database does not have it
    if "status" not in existing_columns:

        cursor.execute("""
            ALTER TABLE cases
            ADD COLUMN status TEXT DEFAULT 'WAITING'
        """)

    # Add voice transcript column if missing
    if "voice_transcript" not in existing_columns:

        cursor.execute("""
            ALTER TABLE cases
            ADD COLUMN voice_transcript TEXT
        """)

    # Add detected factors column if missing
    if "detected_factors" not in existing_columns:

        cursor.execute("""
            ALTER TABLE cases
            ADD COLUMN detected_factors TEXT
        """)

    # Add report analysis column if missing
    if "report_analysis" not in existing_columns:

        cursor.execute("""
            ALTER TABLE cases
            ADD COLUMN report_analysis TEXT
        """)

    # Add image filename column if missing
    if "image_filename" not in existing_columns:

        cursor.execute("""
            ALTER TABLE cases
            ADD COLUMN image_filename TEXT
        """)

    # Add stored image filename column if missing
    if "image_stored_as" not in existing_columns:

        cursor.execute("""
            ALTER TABLE cases
            ADD COLUMN image_stored_as TEXT
        """)

    # Add image file type column if missing
    if "image_file_type" not in existing_columns:

        cursor.execute("""
            ALTER TABLE cases
            ADD COLUMN image_file_type TEXT
        """)

    # =========================================================
    # AUDIT LOG TABLE
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS case_audit_log (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            case_id TEXT NOT NULL,

            action TEXT NOT NULL,

            previous_decision TEXT,

            new_decision TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # =========================================================
    # COMMIT
    # =========================================================

    connection.commit()
    connection.close()