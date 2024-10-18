# Step 1: Create a virtual environment
python3 -m venv ~/myenv

# Step 2: Activate the virtual environment
source ~/myenv/bin/activate

# Step 3: Create project directory
mkdir ~/markdown_to_drive
cd ~/markdown_to_drive

# Step 4: Add your Python script with shebang
# (Make sure your markdown_to_drive.py is in this directory)

# Step 5: Create the setup.py file
echo 'from setuptools import setup

setup(
    name="md2gd",
    version="0.1",
    py_modules=["markdown_to_drive"],
    install_requires=[
        "google-api-python-client",
        "google-auth",
        "google-auth-oauthlib",
        "markdown2",
    ],
    entry_points={
        "console_scripts": [
            "md2gd=markdown_to_drive:main",
        ],
    },
)' > setup.py

# Step 6: Install your package
pip install -e .
