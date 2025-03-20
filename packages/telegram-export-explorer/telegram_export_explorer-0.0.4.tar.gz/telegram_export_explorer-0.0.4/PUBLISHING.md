# Publishing checklist

- Update version in CHANGELOG.md
- Update version in pyproject.toml
- Commit changes: git commit -m 'Release v0.0.2'
- Tag release: git tag -a 'v0.0.2' -m 'Release v0.0.2'
- Push to git: git push --follow-tags
- Build packages: rm -rf dist && python -m build
- Publish: twine upload dist/*
