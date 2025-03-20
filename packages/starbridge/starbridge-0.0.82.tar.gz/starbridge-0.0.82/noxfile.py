"""Nox configuration for test automation and development tasks."""

import json
import os
from pathlib import Path

import nox

nox.options.reuse_existing_virtualenvs = True
nox.options.default_venv_backend = "uv"

NOT_SKIP_WITH_ACT = "not skip_with_act"
JUNIT_XML = "--junitxml=junit.xml"


def _setup_venv(session: nox.Session, all_extras: bool = True) -> None:
    """Install dependencies for the given session using uv."""
    args = ["uv", "sync", "--frozen"]
    if all_extras:
        args.append("--all-extras")
    session.run_install(
        *args,
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
            "UV_PYTHON": str(session.python),
        },
    )


def _is_act_environment() -> bool:
    """Check if running in GitHub ACT environment.

    Returns:
        bool: True if running in ACT environment, False otherwise.
    """
    return os.environ.get("GITHUB_WORKFLOW_RUNTIME") == "ACT"


@nox.session(python=["3.13"])
def lint(session: nox.Session) -> None:
    """Run code formatting checks, linting, and static type checking."""
    _setup_venv(session)
    session.run("ruff", "check", ".")
    session.run(
        "ruff",
        "format",
        "--check",
        ".",
    )
    # session.run("mypy", "src")  # noqa: ERA001


@nox.session(python=["3.13"])
def docs(session: nox.Session) -> None:
    """Build documentation and concatenate README."""
    _setup_venv(session)
    # Concatenate README files
    header = Path("_readme_header.md").read_text(encoding="utf-8")
    main = Path("_readme_main.md").read_text(encoding="utf-8")
    footer = Path("_readme_footer.md").read_text(encoding="utf-8")
    readme_content = f"{header}\n\n{main}\n\n{footer}"
    Path("README.md").write_text(readme_content, encoding="utf-8")
    # Build docs
    session.run("make", "-C", "docs", "clean", external=True)
    session.run("make", "-C", "docs", "html", external=True)


@nox.session(python=["3.13"])
def audit(session: nox.Session) -> None:
    """Run security audit and license checks."""
    _setup_venv(session)
    session.run("pip-audit", "-f", "json", "-o", "vulnerabilities.json")
    session.run("jq", ".", "vulnerabilities.json", external=True)
    session.run("pip-licenses", "--format=json", "--output-file=licenses.json")
    session.run("jq", ".", "licenses.json", external=True)
    # Read and parse licenses.json
    licenses_data = json.loads(Path("licenses.json").read_text(encoding="utf-8"))

    licenses_inverted: dict[str, list[dict[str, str]]] = {}
    licenses_inverted = {}
    for pkg in licenses_data:
        license_name = pkg["License"]
        package_info = {"Name": pkg["Name"], "Version": pkg["Version"]}

        if license_name not in licenses_inverted:
            licenses_inverted[license_name] = []
        licenses_inverted[license_name].append(package_info)

    # Write inverted data
    Path("licenses-inverted.json").write_text(
        json.dumps(licenses_inverted, indent=2),
        encoding="utf-8",
    )
    session.run("jq", ".", "licenses-inverted.json", external=True)
    session.run("cyclonedx-py", "environment", "-o", "sbom.json")
    session.run("jq", ".", "sbom.json", external=True)


@nox.session(python=["3.11", "3.12", "3.13"])
def test(session: nox.Session) -> None:
    """Run tests with pytest."""
    _setup_venv(session)
    session.run("rm", "-rf", ".coverage", external=True)

    # Build pytest arguments with skip_with_act filter if needed
    pytest_args = ["pytest", "--disable-warnings", JUNIT_XML, "-n", "auto", "--dist", "loadgroup"]
    if _is_act_environment():
        pytest_args.extend(["-k", NOT_SKIP_WITH_ACT])
    pytest_args.extend(["-m", "not sequential"])

    session.run(*pytest_args)

    # Sequential tests
    sequential_args = [
        "pytest",
        "--cov-append",
        "--disable-warnings",
        JUNIT_XML,
        "-n",
        "auto",
        "--dist",
        "loadgroup",
    ]
    if _is_act_environment():
        sequential_args.extend(["-k", NOT_SKIP_WITH_ACT])
    sequential_args.extend(["-m", "sequential"])

    session.run(*sequential_args)

    session.run(
        "bash",
        "-c",
        (
            "docker compose ls --format json | jq -r '.[].Name' | "
            "grep ^pytest | xargs -I {} docker compose -p {} down --remove-orphans"
        ),
        external=True,
    )


@nox.session(python=["3.11", "3.12", "3.13"])
def test_no_extras(session: nox.Session) -> None:
    """Run test sessions without extra dependencies."""
    _setup_venv(session, all_extras=False)

    no_extras_args = ["pytest", "--cov-append", "--disable-warnings", JUNIT_XML, "-n", "1"]
    if _is_act_environment():
        no_extras_args.extend(["-k", NOT_SKIP_WITH_ACT])
    no_extras_args.extend(["-m", "no_extras"])

    session.run(*no_extras_args)

    session.run(
        "bash",
        "-c",
        (
            "docker compose ls --format json | jq -r '.[].Name' | "
            "grep ^pytest | xargs -I {} docker compose -p {} down --remove-orphans"
        ),
        external=True,
    )


@nox.session(python=["3.13"], default=False)
def setup_dev(session: nox.Session) -> None:
    """Setup dev environment post project creation."""
    _setup_venv(session)
    session.run("ruff", "format", ".", external=True)
    git_dir = Path(".git")
    if git_dir.is_dir():
        session.run("echo", "found .git directory", external=True)
        session.run("touch", ".act-env-secret", external=True)
        session.run("pre-commit", "install", external=True)
        with Path(".secrets.baseline").open("w", encoding="utf-8") as out:
            session.run("detect-secrets", "scan", stdout=out, external=True)
        session.run("git", "add", ".", external=True)
        try:
            session.run("pre-commit", external=True)
        except Exception:  # noqa: BLE001
            session.log("pre-commit run failed, continuing anyway")
        session.run("git", "add", ".", external=True)
