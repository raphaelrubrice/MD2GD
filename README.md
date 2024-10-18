# MD2GD (Markdown 2 Google Drive)
Project to upload the rendered version of a Markdown file (Markdown to PDF Converter) to a specified Google Drive Folder.

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
  - `google-api-python-client`
  - `google-auth-httplib2`
  - `google-auth-oauthlib`
  - `markdown`
  - `markdown2`
  - `weasyprint`

### Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/raphaelrubrice/MD2GD.git
   cd MD2GD
   ```
   OR
    ```bash
   git clone git@github.com:raphaelrubrice/MD2GD.git
   cd MD2GD
   ```
    
3. **Set Up a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv ~/md2gd
   source ~/md2gd/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Run setup.sh**
   ```bash
   bash setup.sh
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
   source ~/md2gd/bin/activate
   md2gd <path/to/your_markdown_file.md> <https://drive.google.com/drive/folders/your_folder_id> <path_to_credentials_file> <output_file_name>
   deactivate
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
