pkg_folder := "restfly"
git_status := `git status --porcelain`
lib_version := `grep -Eo '[0-9\.]+' restfly/_version.py`

[parallel]
test-parallel: (test-py "3.11") (test-py "3.12") (test-py "3.13") (test-py "3.14") (test-py "3.15")

test: (test-py "3.11") (test-py "3.12") (test-py "3.13") (test-py "3.14") (test-py "3.15")

docs:
    sphinx-build -M clean docs docs/_build
    sphinx-build -M html docs docs/_build

test-py version: (lint version) (unit-tests version) audit version-check


version-check:
    echo "Ensuring that the project file and version file both agree on $(uv version --short)"
    grep "$(uv version --short)" restfly/_version.py

lint version:
    uv run --python {{version}} --isolated --group test mypy {{pkg_folder}}
    uv run --python {{version}} --isolated --group test ty check --exit-zero-on-warning {{pkg_folder}}
    uv run --python {{version}} --isolated --group test ruff check {{pkg_folder}}

unit-tests version:
    uv run --python {{version}} --isolated --group test pytest -q --cov-fail-under 95

audit:
    uv audit --no-group test --no-group dev

release version:
    {{ assert(git_status == "", "Git Repo not clean.") }}
    echo "Checking to see if {{version}} has already been released..."
    uv run pip index versions restfly --json | jq -e '.versions | any(index("{{version}}")) | not' > /dev/null
    uv version {{version}}
    uv lock -U
    uv sync --all-groups
    sed -i 's/version =.*/version = "{{version}}"/g' restfly/_version.py
    git add pyproject.toml uv.lock restfly/_version.py
    git commit -m "Updated Release Version to v{{version}}"
    git tag v{{version}}
