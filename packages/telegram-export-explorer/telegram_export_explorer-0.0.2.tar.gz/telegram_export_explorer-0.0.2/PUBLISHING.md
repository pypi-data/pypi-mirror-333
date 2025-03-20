# Publishing checklist

- Update version in changelog
- Update version in pyproject.toml
- Commit changes
- Tag release
- Build packages: python -m build
- Publish: twine upload --sign --identity 'whispered-good@pm.me'
