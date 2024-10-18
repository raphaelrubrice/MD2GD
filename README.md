# MD2GD
Project to upload the rendered version of a Markdown file (Markdown to PDF Converter) to a specified Google Drive Folder.

#### Overview
A brief description of the project, explaining its purpose: to convert Markdown files into beautifully formatted PDF documents and upload them to Google Drive.

#### Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

### Prerequisites
List any software or libraries required before using the project:
- Python 3.x
- Required Python libraries:
  - `markdown2`
  - `weasyprint`
  - `google-auth`
  - `google-auth-oauthlib`
  - `google-api-python-client`

### Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/raphaelrubrice/MD2GD.git
   cd MD2GD
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Libraries**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
1. **Google Drive API Credentials**
   - Go to the [Google Developers Console](https://console.developers.google.com/).
   - Create a new project.
   - Enable the Google Drive API for that project.
   - Create OAuth 2.0 credentials and download the `credentials.json` file.
   - Place `credentials.json` in the project directory.

### Usage
1. **Run the Script**
   ```bash
   python markdown_to_drive.py <path/to/your_markdown_file.md> <https://drive.google.com/drive/folders/your_folder_id> <path_to_credentials_file> <output_file_name>
   ```
   - Replace `<path/to/your_markdown_file.md>` with the path to your Markdown file.
   - Replace `<https://drive.google.com/drive/folders/your_folder_id>` with the link to the Google Drive folder where you want to upload the PDF.
   - Replace `<path_to_credentials_file>` with the actual path to your credentials.json file
   - Replace `<output_file_name>` with the desired output name

2. **Authentication**
   - The first time you run the script, it will prompt you to authenticate with your Google account. Follow the on-screen instructions to grant access.

### Troubleshooting
- **Common Issues**:
  - If you encounter a `FileNotFoundError` for `credentials.json`, make sure the file is in the project directory.
  - If you see a Google API error, ensure the Drive API is enabled for your project in the Google Developers Console.

## Contributing
Feel free to submit issues and pull requests!

## License
MIT License
