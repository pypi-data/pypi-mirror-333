# Local Development
1. Clone the repo
2. Run `pre-commit install` to install pre-commit hooks and required tools
3. Run `pip install -r requirements.txt` to install required Python packages
4. Run `python src/main.py init` to initialize the project structure
5. Run `python src/main.py apply` to generate contexts

# BigQuery Schema Analysis

This project analyzes BigQuery schemas and organizes them into modules for easier analysis.


### Step 4: Build and Distribute (Optional)
To test locally:
1. Install build tools: `pip install build twine`.
2. Build the package: `python -m build`.
3. Install locally: `pip install dist/tabletalk-0.1.0-py3-none-any.whl`.

To distribute on PyPI:
1. Build: `python -m build`.
2. Upload: `twine upload dist/*` (after registering on PyPI).

### Result
With this `setup.py`, users can:
- Install your package with `pip install tabletalk`.
- Run it as `tabletalk run` or `tabletalk test` from the command line, just like dbt.

This setup mirrors dbt’s approach, adapted to your simpler application and specific requirements, ensuring a seamless user experience without compilation. Adjust the `author`, `author_email`, `url`, and `version` as needed for your project.