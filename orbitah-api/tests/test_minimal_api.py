from api.main import api


def test_app_exists():
    assert api is not None
