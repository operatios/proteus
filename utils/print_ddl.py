from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateIndex, CreateTable

from app.models import Base

dialect = postgresql.dialect()


def print_stmt(stmt) -> None:
    print(
        stmt.compile(
            dialect=dialect,
            compile_kwargs={"literal_binds": True},
        )
    )


def main() -> None:
    for table in Base.metadata.sorted_tables:
        print(CreateTable(table).compile(dialect=dialect))
        for idx in table.indexes:
            print(CreateIndex(idx).compile(dialect=dialect))


if __name__ == "__main__":
    main()
