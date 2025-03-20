import pytest

from pydantic_core._pydantic_core import ValidationError


pytestmark = [
    pytest.mark.usefixtures("backup_database_schema"),
]


def test_iter(schemas, temp_schema, temp_schema_case_sensitive):
    schema_names = [s.name for s in schemas.iter()]
    assert temp_schema.name.upper() in schema_names

    # TODO(SNOW-1354988) - Please uncomment this once you have this bug resolved
    # assert any(
    #     map(
    #         lambda e: e in schema_names,
    #         (
    #             temp_schema_case_sensitive.name,  # for mixed case names
    #         ),
    #     )
    # )


@pytest.mark.flaky
def test_iter_like(schemas, temp_schema, temp_schema_case_sensitive):
    schema_names = [s.name for s in schemas.iter(like="test_schema%")]
    assert temp_schema.name.upper() in schema_names

    # TODO(SNOW-1354988) - Please uncomment this once you have this bug resolved
    # assert any(
    #     map(
    #         lambda e: e in schema_names,
    #         (
    #             temp_schema_case_sensitive.name,  # for mixed case names
    #         ),
    #     )
    # )


def test_iter_starts_with(schemas, temp_schema, temp_schema_case_sensitive):
    schema_names = [s.name for s in schemas.iter(starts_with="Test_schema")]
    assert temp_schema.name.upper() not in schema_names
    assert temp_schema_case_sensitive.name not in schema_names

    schema_names = [s.name for s in schemas.iter(starts_with="TEST_SCHEMA")]
    assert temp_schema.name.upper() in schema_names
    assert temp_schema_case_sensitive.name not in schema_names


# The limit keyword is required for the from keyword to function, limit=10 was chosen arbitrarily
# as it does not affect the test
def test_iter_from_name(schemas, temp_schema, temp_schema_case_sensitive):
    schema_names = [s.name for s in schemas.iter(limit=10, from_name="test_schema")]
    assert temp_schema.name.upper() not in schema_names


#     # TODO(SNOW-1354988) - Please uncomment this once you have this bug resolved
#     # assert any(
#     #     map(
#     #         lambda e: e in schema_names,
#     #         (
#     #             temp_schema_case_sensitive.name,  # for mixed case names
#     #         ),
#     #     )
#     # )


def test_iter_limit(schemas):
    data = list(schemas.iter(limit=10))
    assert len(data) <= 10

    with pytest.raises(
        ValidationError,
    ):
        list(schemas.iter(limit=10001))
