"""This modules contains functions for querying the database for wafer objects."""

from collections.abc import Sequence

from sqlalchemy.sql import ColumnElement
from sqlmodel import Session
from sqlmodel.sql.expression import SelectOfScalar

from doplaydo.dodata_core import models as m

from .. import select


def _get_die_joined_query() -> SelectOfScalar[m.Die]:
    return (
        select(m.Die)
        .join(m.Wafer)
        .join(m.Analysis, m.Analysis.die_pkey == m.Die.pkey, isouter=True)
        .join(m.Project, m.Wafer.project_pkey == m.Project.pkey)
        .join(
            m.AnalysisFunction,
            onclause=m.Analysis.analysis_function_pkey == m.AnalysisFunction.pkey,
            isouter=True,
        )
    )


def get_dies_by_query(
    clauses: list[ColumnElement[bool] | bool],
    *,
    session: Session,
) -> Sequence[m.Die]:
    """Return a list of filtered wafers.

    Args:
        clauses: sql expressions such as `dd.Cell.cell_id == "RibLoss"`.
        session: sqlmodel Session, can be retrieved with `get_session()`.
    """
    statement = _get_die_joined_query()

    for clause in clauses:
        statement = statement.where(clause)

    _wafers = session.exec(statement).all()

    return _wafers


def get_by_pkey(
    die_pkey: int,
    *,
    session: Session,
) -> m.Die:
    """Get a wafer by its unique pkey.

    Args:
        die_pkey: Primary key of the Die.
        session: sqlmodel Session, can be retrieved with `get_session()`.
    """
    _dies = get_dies_by_query([m.Die.pkey == die_pkey], session=session)

    if not _dies:
        raise ValueError(f"Could not find die with {die_pkey=}")

    return _dies[0]
