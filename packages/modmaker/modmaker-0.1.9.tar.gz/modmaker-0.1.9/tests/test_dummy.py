"""
Basic test to ensure testing infrastructure works.
"""


def test_modmaker_exists():
    """Verify the modmaker module exists."""
    import modmaker
    assert modmaker is not None