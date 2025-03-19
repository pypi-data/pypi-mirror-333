# UltraSMTP

UltraSMTP is a lightweight Python library for sending emails with attachments and HTML templates. It provides easy configuration for common SMTP settings and offers template-based email rendering.

## Features
- Simple configuration of SMTP details (host, port, username, password).
- Support for plain and HTML email content.
- Built-in template loading with customizable placeholders.
- Flexible handling of recipients (To, CC, BCC) and display names.
- Attach multiple files effortlessly.
- Preview text insertion for better email client previews.

## Installation

To install UltraSMTP, you can use pip:

```sh
pip install ultrasmtp
```

## Usage

1. Import and initialize the UltraSMTP class with your SMTP credentials:
   ```python
   from ultrasmtp import UltraSMTP

   email = UltraSMTP("smtp_host", 587, "username", "password")
   ```

2. Use the `send_email` method to send emails:
   ```python
   email.send_email(
       to="recipient@example.com",
       subject="Hello from UltraSMTP!",
       body="This is an email body.",
       html_template="default",
       attachments=["/path/to/file1.pdf", "/path/to/file2.png"]
   )
   ```

## Functions

### UltraSMTP.__init__(smtp_host, smtp_port, username, password)
- Initializes the UltraSMTP object.
- Parameters:
  - `smtp_host` (str): SMTP server address.
  - `smtp_port` (int): SMTP port (commonly 587).
  - `username` (str): Login username.
  - `password` (str): Login password.

### UltraSMTP.send_email(...)
- Sends an email.
- Parameters:
  - `to` (str | list | dict | list[dict]): Recipient or multiple recipients; supports name/email dicts.
  - `subject` (str): Email subject.
  - `body` (str): Main email content (plain text or HTML).
  - `from_email` (str): Sender's email address (defaults to `username`).
  - `from_name` (str): Sender's display name.
  - `reply_to` (str | dict): Reply-to address.
  - `cc` (str | list | dict | list[dict]): CC recipients.
  - `bcc` (str | list | dict | list[dict]): BCC recipients.
  - `preview_text` (str): Hidden snippet for email preview.
  - `attachments` (list[str]): File paths to attach.
  - `html_template` (str): Template name without file extension.
  - `template_path` (str): Custom HTML template path.

## Example

```python
from ultrasmtp import UltraSMTP

creds = {
   "smtp_server": "smtp.example.com",
   "smtp_port": 587,
   "sender_email": "user@example.com",
   "sender_password": "examplepass"
}

email = UltraSMTP(
   creds["smtp_server"],
   creds["smtp_port"],
   creds["sender_email"],
   creds["sender_password"]
)

email.send_email(
   to=["alice@example.com", {"email": "bob@example.com", "name": "Bob"}],
   subject="Greetings!",
   body="<p>This is an <b>HTML</b> email</p>",
   from_name="Your Name",
   preview_text="Short preview goes here",
   attachments=["/path/to/report.pdf"]
)
```

## Detailed Parameters

### `to`
- Type: `str | list | dict | list[dict]`
- Description: Recipient or multiple recipients. Supports name/email dictionaries.
- Examples:
  - `"recipient@example.com"`
  - `["recipient1@example.com", "recipient2@example.com"]`
  - `{"email": "recipient@example.com", "name": "Recipient Name"}`
  - `[{"email": "recipient1@example.com", "name": "Recipient One"}, {"email": "recipient2@example.com", "name": "Recipient Two"}]`

### `subject`
- Type: `str`
- Description: The subject of the email.

### `body`
- Type: `str`
- Description: The main content of the email. Can be plain text or HTML.

### `from_email`
- Type: `str`
- Description: The sender's email address. Defaults to the username provided during initialization.

### `from_name`
- Type: `str`
- Description: The display name of the sender.

### `reply_to`
- Type: `str | dict`
- Description: The reply-to address. Can be a string or a dictionary with 'email' and 'name'.

### `cc`
- Type: `str | list | dict | list[dict]`
- Description: CC recipients. Supports multiple formats similar to `to`.

### `bcc`
- Type: `str | list | dict | list[dict]`
- Description: BCC recipients. Supports multiple formats similar to `to`.

### `preview_text`
- Type: `str`
- Description: A hidden snippet for email preview in clients.

### `attachments`
- Type: `list[str]`
- Description: List of file paths to attach to the email.

### `html_template`
- Type: `str`
- Description: The name of the HTML template to use (without file extension).

### `template_path`
- Type: `str`
- Description: Custom path to an HTML template file.

## Enhanced Documentation

UltraSMTP is designed to be simple yet powerful. It supports both plain text and HTML emails with customizable templates and attachments. This guide provides a step-by-step approach, detailed API reference, and practical examples.

### Quick Start

1. Install UltraSMTP:
```sh
pip install ultrasmtp
```

2. Initialize the library:
```python
from ultrasmtp import UltraSMTP

creds = {
   "smtp_server": "smtp.example.com",
   "smtp_port": 587,
   "sender_email": "user@example.com",
   "sender_password": "examplepass",
   "from_email": "user@example.com",
   "reply_to": "reply@example.com"
}

email = UltraSMTP(creds)
```

3. Send an email:
```python
email.send_email(
   to="recipient@example.com",
   from_name="Your Name",
   subject="Hello from UltraSMTP!",
   plain_content="This is an email body.",
   html_template_path="path/to/template.html",
   attachments=["/path/to/file.pdf"]
)
```

### Advanced Usage

- Multiple recipients and CC/BCC support:
```python
email.send_email(
   to=["alice@example.com", {"email": "bob@example.com", "name": "Bob"}],
   cc="cc@example.com",
   bcc="bcc@example.com",
   subject="Group Email",
   plain_content="This email contains multiple recipients."
)
```

- Custom HTML templates with placeholders:
```python
email.send_email(
   to="recipient@example.com",
   from_name="Your Company",
   subject="Welcome!",
   plain_content="Welcome to our service.",
   html_template_path="templates/welcome.html",
   placeholders={"{{username}}": "User"}
)
```

### Examples Folder

For a comprehensive demonstration, refer to the examples in the `examples` folder.

