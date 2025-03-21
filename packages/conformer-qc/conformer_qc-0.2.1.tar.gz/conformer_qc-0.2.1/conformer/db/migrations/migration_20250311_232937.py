#
# Copyright 2018-2025 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
"""Migration migration_20250311_232937.py

Non-canonized matrix-based data was being stored in the database.

This could happen when a NamedSystem was passed directly to a driver in the CLI.
This migration attempts to fix the issue. Given the sparsity of matrix-based
data (no pun intended), this scripts just assumes that all data generated this
way per-migration is problematic
"""

import peewee

from conformer.db.models import DBSystemRecord
from conformer.project import Project
from conformer_core.db.models import DBCalculationRecord as CR


def migrate(project: Project, database_path: peewee.Database) -> None:
    # Get all the calculations in the database!
    calc_names = [c[0] for c in CR.all_calculation_names()]

    # Do nothing if this DB has no calculations
    if not calc_names:
        return

    for calc in project.get_calculations(*calc_names).values():
        if len(calc.steps) != 2:
            continue

        (step1, (system,)), (driver_name, _) = calc.steps

        # Make sure that the first argument is '_get_system'
        if step1 != "_get_system":
            continue

        system = project.get_systems(system)[system]
        canon_system = system.canonize()
        driver = project.get_stage(driver_name)

        # Canon system wont re-sort rows and columns
        rec = DBSystemRecord.get_system_records(driver, [canon_system])[canon_system]

        # Skip the swap step!
        rec.system = system

        # For a swap from name_system --> canon_system
        canon_rec = rec.swap_system(canon_system)
        assert canon_rec.id == rec.id

        # Save
        DBSystemRecord.add_or_update_system_record([canon_rec], add_only=False)

        db_rec = DBSystemRecord.get_system_records(driver, [canon_system])[canon_system]

        import numpy as np

        np.testing.assert_allclose(
            db_rec.properties["nuclear_gradient"],
            canon_rec.properties["nuclear_gradient"],
        )
