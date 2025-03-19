import smtplib
from email.message import EmailMessage
import logging
import mimetypes
from pathlib import Path

class EmailSender:
    def __init__(self, credentials):
        self.smtp_server = credentials["smtp_server"]
        self.smtp_port = credentials["smtp_port"]
        self.sender_email = credentials["sender_email"]
        self.sender_password = credentials["sender_password"]
        self.default_from_email = credentials.get("from_email", self.sender_email)
        self.default_reply_to = credentials.get("reply_to", self.default_from_email)

    def log_error(self, error, function_name):
        """Log errors to file"""
        logging.error(f"Error in {function_name.__name__}: {str(error)}")

    def _add_attachment(self, msg, file_path):
        """Helper method to add attachments"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"Attachment not found: {file_path}")
            
            # Guess the content type based on the file extension
            content_type, encoding = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/octet-stream'
            
            main_type, sub_type = content_type.split('/', 1)
            
            with open(file_path, 'rb') as f:
                msg.add_attachment(
                    f.read(),
                    maintype=main_type,
                    subtype=sub_type,
                    filename=file_path.name
                )
            return True
        except Exception as e:
            self.log_error(e, self._add_attachment)
            return False

    def send_email(self, to_email, from_name, subject, plain_content, html_template_path=None, 
                placeholders=None, from_email=None, reply_to=None, attachments=None):
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                if server.noop()[0] != 250:
                    return False, 'Server not responding, please try again later'

                msg = EmailMessage()
                # Use override values if provided, otherwise use defaults
                actual_from_email = from_email or self.default_from_email
                actual_reply_to = reply_to or self.default_reply_to

                msg['From'] = f"{from_name} <{actual_from_email}>"
                msg['To'] = to_email
                msg['Reply-To'] = actual_reply_to
                msg['Subject'] = subject
                msg.set_content(plain_content)

                if html_template_path:
                    try:
                        with open(html_template_path, 'r') as file:
                            html_content = file.read()

                        if placeholders:
                            for key, value in placeholders.items():
                                html_content = html_content.replace(key, str(value))

                        msg.add_alternative(html_content, subtype='html')
                    except FileNotFoundError:
                        self.log_error(f"HTML template not found: {html_template_path}", self.send_email)
                        return False, 'Email template not found'

                # Handle attachments
                if attachments:
                    if isinstance(attachments, (str, Path)):
                        # Single attachment
                        self._add_attachment(msg, attachments)
                    elif isinstance(attachments, (list, tuple)):
                        # Multiple attachments
                        for attachment in attachments:
                            self._add_attachment(msg, attachment)

                server.send_message(msg)
                return True, 'Email sent successfully'

        except Exception as e:
            self.log_error(e, self.send_email)
            return False, 'Failed to send email, please try again later'