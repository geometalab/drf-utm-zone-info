from contextlib import closing

import pytest
import sqlalchemy
from sqlalchemy.sql.schema import Table as DbTable

from osmaxx.utils.frozendict import frozendict
from tests.conftest import TagCombination
from tests.inside_worker_test.conftest import slow
from tests.inside_worker_test.declarative_schema import osm_models

MAJOR_KEYS = frozenset({'highway', 'railway'})

CORRESPONDING_OSMAXX_WAY_TYPES_FOR_OSM_TAG_COMBINATIONS = frozendict(
    {
        TagCombination(highway='track'): 'track',
        TagCombination(highway='track', tracktype='grade3'): 'grade3',
        TagCombination(highway='footway'): 'footway',
    },
)

CORRESPONDING_OSMAXX_STATUSES_FOR_OSM_STATUSES = frozendict(
    planned='P',
    disused='D',
    construction='C',
    abandoned='A',
)


@slow
def test_osm_object_without_status_does_not_end_up_in_nonop(non_lifecycle_data_import, nonop_l):
    engine = non_lifecycle_data_import
    with closing(engine.execute(sqlalchemy.select('*').select_from(nonop_l))) as result:
        assert result.rowcount == 0


@slow
def test_osm_object_with_status_ends_up_in_nonop_with_correct_attribute_values(
        lifecycle_data_import, nonop_l, expected_osmaxx_status, osm_status, non_lifecycle_osm_tags, major_tag_key, expected_nonop_subtype):
    engine = lifecycle_data_import
    with closing(engine.execute(sqlalchemy.select('*').select_from(nonop_l))) as result:
        assert result.rowcount == 1
        row = result.fetchone()
        assert row['status'] == expected_osmaxx_status
        assert row['tags'] == '"{key}"=>"{value}"'.format(key=osm_status, value=non_lifecycle_osm_tags[major_tag_key])
        assert row['sub_type'] == expected_nonop_subtype


@pytest.fixture
def nonop_l():
    return DbTable('nonop_l', osm_models.metadata, schema='view_osmaxx')


@pytest.yield_fixture
def lifecycle_data_import(lifecycle_data, data_import):
    with data_import(lifecycle_data) as engine:
        yield engine


@pytest.yield_fixture
def non_lifecycle_data_import(non_lifecycle_data, data_import):
    with data_import(non_lifecycle_data) as engine:
        yield engine


@pytest.fixture
def lifecycle_data(non_lifecycle_osm_tags, osm_status, major_tag_key):
    osm_tags = dict(non_lifecycle_osm_tags)
    major_tag_value = osm_tags.pop(major_tag_key)
    osm_tags.update({major_tag_key: osm_status, 'tags': {osm_status: major_tag_value}})
    assert len(osm_tags) == len(non_lifecycle_osm_tags) + 1
    return {osm_models.t_osm_line: osm_tags}


@pytest.fixture
def major_tag_key(non_lifecycle_osm_tags):
    major_keys = MAJOR_KEYS.intersection(non_lifecycle_osm_tags)
    assert len(major_keys) == 1
    return next(iter(major_keys))


@pytest.fixture
def non_lifecycle_data(non_lifecycle_osm_tags):
    return {osm_models.t_osm_line: non_lifecycle_osm_tags}


@pytest.fixture
def non_lifecycle_osm_tags(non_lifecycle_osm_tags_and_expected_nonop_subtype):
    osm_tags, _ = non_lifecycle_osm_tags_and_expected_nonop_subtype
    return osm_tags


@pytest.fixture
def expected_nonop_subtype(non_lifecycle_osm_tags_and_expected_nonop_subtype):
    _, subtype = non_lifecycle_osm_tags_and_expected_nonop_subtype
    return subtype


@pytest.fixture
def osm_status(osm_status_and_expected_osmaxx_status):
    status, _ = osm_status_and_expected_osmaxx_status
    return status


@pytest.fixture
def expected_osmaxx_status(osm_status_and_expected_osmaxx_status):
    _, osmaxx_status = osm_status_and_expected_osmaxx_status
    return osmaxx_status


@pytest.fixture(
    params=CORRESPONDING_OSMAXX_WAY_TYPES_FOR_OSM_TAG_COMBINATIONS.items(),
    ids=[str(tag_combination) for tag_combination in CORRESPONDING_OSMAXX_WAY_TYPES_FOR_OSM_TAG_COMBINATIONS.keys()],
)
def non_lifecycle_osm_tags_and_expected_nonop_subtype(request):
    return request.param


@pytest.fixture(
    params=CORRESPONDING_OSMAXX_STATUSES_FOR_OSM_STATUSES.items(),
    ids=list(CORRESPONDING_OSMAXX_STATUSES_FOR_OSM_STATUSES.keys()),
)
def osm_status_and_expected_osmaxx_status(request):
    return request.param
