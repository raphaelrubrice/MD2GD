import argparse
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import markdown
import re
import io
from googleapiclient.http import MediaIoBaseUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive(credentials_path):
    """
    Authenticates the user and returns a Google Drive API service.
    
    Parameters:
        credentials_path (str): Path to the Google Drive API credentials JSON file.
    
    Returns:
        Google Drive API service object.
    """
    creds = None
    token_path = 'token.json'
    
    # Load saved credentials from token.json, if they exist
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # If there are no valid credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Use the custom or default credentials file to log in
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return build('drive', 'v3', credentials=creds)

def convert_markdown_to_html(markdown_file):
    """
    Converts a markdown file to HTML.
    
    Parameters:
        markdown_file (str): Path to the markdown file.
    
    Returns:
        str: The HTML content.
    """
    with open(markdown_file, 'r', encoding='utf-8') as f:
        text = f.read()
    html = markdown.markdown(text)
    return html

def extract_folder_id(drive_folder_link):
    """
    Extracts the folder ID from a Google Drive folder link.
    
    Parameters:
        drive_folder_link (str): Google Drive folder link.
    
    Returns:
        str: The folder ID.
    """
    match = re.search(r'folders/([a-zA-Z0-9-_]+)', drive_folder_link)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid Google Drive folder link. Folder ID could not be extracted.")

def upload_html_to_drive(service, html_content, folder_id, file_name="output.html"):
    """
    Uploads the HTML file to Google Drive in the specified folder.
    
    Parameters:
        service: Google Drive API service object.
        html_content (str): The HTML content to upload.
        folder_id (str): The Google Drive folder ID where the file will be uploaded.
        file_name (str): The name of the file to be uploaded.
    
    Returns:
        dict: The uploaded file metadata.
    """
    file_metadata = {
        'name': file_name,
        'parents': [folder_id],
        'mimeType': 'text/html'
    }

    html_bytes = io.BytesIO(html_content.encode('utf-8'))
    media = MediaIoBaseUpload(html_bytes, mimetype='text/html', resumable=True)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id').execute()

    return file

def main(markdown_file, drive_folder_link, credentials_path):
    """
    Main function to convert a markdown file to HTML and upload it to Google Drive.
    
    Parameters:
        markdown_file (str): Path to the markdown file.
        drive_folder_link (str): Google Drive folder link where the HTML file will be uploaded.
        credentials_path (str): Path to the Google Drive API credentials JSON file.
    """
    # Authenticate Google Drive API
    service = authenticate_google_drive(credentials_path)

    # Convert the markdown file to HTML
    html_content = convert_markdown_to_html(markdown_file)

    # Extract folder ID from the provided Google Drive folder link
    folder_id = extract_folder_id(drive_folder_link)

    # Upload the HTML content to Google Drive
    uploaded_file = upload_html_to_drive(service, html_content, folder_id)

    print(f"File uploaded successfully. File ID: {uploaded_file['id']}")

if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Convert a markdown file to HTML and upload it to Google Drive.')
    
    # Add arguments for the markdown file path, Google Drive folder link, and credentials path
    parser.add_argument('markdown_file', help='The path to the markdown file.')
    parser.add_argument('drive_folder_link', help='The Google Drive folder link where the HTML file will be uploaded.')
    parser.add_argument('credentials', help='The path to the Google Drive API credentials JSON file.')

    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    main(args.markdown_file, args.drive_folder_link, args.credentials)

