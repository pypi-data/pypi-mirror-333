"""
Tests for bin/modmaker entrypoint
"""

import os
import sys
import ast
import subprocess
import pytest
from pathlib import Path


@pytest.fixture
def bin_modmaker_path():
    """Return the path to the bin/modmaker entrypoint."""
    project_root = Path(__file__).parent.parent
    bin_path = project_root / "modmaker" / "bin" / "modmaker"
    
    if not bin_path.exists():
        pytest.fail(f"Entrypoint script not found at {bin_path}")
    
    return bin_path


def test_entrypoint_permissions(bin_modmaker_path):
    """Test that the entrypoint is executable."""
    assert os.access(bin_modmaker_path, os.X_OK), "Entrypoint script should be executable"


def test_entrypoint_shebang(bin_modmaker_path):
    """Test that the entrypoint has the correct shebang."""
    with open(bin_modmaker_path, 'r') as f:
        first_line = f.readline().strip()
    
    assert first_line == "#!/usr/bin/env python", "Entrypoint should use #!/usr/bin/env python shebang"


def test_entrypoint_structure(bin_modmaker_path):
    """Test the structural elements of the entrypoint script."""
    with open(bin_modmaker_path, 'r') as f:
        content = f.read()
    
    # Parse the script into an AST
    tree = ast.parse(content)
    
    # Check for imports
    imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
    import_names = []
    for node in imports:
        if isinstance(node, ast.Import):
            import_names.extend(name.name for name in node.names)
        else:  # ImportFrom
            import_names.append(node.module)
    
    assert "sys" in import_names, "Script should import sys"
    assert "os" in import_names, "Script should import os"
    
    # Check for try-except blocks
    try_blocks = [node for node in ast.walk(tree) if isinstance(node, ast.Try)]
    assert len(try_blocks) >= 1, "Script should have at least one try-except block"
    
    # Check for string "sys.path.insert" anywhere in the code
    # This is more reliable than AST parsing which might not handle all cases
    assert "sys.path.insert" in content, "Script should modify sys.path"
    
    # Check for sys.exit in the content
    assert "sys.exit" in content, "Script should have sys.exit for error handling"
    
    # Check for if __name__ == "__main__" block using string search
    assert 'if __name__ == "__main__"' in content or "if __name__ == '__main__'" in content, \
           "Script should have if __name__ == '__main__' block"


def test_entrypoint_execution(bin_modmaker_path):
    """Test that the entrypoint can be executed."""
    # Run with --help to avoid actual command execution
    result = subprocess.run(
        [sys.executable, bin_modmaker_path, "--help"],
        capture_output=True,
        text=True,
        check=False
    )
    
    assert result.returncode == 0, f"Entrypoint should exit with code 0 for --help: {result.stderr}"
    assert "usage:" in result.stdout, "Entrypoint should output help text"


def test_entrypoint_version(bin_modmaker_path):
    """Test that the entrypoint supports --version flag."""
    result = subprocess.run(
        [sys.executable, bin_modmaker_path, "--version"],
        capture_output=True,
        text=True,
        check=False
    )
    
    assert result.returncode == 0, f"Entrypoint should exit with code 0 for --version: {result.stderr}"
    assert result.stdout.strip(), "Entrypoint should output version info"


def test_entrypoint_error_handling(bin_modmaker_path):
    """Test that the entrypoint handles errors."""
    # Using an invalid command should trigger error handling
    result = subprocess.run(
        [sys.executable, bin_modmaker_path, "invalid_command"],
        capture_output=True,
        text=True,
        check=False
    )
    
    # Should exit with non-zero code
    assert result.returncode != 0, "Entrypoint should exit with non-zero code for invalid commands"
    assert result.stderr, "Entrypoint should output error message"


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])