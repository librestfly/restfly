pkg_folder := "restfly"
git_status := `git status --porcelain`
lib_version := `grep -Eo '[0-9\.]+' restfly/_version.py`
proj_version := `uv version --short`

[parallel]
test-parallel: (test-py "3.11") (test-py "3.12") (test-py "3.13") (test-py "3.14") (test-py "3.15")

test: (test-py "3.11") (test-py "3.12") (test-py "3.13") (test-py "3.14") (test-py "3.15")

docs:
    sphinx-build -M clean docs docs/_build
    sphinx-build -M html docs docs/_build

test-py version: (lint version) (unit-tests version) audit version-check


version-check:
    {{ assert(lib_version == proj_version, "Project file and version file mismatch") }}

git_clean:
    {{ assert(git_status == "", "Git Repo not clean.") }}

lint version:
    @echo "🧪 ==> Running the library through type checkers and linters."
    uv run --python {{version}} --isolated --group test mypy {{pkg_folder}}
    uv run --python {{version}} --isolated --group test ty check --exit-zero-on-warning {{pkg_folder}}
    uv run --python {{version}} --isolated --group test ruff check {{pkg_folder}}

unit-tests version:
    @echo "📝 ==> Unit Testing {{version}}"
    uv run --python {{version}} --isolated --group test pytest -q --cov-fail-under 95

audit:
    @echo "🚧 ==> Running security audits..."
    uv audit --no-group test --no-group dev

release version: test audit git_clean
    @echo "🏭 ==> Checking to see if {{version}} has already been released..."
    uv run pip index versions restfly --json | jq -e '.versions | any(index("{{version}}")) | not' > /dev/null
    
    @echo "🔒 ==> Updating the lockfiles..."
    uv lock -U
    uv sync --all-groups
    
    @echo "🚀 ==> Updating version to {{version}}"
    uv version {{version}}
    sed -i 's/version =.*/version = "{{version}}"/g' restfly/_version.py
    git add pyproject.toml uv.lock restfly/_version.py
    
    @echo "👀 ==> Checking that the updated version is consistent..."
    just version-check
    
    @echo "🏭 ==> Commiting the release version && tagging it for deployment to pypi."
    git commit -m "Updated Release Version to v{{version}}"
    git tag v{{version}}
    git push --tags
    @echo "🤩 👍 ==> Released!"
