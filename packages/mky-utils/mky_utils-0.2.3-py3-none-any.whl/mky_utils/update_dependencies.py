import toml


# Load dependencies from requirements.txt
def load_requirements(requirements_file):
    with open(requirements_file, "r") as f:
        requirements = [
            line.strip() for line in f if line.strip() and not line.startswith("#")
        ]
    return requirements


# Update dependencies in pyproject.toml
def update_pyproject(pyproject_file, requirements):
    # Load existing pyproject.toml
    with open(pyproject_file, "r") as f:
        pyproject_data = toml.load(f)

    # Update the dependencies section in [project]
    if "dependencies" in pyproject_data["project"]:
        pyproject_data["project"]["dependencies"] = requirements
    else:
        pyproject_data["project"]["dependencies"] = requirements

    # Write back the updated pyproject.toml
    with open(pyproject_file, "w") as f:
        toml.dump(pyproject_data, f)


if __name__ == "__main__":
    requirements = load_requirements("requirements.txt")
    update_pyproject("pyproject.toml", requirements)
