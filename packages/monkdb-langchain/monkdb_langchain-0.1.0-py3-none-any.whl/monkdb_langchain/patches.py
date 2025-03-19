import warnings

from monk_orm.query_compiler import MonkDBDDLCompiler


def ddl_compiler_visit_create_index(self, create, **kw) -> str:  # type: ignore[no-untyped-def]
    """
    MonkDB does not support `CREATE INDEX` statements as on today.
    """
    warnings.warn(
        "MonkDB does not support `CREATE INDEX` statements as on today, "
        "and they will be omitted when generating DDL statements.",
        stacklevel=2,
    )
    return "SELECT 1"


def patch_sqlalchemy_dialect() -> None:
    """
    This patch fixes `AttributeError: 'MonkDBCompilerSA20' object has no attributes 'visit_on_conflict_do_update' and
    '_on_conflict_target'`

    TODO: Upstream to `monk_orm`.
    """  # noqa: E501
    from sqlalchemy.dialects.postgresql.base import PGCompiler
    from monk_orm.query_compiler import MonkDBCompiler

    MonkDBCompiler.visit_on_conflict_do_update = PGCompiler.visit_on_conflict_do_update
    MonkDBCompiler._on_conflict_target = PGCompiler._on_conflict_target
    MonkDBDDLCompiler.visit_create_index = ddl_compiler_visit_create_index


patch_sqlalchemy_dialect()