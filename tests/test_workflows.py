"""Tests for GitHub Actions workflow files.

This module validates GitHub Actions workflow files for best practices and configuration.
Tests are organized by functional area to improve maintainability.
"""

import re
from pathlib import Path
from typing import Any, Dict, List

import pytest
import yaml

# Path constants
GITHUB_DIR = Path(__file__).parent.parent / ".github"
WORKFLOWS_DIR = GITHUB_DIR / "workflows"


def load_yaml_file(file_path: Path) -> Dict:
    """Load a YAML file and return its contents."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # Use yaml.load with BaseLoader to avoid converting 'on' to True
            return yaml.load(f, Loader=yaml.BaseLoader) or {}
    except yaml.YAMLError as e:
        pytest.fail(f"{file_path.name} contains invalid YAML: {e}")
    except FileNotFoundError:
        pytest.fail(f"File not found: {file_path}")
    return {}


# Helper function for parameterization
def _get_workflow_params() -> List[Any]:
    """Generate pytest parameters for all workflow files."""
    files = list(WORKFLOWS_DIR.glob("*.yml")) + list(WORKFLOWS_DIR.glob("*.yaml"))
    return [pytest.param(f, id=f.name) for f in files]


# Fixtures with module scope for better performance
# Removed workflow_files fixture


@pytest.fixture(scope="module")
# pylint: disable=redefined-outer-name
def publish_workflow_file() -> Path:
    """Path to the publish.yml workflow file."""
    return WORKFLOWS_DIR / "publish.yml"


@pytest.fixture(scope="module")
# pylint: disable=redefined-outer-name
def publish_workflow(publish_workflow_file: Path) -> Dict:
    """Parsed content of the publish.yml workflow."""
    return load_yaml_file(publish_workflow_file)


@pytest.fixture(scope="module")
# pylint: disable=redefined-outer-name
def release_drafter_file() -> Path:
    """Path to the release-drafter.yml config file."""
    return GITHUB_DIR / "release-drafter.yml"


@pytest.fixture(scope="module")
# pylint: disable=redefined-outer-name
def release_drafter_config(release_drafter_file: Path) -> Dict:
    """Parsed content of the release-drafter.yml config."""
    return load_yaml_file(release_drafter_file)


@pytest.fixture(scope="module")
def common_category_labels() -> List[str]:
    """Common labels for release drafter categories."""
    return ["feature", "bug", "documentation", "dependencies"]


class TestWorkspaceStructure:
    """Tests for the basic GitHub Actions directory and file structure."""

    def test_workflows_dir_exists(self) -> None:
        """Verify .github/workflows directory exists."""
        assert WORKFLOWS_DIR.exists(), ".github/workflows directory missing"
        assert WORKFLOWS_DIR.is_dir(), ".github/workflows is not a directory"

    @pytest.mark.parametrize(
        "file_path,description",
        [
            (WORKFLOWS_DIR / "publish.yml", "CI/CD publishing workflow"),
            (GITHUB_DIR / "release-drafter.yml", "Release notes configuration"),
        ],
    )
    def test_required_files_exist(self, file_path: Path, description: str) -> None:
        """Verify required files exist."""
        assert file_path.exists(), f"{file_path.name} ({description}) missing"


class TestWorkflowSyntax:
    """Tests for workflow file syntax and basic structure."""

    @pytest.mark.parametrize("workflow_file", _get_workflow_params())
    def test_workflow_syntax(self, workflow_file: Path) -> None:
        """Verify workflow files have valid YAML syntax."""
        load_yaml_file(workflow_file)  # Will fail if YAML is invalid

    @pytest.mark.parametrize("workflow_file", _get_workflow_params())
    def test_workflow_required_sections(self, workflow_file: Path) -> None:
        """Verify workflow files have required sections."""
        workflow = load_yaml_file(workflow_file)

        assert "name" in workflow, f"{workflow_file.name} missing name"
        # Check for the string key 'on'
        assert "on" in workflow, f"{workflow_file.name} missing 'on' section"
        assert "jobs" in workflow, f"{workflow_file.name} missing 'jobs' section"
        assert workflow["jobs"], f"{workflow_file.name} has empty 'jobs' section"


class TestJobDependencies:
    """Tests for job dependencies in workflow files."""

    # pylint: disable=too-few-public-methods

    @pytest.mark.parametrize("workflow_file", _get_workflow_params())
    def test_workflow_job_dependencies(self, workflow_file: Path) -> None:
        """Verify job dependencies reference valid jobs."""
        workflow = load_yaml_file(workflow_file)

        if "jobs" not in workflow:
            pytest.skip(f"{workflow_file.name} has no jobs section")

        job_ids = set(workflow["jobs"].keys())

        for job_id, job_config in workflow["jobs"].items():
            if "needs" not in job_config:
                continue

            needs = job_config["needs"]
            if isinstance(needs, str):
                assert needs in job_ids, f"Job '{job_id}' depends on non-existent job '{needs}'"
                continue

            # Handle list of dependencies
            missing_deps = [n for n in needs if n not in job_ids]
            assert all(
                needed_job in job_ids for needed_job in needs
            ), f"Job '{job_id}' depends on non-existent job(s): {missing_deps}"


class TestActionReferences:
    """Tests for GitHub Action references in workflow files."""

    # pylint: disable=too-few-public-methods

    @pytest.mark.parametrize("workflow_file", _get_workflow_params())
    def test_github_action_references(self, workflow_file: Path) -> None:
        """Verify GitHub Action references use proper versioning."""
        workflow_data = load_yaml_file(workflow_file)

        if "jobs" not in workflow_data:
            pytest.skip(f"{workflow_file.name} has no jobs section")

        action_refs = self._get_action_references(workflow_data)
        # Check for unstable references
        for ref in action_refs:
            assert not ref.endswith("@main"), f"Action {ref} uses unstable @main reference"
            assert not ref.endswith("@master"), f"Action {ref} uses unstable @master reference"

            # Check version format
            version = ref.split("@")[-1]
            assert re.match(
                r"^[a-zA-Z0-9_\-\.\/]+$|^[0-9a-f]{7,40}$", version
            ), f"Action {ref} has invalid version format"

    def _get_action_references(self, workflow: Dict) -> List[str]:
        """Extract GitHub Action references from a workflow."""
        action_refs = []

        # Process each job
        for job in workflow["jobs"].values():
            # Skip jobs without steps
            if "steps" not in job:
                continue

            # Process each step in the job
            for step in job.get("steps", []):
                # Skip steps without external actions
                if "uses" not in step:
                    continue
                if step["uses"].startswith("./"):
                    continue

                # Only include steps with version references
                if "@" in step["uses"]:
                    action_refs.append(step["uses"])

        return action_refs


class TestPublishWorkflow:
    """Tests for the publish workflow structure and configuration."""

    # pylint: disable=redefined-outer-name
    def test_publish_workflow_jobs(self, publish_workflow: Dict) -> None:
        """Verify publish workflow has required jobs."""
        publish_workflow_data = publish_workflow  # Rename for clarity if needed, or use directly
        assert "jobs" in publish_workflow_data, "publish.yml missing jobs section"
        assert publish_workflow_data["jobs"], "publish.yml has no jobs defined"

        # Check for essential job types using functional approach
        job_names = list(publish_workflow_data["jobs"].keys())
        has_validation = any("validate" in name.lower() for name in job_names)
        has_publishing = any(
            "publish" in name.lower() or "deploy" in name.lower() for name in job_names
        )

        assert has_validation, "publish workflow missing validation job"
        assert has_publishing, "publish workflow missing publishing job"

    # pylint: disable=redefined-outer-name
    def test_publish_workflow_triggers(self, publish_workflow: Dict) -> None:
        """Verify publish workflow has required triggers."""
        publish_workflow_data = publish_workflow
        # Check for the string key 'on'
        assert "on" in publish_workflow_data, "publish.yml missing triggers"

        triggers = publish_workflow_data["on"]
        assert "release" in triggers, "publish workflow should trigger on releases"
        assert "workflow_dispatch" in triggers, "publish workflow should support manual triggering"

    # pylint: disable=redefined-outer-name
    def test_publish_release_trigger_config(self, publish_workflow: Dict) -> None:
        """Verify release trigger is properly configured."""
        publish_workflow_data = publish_workflow
        # Check for the string key 'on'
        if "on" not in publish_workflow_data or "release" not in publish_workflow_data["on"]:
            pytest.skip("No release trigger in publish workflow")

        release_config = publish_workflow_data["on"]["release"]

        if not isinstance(release_config, dict):
            pytest.skip("Release trigger has no configuration")

        assert "types" in release_config, "Release trigger should specify types"
        assert (
            "published" in release_config["types"]
        ), "Release trigger should include 'published' type"

    # pylint: disable=redefined-outer-name
    def test_publish_job_dependencies(self, publish_workflow: Dict) -> None:
        """Verify publish jobs depend on validation jobs."""
        publish_workflow_data = publish_workflow
        if "jobs" not in publish_workflow_data:
            pytest.skip("No jobs in publish workflow")

        publish_jobs = [
            name for name in publish_workflow_data["jobs"] if "publish" in name.lower()
        ]
        validate_jobs = [
            name for name in publish_workflow_data["jobs"] if "validate" in name.lower()
        ]

        if not publish_jobs or not validate_jobs:
            pytest.skip("Missing publish or validate jobs")

        for pub_job in publish_jobs:
            job_config = publish_workflow_data["jobs"][pub_job]

            assert "needs" in job_config, f"Publish job '{pub_job}' has no dependencies"

            needs = job_config["needs"]
            # Standardize to list for simpler processing
            needs_list = needs if isinstance(needs, list) else [needs]

            # Check if any validation job is included in dependencies
            assert any(
                dep in validate_jobs for dep in needs_list
            ), f"Publish job '{pub_job}' should depend on a validation job"


class TestReleaseDrafter:
    """Tests for the release-drafter.yml configuration."""

    # pylint: disable=redefined-outer-name
    def test_release_drafter_sections(self, release_drafter_config: Dict) -> None:
        """Verify release-drafter.yml has required sections."""
        release_drafter_data = release_drafter_config
        required_sections = ["categories", "template", "name-template", "tag-template"]

        for section in required_sections:
            assert (
                section in release_drafter_data
            ), f"release-drafter.yml missing '{section}' section"

    # pylint: disable=redefined-outer-name
    def test_release_drafter_categories(
        self, release_drafter_config: Dict, common_category_labels: List[str]
    ) -> None:
        """Verify release-drafter.yml includes common category labels."""
        release_drafter_data = release_drafter_config
        category_labels_data = common_category_labels
        if "categories" not in release_drafter_data:
            pytest.skip("No categories in release-drafter.yml")

        assert release_drafter_data[
            "categories"
        ], "release-drafter.yml has empty categories section"

        # Extract all labels with functional approach
        all_labels = [
            label.lower()
            for category in release_drafter_data["categories"]
            for label in category.get("labels", [])
        ]

        assert all_labels, "No labels defined in release-drafter.yml categories"

        # Check each required label has at least one matching entry
        missing_categories = [
            label
            for label in category_labels_data
            if not any(label.lower() in existing for existing in all_labels)
        ]

        assert (
            not missing_categories
        ), f"release-drafter.yml missing categories for: {missing_categories}"
