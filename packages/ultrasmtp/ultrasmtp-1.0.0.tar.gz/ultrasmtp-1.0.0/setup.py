from setuptools import setup, find_packages

setup(
    name='ultrasmtp',
    version='1.0.0',
    license="MIT License with attribution requirement",
    author="Ranit Bhowmick",
    author_email='bhowmickranitking@duck.com',
    description='''UltraSMTP is a lightweight Python library for sending emails with attachments and HTML templates. It provides easy configuration for common SMTP settings and offers template-based email rendering.''',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Kawai-Senpai/UltraSMTP',
    download_url='https://github.com/Kawai-Senpai/UltraSMTP',
    keywords=["Email", "SMTP", "HTML Email", "Email Templates", "Email Attachments", "Email Sender"],
    install_requires=[],
)
