import os
import tempfile
import shutil
import pytest
from repo_to_one_file.__main__ import create_markdown, generate_directory_structure


@pytest.fixture
def temp_repo():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    # Create some sample files and directories
    os.makedirs(os.path.join(temp_dir, "src"))
    os.makedirs(os.path.join(temp_dir, "tests"))
    os.makedirs(os.path.join(temp_dir, "node_modules"))  # Add this line
    
    with open(os.path.join(temp_dir, "README.md"), "w") as f:
        f.write("# Test Repository\n\nThis is a test repository.")
    
    with open(os.path.join(temp_dir, "src", "main.py"), "w") as f:
        f.write("def main():\n    print('Hello, World!')")
    
    with open(os.path.join(temp_dir, "tests", "test_main.py"), "w") as f:
        f.write("def test_main():\n    assert True")
    
    # Create a file that should be ignored
    with open(os.path.join(temp_dir, "node_modules", "some_module.js"), "w") as f:
        f.write("console.log('This should be ignored');")

    yield temp_dir
    
    # Cleanup the temporary directory
    import shutil
    shutil.rmtree(temp_dir)

def test_generate_directory_structure(temp_repo):
    ignored_patterns = ["node_modules*"]
    structure = generate_directory_structure(temp_repo, ignored_patterns)
    
    assert "README.md" in structure
    assert "src/" in structure
    assert "main.py" in structure
    assert "tests/" in structure
    assert "test_main.py" in structure
    assert "node_modules" not in structure

    # Print the structure for debugging
    print("Generated structure:")
    print(structure)

def test_create_markdown(temp_repo):
    ignored_patterns = ["node_modules*"]
    output_file = os.path.join(temp_repo, "output.md")
    
    create_markdown(temp_repo, output_file, 1000, ignored_patterns)
    
    assert os.path.exists(output_file)
    
    with open(output_file, "r") as f:
        content = f.read()
        
    assert "# Directory Structure" in content
    assert "## README.md" in content
    assert "## src/main.py" in content
    assert "## tests/test_main.py" in content
    assert "node_modules" not in content

def test_max_lines_limit(temp_repo):
    ignored_patterns = ["node_modules*"]
    output_file = os.path.join(temp_repo, "output.md")
    
    # Create a file with more than 5 lines
    with open(os.path.join(temp_repo, "long_file.py"), "w") as f:
        f.write("\n".join([f"print({i})" for i in range(10)]))
    
    create_markdown(temp_repo, output_file, 5, ignored_patterns)
    
    with open(output_file, "r") as f:
        content = f.read()
    
    assert "File exceeds 5 lines. Skipped." in content

if __name__ == "__main__":
    pytest.main()