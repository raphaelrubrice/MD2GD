# Step 1: Create a virtual environment
current_dir=$PWD
python3 -m venv ~/md2gd

# Step 2: Activate the virtual environment
source ~/md2gd/bin/activate

# Step 3: Create project directory
mkdir ~/markdown_to_drive
cd ~/markdown_to_drive

# Step 4: Add your Python script with shebang
cp ${current_dir}/markdown_to_drive.py markdown_to_drive.py

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
	"markdown",
	"weasyprint"
    ],
    entry_points={
        "console_scripts": [
            "md2gd=markdown_to_drive:main",
        ],
    },
)' > setup.py

# Step 6: Install your package
pip install -e .
