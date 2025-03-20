def test_level1_import():
    try:
        import bibt  # noqa: F401
    except ImportError:
        assert False
    assert True


def test_level2_import():
    try:
        from bibt import gcp  # noqa: F401
    except ImportError:
        assert False
    assert True


def test_level3_import():
    try:
        from bibt.gcp import storage  # noqa: F401
    except ImportError:
        assert False
    assert True


def test_level4_import():
    try:
        from bibt.gcp.storage import Client  # noqa: F401
    except ImportError:
        assert False
    assert True


def test_level4_impor_method():
    try:
        from bibt.gcp.storage import parse_json_nld  # noqa: F401
    except ImportError:
        assert False
    assert True
