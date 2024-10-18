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

# Step 7: Correct installed script
cd ~/mg2gd/bin/
echo 'import argparse
from markdown_to_drive import main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF and upload to Google Drive.")
    parser.add_argument('markdown_file', type=str, help="Path to the Markdown file.")
    parser.add_argument('drive_folder_link', type=str, help="Google Drive folder link where the PDF will be uploaded.")
    parser.add_argument('credentials', type=str, help="Path to the Google Drive API credentials JSON file.")
    parser.add_argument('output_name', type=str, help='The name of the outputed file.')
    args = parser.parse_args()
    main(args.markdown_file, args.drive_folder_link, args.credentials, args.output_name)
    ' > md2gd

