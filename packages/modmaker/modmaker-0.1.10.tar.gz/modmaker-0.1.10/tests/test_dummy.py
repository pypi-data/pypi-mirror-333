"""
Basic test to ensure testing infrastructure works.
"""


def test_modmaker_exists():
    """Verify the modmaker module exists."""
    import sys
    from pathlib import Path
    
    # Ensure modmaker is in the path
    project_root = str(Path(__file__).parent.parent)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        
    import modmaker
    assert modmaker is not None