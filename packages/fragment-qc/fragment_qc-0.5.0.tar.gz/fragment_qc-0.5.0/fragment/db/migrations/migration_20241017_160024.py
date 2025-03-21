#
# Copyright 2018-2025 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
"""Migration migration_20241017_160024.py

There a spelling error `primative` --> `primitive`. It has been corrected
in the code. This migration update the ViewNode table to fix this.
"""
import peewee
from playhouse.migrate import SqliteMigrator
from playhouse.migrate import migrate as run_migration


def migrate(project_path: str, database: peewee.Database) -> None:
    table_name = "view_node"
    old_column_name = "is_primative"
    new_column_name = "is_primitive"

    # Check that the spelling error exists in the database
    column_names = [c.name for c in database.get_columns(table_name)]
    if new_column_name in column_names:
        return  # Do nothing. This database is fine!

    # Rename the column!
    migrator = SqliteMigrator(database)
    run_migration(
        migrator.rename_column(table_name, old_column_name, new_column_name),
    )
