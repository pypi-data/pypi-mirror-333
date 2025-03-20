import os
import uuid

import pandas as pd
import polars as pl
import pytest
import sqlalchemy as sa
from sqlalchemy import text

# Import the function to be tested. Adjust the import to match your module/package name.
from dataframe_to_pg.writer import write_dataframe_to_postgres


# A pytest fixture to create a SQLAlchemy engine connected to a test database.
# Set the environment variable TEST_DATABASE_URL (e.g. "postgresql+psycopg2://user:pass@localhost/test_db")
# or adjust the default connection string below.
@pytest.fixture(scope="module")
def engine() -> sa.engine.Engine:
    database_url = os.environ.get("TEST_DATABASE_URL", "postgresql+psycopg2://user:password@localhost/test_db")
    engine = sa.create_engine(database_url)
    yield engine
    engine.dispose()


# Helper to drop a table if it exists.
def drop_table(engine: sa.engine.Engine, table_name: str) -> None:
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS :table_name").bindparams(table_name=table_name))
        conn.commit()


def generate_table_name(prefix: str = "test_table") -> str:
    # Generate a unique table name using uuid.
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def test_write_pandas_insert(engine: sa.engine.Engine) -> None:
    # Create a simple pandas DataFrame.
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    df.index.name = "id"
    table_name = generate_table_name("pandas_insert")
    drop_table(engine, table_name)

    # Write using the default (upsert) write_method.
    write_dataframe_to_postgres(df, engine, table_name)

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM :table_name").bindparams(table_name=table_name)).fetchall()
        # There should be 3 rows.
        assert len(result) == 3
        # Check that the 'b' column values match.
        values = sorted(row[1] for row in result)  # assuming first column is "id"
        assert values == sorted(["x", "y", "z"])


def test_write_pandas_chunksize(engine: sa.engine.Engine) -> None:
    # Create a larger pandas DataFrame.
    df = pd.DataFrame({"a": range(100), "b": [f"val{i}" for i in range(100)]})
    df.index.name = "id"
    table_name = generate_table_name("pandas_chunksize")
    drop_table(engine, table_name)

    # Write using a chunksize.
    write_dataframe_to_postgres(df, engine, table_name, chunksize=10)

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM :table_name").bindparams(table_name=table_name)).fetchall()
        assert len(result) == 100


def test_write_pandas_replace(engine: sa.engine.Engine) -> None:
    # Create an initial pandas DataFrame.
    df_initial = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    df_initial.index.name = "id"
    table_name = generate_table_name("pandas_replace")
    drop_table(engine, table_name)

    # First insert.
    write_dataframe_to_postgres(df_initial, engine, table_name, write_method="insert")

    # Create an updated DataFrame (with same primary keys) but new values.
    df_updated = pd.DataFrame({"a": [1, 2], "b": ["updated_x", "updated_y"]})
    df_updated.index.name = "id"
    write_dataframe_to_postgres(df_updated, engine, table_name, write_method="replace")

    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM :table_name ORDER BY id").bindparams(table_name=table_name)).fetchall()
        # Check that values have been updated.
        # Here we assume the table has two columns: the primary key (id) and column b.
        # Adjust the tuple indices as needed.
        assert rows[0][1] == "updated_x"
        assert rows[1][1] == "updated_y"


def test_write_polars_insert(engine: sa.engine.Engine) -> None:
    # Create a simple Polars DataFrame.
    df = pl.DataFrame({"a": [10, 20, 30], "b": ["p", "q", "r"]})
    # For Polars, the index parameter is required.
    table_name = generate_table_name("polars_insert")
    drop_table(engine, table_name)

    write_dataframe_to_postgres(df, engine, table_name, index="a", write_method="insert")

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM :table_name").bindparams(table_name=table_name)).fetchall()
        assert len(result) == 3
        # Verify that the primary key column "a" has the correct values.
        pk_values = sorted(row[0] for row in result)
        assert pk_values == sorted([10, 20, 30])


def test_write_polars_chunksize(engine: sa.engine.Engine) -> None:
    # Create a Polars DataFrame with more rows.
    df = pl.DataFrame({"a": list(range(50)), "b": [f"str{i}" for i in range(50)]})
    table_name = generate_table_name("polars_chunksize")
    drop_table(engine, table_name)

    write_dataframe_to_postgres(df, engine, table_name, index="a", chunksize="auto")

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM :table_name").bindparams(table_name=table_name)).fetchall()
        assert len(result) == 50
