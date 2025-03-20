"""
The `services` module provides various services for delivering documents and managing
templates. These services include sending emails, uploading files to S3, and transferring 
files over SFTP. Additionally, the `TemplateManager` handles the generation of documents 
based on different data sources.

Classes:
    EmailMessageBuilder: Helps in constructing email messages.
    EmailSender: Sends emails via an SMTP server.
    AWSConfig: Configures the AWS credentials and region.
    S3Delivery: Uploads files to Amazon S3.
    SFTPDelivery: Transfers files via SFTP.
    SMTPConfig: Configures the SMTP server for sending emails.
    TemplateManager: Manages document templates and integrates them with data sources.
"""

from .s3_delivery import AWSConfig, S3Delivery
from .sftp_delivery import SFTPDelivery
from .smtp_delivery import EmailMessageBuilder, EmailSender, SMTPConfig
from .template_manager import TemplateManager

__all__ = [
    "EmailMessageBuilder",
    "EmailSender",
    "AWSConfig",
    "S3Delivery",
    "SFTPDelivery",
    "SMTPConfig",
    "TemplateManager",
]
