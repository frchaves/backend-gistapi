import os
from subprocess import run

# create a new Poetry project
run(["poetry", "new", "myproject"])

# get the path to the newly created project
project_path = os.path.abspath("myproject")

# move the requirements.txt file to the project root
os.replace("requirements.txt", os.path.join(project_path, "requirements.txt"))

# read the contents of the requirements.txt file
with open(os.path.join(project_path, "requirements.txt")) as f:
    packages = f.read().splitlines()


# add each package to the project
for package in packages:
    run(["poetry", "add", package], cwd=project_path)

# install the packages and generate the pyproject.toml file
run(["poetry", "install"])

# remove the requirements.txt file
os.remove(os.path.join(project_path, "requirements.txt"))
