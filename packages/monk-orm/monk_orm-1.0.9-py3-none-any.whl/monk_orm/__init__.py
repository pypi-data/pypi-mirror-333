# -*- coding: utf-8; -*-
#
# Licensed to MonkDB Labs Private Limited (MonkDB) under one or more contributor
# license agreements.  See the NOTICE file distributed with this work for
# additional information regarding copyright ownership.  MonkDB licenses
# this file to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may
# obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.

from monk_orm import dialect
from monk_orm.compat.api13 import monkeypatch_add_exec_driver_sql
from monk_orm.predicate import match
from monk_orm.sa_version import SA_1_4, SA_VERSION
from monk_orm.support.pandas import insert_bulk
from monk_orm.type.array import ObjectArray
from monk_orm.type.geospatial import Geopoint, Geoshape
from monk_orm.type.objects import ObjectType
from monk_orm.type.vector import FloatVector, knn_match


if SA_VERSION < SA_1_4:
    import textwrap
    import warnings

    # SQLAlchemy 1.3 is effectively EOL.
    SA13_DEPRECATION_WARNING = textwrap.dedent(
        """
    WARNING: SQLAlchemy 1.3 has reached its end of life. 
    
    Therefore, future versions of MonkDB will deprecate the support for SA 1.3. 
    
    Please update to either SA 1.4 or SA 2.0 for seamless operations. 
    """.lstrip("\n")
    )
    warnings.warn(message=SA13_DEPRECATION_WARNING,
                  category=DeprecationWarning, stacklevel=2)

    # SQLAlchemy 1.3 does not have the `exec_driver_sql` method, so add it.
    monkeypatch_add_exec_driver_sql()

try:
    from importlib.metadata import PackageNotFoundError, version
except (ImportError, ModuleNotFoundError):  # pragma:nocover
    from importlib_metadata import (  # type: ignore[assignment,no-redef,unused-ignore]
        PackageNotFoundError,
        version,
    )

try:
    __version__ = version("monk-orm")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

__all__ = [
    __version__,
    dialect,
    FloatVector,
    Geopoint,
    Geoshape,
    ObjectArray,
    ObjectType,
    match,
    knn_match,
    insert_bulk,
]
