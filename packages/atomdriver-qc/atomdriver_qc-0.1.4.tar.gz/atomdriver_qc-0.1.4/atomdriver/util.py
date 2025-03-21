#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
from atomdriver.accessors import DriverAccessor

# # Handle driver calls
# if isinstance(in_value, System) and isinstance(stage, Driver):
#     accessor = self.get_driver(stage, *args)
#     accessor.submit(in_value)
#     while True:  # Oooh. Infinite loop ;)
#         completed = accessor.get_completed()
#         if not completed:
#             yield
#         else:
#             _sys, rec = completed[0]
#             return rec


class SystemCalculationRunner:
    # 1 Setup
    def __init__(self, system, accessor: DriverAccessor) -> None:
        ...

    # 2 Check
    # Do this to keep inline with accessor protocol?
    def get_completed(self):
        ...

    # 3 Complete
    def clean(self) -> None:
        ...

    # Add iterator?
