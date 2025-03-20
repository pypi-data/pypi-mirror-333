import os
import sys
import pytest
import importlib.util
from pathlib import Path
import logging
import traceback
from unittest.mock import patch

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the root directory of the project
ROOT_DIR = Path(__file__).parent.parent
EXAMPLES_DIR = ROOT_DIR / "examples"

# Test configurations with different datasets and project names
TEST_CONFIGS = [
    {"dataset_name": "test_dataset_1", "project_name": "test_project_1"},
    {"dataset_name": "test_dataset_2", "project_name": "test_project_2"},
]

class ExampleRunner:
    """Class to run examples with different configurations."""
    
    def __init__(self):
        self.examples = self._discover_examples()
    
    def _discover_examples(self):
        """Find all example Python files in the examples directory."""
        examples = []
        for root, _, files in os.walk(EXAMPLES_DIR):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    file_path = Path(root) / file
                    # Determine the framework based on the directory structure
                    framework = self._get_framework(file_path)
                    examples.append({
                        "path": str(file_path),
                        "framework": framework,
                        "name": file_path.stem,
                        "relative_path": str(file_path.relative_to(ROOT_DIR))
                    })
        return examples
    
    def _get_framework(self, file_path):
        """Determine the framework based on the file path."""
        path_str = str(file_path)
        if "langgraph" in path_str:
            return "langgraph"
        # elif "autogen" in path_str:
        #     return "autogen"
        # elif "crewai" in path_str:
        #     return "crewai"
        # elif "langchain" in path_str:
        #     return "langchain"
        # elif "llamaindex_examples" in path_str:
        #     return "llamaindex"
        # elif "smolagents" in path_str:
        #     return "smolagents"
        # elif "haystack" in path_str:
        #     return "haystack"
        # elif "custom_agents" in path_str:
        #     return "custom"
        return "unknown"
    
    def get_env_vars(self, config):
        """Create environment variables for testing."""
        return {
            "DATASET_NAME": config["dataset_name"],
            "PROJECT_NAME": config["project_name"]
        }
    
    def run_example(self, example, config):
        """Run an example with the given configuration."""
        logger.info(f"Running example: {example['name']} ({example['framework']})")
        
        # Add the example's directory to sys.path temporarily
        example_dir = os.path.dirname(example['path'])
        
        # Save original environment
        original_env = os.environ.copy()
        
        # Set environment variables
        env_vars = self.get_env_vars(config)
        for key, value in env_vars.items():
            os.environ[key] = value
        
        try:
            # Execute the Python file directly as a script using subprocess
            try:
                import subprocess
                
                # Get the current Python executable
                python_executable = sys.executable
                
                # Create environment with the necessary variables
                subprocess_env = os.environ.copy()
                
                # Run the example file as a subprocess
                logger.info(f"Executing {example['path']} as a subprocess")
                result = subprocess.run(
                    [python_executable, example['path']],
                    env=subprocess_env,
                    capture_output=True,
                    text=True,
                    check=False,
                    cwd=example_dir  # Set the working directory to the example directory
                )
                
                # Log the output regardless of success or failure
                if result.stdout.strip():
                    logger.info(f"STDOUT from {example['name']}:\n{result.stdout}")
                if result.stderr.strip():
                    logger.warning(f"STDERR from {example['name']}:\n{result.stderr}")
                
                # Check if the execution was successful
                if result.returncode == 0:
                    logger.info(f"Successfully ran example: {example['name']}")
                    return True
                else:
                    logger.error(f"Error running example {example['path']}: Exit code {result.returncode}")
                    return False
            except Exception as e:
                logger.error(f"Error running example {example['path']}: {str(e)}")
                logger.error(traceback.format_exc())
                return False
        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)

# Generate test ids for better reporting
def idfn(val):
    if isinstance(val, dict):
        if 'name' in val:
            return f"{val['name']}_{val['framework']}"
        elif 'dataset_name' in val:
            return f"{val['dataset_name']}_{val['project_name']}"
    return str(val)

# Create the runner
runner = ExampleRunner()

# Parametrize the test with examples and configurations
@pytest.mark.parametrize("example", runner.examples, ids=idfn)
@pytest.mark.parametrize("config", TEST_CONFIGS, ids=idfn)
def test_example_with_config(example, config):
    """Test each example with different configurations."""
    logger.info(f"Testing {example['name']} with dataset={config['dataset_name']}, project={config['project_name']}")
    
    # Run the example and assert it completes without errors
    result = runner.run_example(example, config)
    assert result, f"Example {example['path']} failed with dataset={config['dataset_name']}, project={config['project_name']}"

if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
