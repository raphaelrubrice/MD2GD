import argparse
import io
import markdown2
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive(credentials_path):
    """
    Authenticates and creates a Google Drive API service object.

    Parameters:
        credentials_path (str): Path to the Google Drive API credentials JSON file.

    Returns:
        service: Google Drive API service object.
    """
    flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('drive', 'v3', credentials=creds)
    return service

def convert_markdown_to_pdf(markdown_file):
    """
    Converts a Markdown file to a PDF file.

    Parameters:
        markdown_file (str): Path to the Markdown file.

    Returns:
        bytes: PDF content as bytes.
    """
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown2.markdown(markdown_content)

    # Create PDF from HTML using WeasyPrint
    pdf_content = io.BytesIO()
    from weasyprint import HTML
    HTML(string=html_content).write_pdf(pdf_content)
    pdf_content.seek(0)  # Reset the buffer position to the beginning
    return pdf_content

def upload_pdf_to_drive(service, pdf_content, folder_id, file_name="output.pdf"):
    """
    Uploads the PDF file to Google Drive in the specified folder.

    Parameters:
        service: Google Drive API service object.
        pdf_content (bytes): The PDF content to upload.
        folder_id (str): The Google Drive folder ID where the file will be uploaded.
        file_name (str): The name of the file to be uploaded.

    Returns:
        dict: The uploaded file metadata including 'id' and 'webViewLink'.
    """
    file_metadata = {
        'name': file_name,
        'parents': [folder_id],
        'mimeType': 'application/pdf'
    }

    media = MediaIoBaseUpload(pdf_content, mimetype='application/pdf', resumable=True)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink').execute()

    return file

def extract_folder_id(drive_folder_link):
    """
    Extracts the folder ID from the Google Drive folder link.

    Parameters:
        drive_folder_link (str): The Google Drive folder link.

    Returns:
        str: The extracted folder ID.
    """
    return drive_folder_link.split('/')[-1]

def main(markdown_file, drive_folder_link, credentials_path):
    """
    Main function to convert a Markdown file to PDF and upload it to Google Drive.

    Parameters:
        markdown_file (str): Path to the Markdown file.
        drive_folder_link (str): Google Drive folder link where the PDF file will be uploaded.
        credentials_path (str): Path to the Google Drive API credentials JSON file.
    """
    # Authenticate Google Drive API
    service = authenticate_google_drive(credentials_path)

    # Convert the Markdown file to PDF
    pdf_content = convert_markdown_to_pdf(markdown_file)

    # Extract folder ID from the provided Google Drive folder link
    folder_id = extract_folder_id(drive_folder_link)

    # Upload the PDF content to Google Drive
    uploaded_file = upload_pdf_to_drive(service, pdf_content, folder_id)

    # Get file ID and webViewLink
    file_id = uploaded_file['id']
    web_view_link = uploaded_file.get('webViewLink', None)

    print(f"File uploaded successfully. Web View Link: {web_view_link}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF and upload to Google Drive.")
    parser.add_argument('markdown_file', type=str, help="Path to the Markdown file.")
    parser.add_argument('drive_folder_link', type=str, help="Google Drive folder link where the PDF will be uploaded.")
    parser.add_argument('credentials', type=str, help="Path to the Google Drive API credentials JSON file.")

    args = parser.parse_args()
    main(args.markdown_file, args.drive_folder_link, args.credentials)

