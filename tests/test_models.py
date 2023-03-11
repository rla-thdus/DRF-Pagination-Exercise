import pytest

from api.models import Tag


@pytest.mark.django_db
def test_insert_data_in_tag():
    tag = Tag.objects.create(name='tag_test')
    assert tag.name == 'tag_test'

