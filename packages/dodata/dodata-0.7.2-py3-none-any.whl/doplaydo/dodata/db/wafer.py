"""This modules contains functions for querying the database for wafer objects."""

from collections.abc import Sequence

from sqlalchemy.sql import ColumnElement
from sqlmodel import Session
from sqlmodel.sql.expression import SelectOfScalar

from doplaydo.dodata_core import models as m

from .. import select
from .die import _get_die_joined_query


def _get_wafer_joined_query() -> SelectOfScalar[m.Wafer]:
    return (
        select(m.Wafer)
        .join(m.Die)
        .join(m.Project, m.Wafer.project_pkey == m.Project.pkey)
        .join(m.Analysis, m.Analysis.wafer_pkey == m.Wafer.pkey, isouter=True)
        .join(
            m.AnalysisFunction,
            onclause=m.Analysis.analysis_function_pkey == m.AnalysisFunction.pkey,
            isouter=True,
        )
    )


def get_wafers_by_query(
    clauses: list[ColumnElement[bool] | bool],
    *,
    session: Session,
) -> Sequence[m.Wafer]:
    """Return a list of filtered wafers.

    Args:
        clauses: sql expressions such as `dd.Cell.cell_id == "RibLoss"`.
        session: sqlmodel Session, can be retrieved with `get_session()`.
    """
    statement = _get_wafer_joined_query()

    for clause in clauses:
        statement = statement.where(clause)

    _wafers = session.exec(statement).all()
    return _wafers


def get_by_id(
    project_id: str,
    wafer_id: str,
    *,
    session: Session,
) -> Sequence[m.Wafer]:
    """Get a wafer by project name and wafer name.

    Args:
        project_id: The project name.
        wafer_id: The wafer name.
        session: sqlmodel Session, can be retrieved with `get_session()`.
    """
    return get_wafers_by_query(
        [m.Project.project_id == project_id, m.Wafer.wafer_id == wafer_id]
    )


def get_by_pkey(
    wafer_pkey: int,
    *,
    session: Session,
) -> m.Wafer:
    """Get a wafer by its unique pkey.

    Args:
        wafer_pkey: Primary key of the wafer.
        session: sqlmodel Session, can be retrieved with `get_session()`.
    """
    _wafers = get_wafers_by_query([m.Wafer.pkey == wafer_pkey])

    if not _wafers:
        raise ValueError(f"Could not find wafer with {wafer_pkey=}")

    return _wafers[0]


def get_wafer_dies(
    wafer_id: str,
    project_id: str,
    clauses: list[ColumnElement[bool] | bool],
    *,
    session: Session,
) -> Sequence[m.Die]:
    """Return a list of filtered wafer dies.

    Args:
        wafer_id: The wafer name.
        project_id: The project name.
        clauses: A list of sqlalchemy clauses to filter the dies.
        session: sqlmodel Session, can be retrieved with `get_session()`.
    """
    statement = _get_die_joined_query()

    clauses.append(m.Project.project_id == project_id)
    clauses.append(m.Wafer.wafer_id == wafer_id)

    for clause in clauses:
        statement = statement.where(clause)

    _dies = session.exec(statement).all()
    return _dies
