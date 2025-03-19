# pyramid-helpers -- Helpers to develop Pyramid applications
# By: Cyril Lacoux <clacoux@easter-eggs.com>
#     Valéry Febvre <vfebvre@easter-eggs.com>
#
# Copyright (C) Cyril Lacoux, Easter-eggs
# https://gitlab.com/yack/pyramid-helpers
#
# This file is part of pyramid-helpers.
#
# pyramid-helpers is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# pyramid-helpers is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" SQLAlchemy utilities for Pyramid """

from sqlalchemy.orm import mapperlib
from sqlalchemy.schema import Table
from sqlalchemy.sql.annotation import AnnotatedAlias    # pylint: disable=no-name-in-module
from sqlalchemy.sql.util import find_tables


def get_entity(clause, name):
    """ Get entity by name from SQL clause """

    for entity in find_tables(clause, include_joins=True, include_aliases=True):
        if isinstance(entity, Table):
            for mapper in get_mappers(entity):
                if mapper.class_.__name__.lower() == name:
                    return mapper.entity_namespace

        elif isinstance(entity, AnnotatedAlias) and entity.name.lower() == name:
            return entity.entity_namespace

    return None


def get_mappers(table):
    """ Return associated declarative class(es) from table """

    mappers = {
        mapper
        for mapper_registry in mapperlib._all_registries()  # pylint: disable=protected-access
        for mapper in mapper_registry.mappers
        if table in mapper.tables
    }

    return sorted(mappers, key=lambda mapper: mapper.class_.__name__)
