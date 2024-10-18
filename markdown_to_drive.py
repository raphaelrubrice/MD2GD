import os
import markdown
import mimetypes
import argparse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Scopes required by the Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive():
    """Authenticates the user and returns a Google Drive API service."""
    creds = None
    # Token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def convert_markdown_to_html(md_file_path):
    """Converts a markdown file to an HTML file and returns the HTML file path."""
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        text = md_file.read()
    html_content = markdown.markdown(text)
    html_file_path = os.path.splitext(md_file_path)[0] + ".html"
    with open(html_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)
    return html_file_path

def upload_to_google_drive(service, folder_id, file_path):
    """Uploads a file to the specified Google Drive folder."""
    file_name = os.path.basename(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)

    # Define file metadata
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    media = MediaFileUpload(file_path, mimetype=mime_type)

    # Upload the file
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    
    print(f'File {file_name} uploaded to Drive with ID: {file.get("id")}')

def get_folder_id_from_link(drive_link):
    """Extracts the folder ID from the Google Drive link."""
    if "folders" in drive_link:
        folder_id = drive_link.split("folders/")[1].split("?")[0]
        return folder_id
    else:
        raise ValueError("Invalid Google Drive folder link.")

def main(md_file_path, google_drive_folder_link):
    """Main function to convert markdown and upload the HTML to Google Drive."""
    # Authenticate Google Drive API
    service = authenticate_google_drive()

    # Convert the markdown file to HTML
    html_file_path = convert_markdown_to_html(md_file_path)

    # Get the Google Drive folder ID from the link
    folder_id = get_folder_id_from_link(google_drive_folder_link)

    # Upload the HTML file to the specified Google Drive folder
    upload_to_google_drive(service, folder_id, html_file_path)

if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Convert a markdown file to HTML and upload it to Google Drive.')
    
    # Add arguments for the markdown file path and Google Drive folder link
    parser.add_argument('markdown_file', help='The path to the markdown file.')
    parser.add_argument('drive_folder_link', help='The Google Drive folder link where the HTML file will be uploaded.')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Call the main function with the parsed arguments
    main(args.markdown_file, args.drive_folder_link) 
