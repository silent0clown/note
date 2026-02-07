from typing import List, Dict, Any
from src.utils.logger import get_logger

logger = get_logger()


class Notifier:
    """Handles notifications through various channels"""

    def __init__(self, config: Dict[str, Any]):
        self.enabled = config.get('enabled', True)
        self.channels = config.get('channels', [])

    def notify(self, message: str, level: str = "info"):
        """
        Send notification through configured channels

        Args:
            message: Notification message
            level: Notification level (info, warning, error)
        """
        if not self.enabled:
            return

        for channel in self.channels:
            channel_type = channel.get('type', 'console')

            try:
                if channel_type == 'console':
                    self._notify_console(message, level)
                elif channel_type == 'email':
                    self._notify_email(message, level, channel)
                elif channel_type == 'webhook':
                    self._notify_webhook(message, level, channel)
                else:
                    logger.warning(f"Unknown notification channel: {channel_type}")

            except Exception as e:
                logger.error(f"Failed to send notification via {channel_type}: {e}")

    def _notify_console(self, message: str, level: str):
        """Send notification to console"""
        prefix = {
            'info': 'ℹ️ ',
            'warning': '⚠️ ',
            'error': '❌ ',
            'success': '✅ '
        }.get(level, '')

        print(f"\n{prefix}{message}\n")
        logger.info(f"Console notification: {message}")

    def _notify_email(self, message: str, level: str, config: Dict[str, Any]):
        """
        Send email notification

        Args:
            message: Notification message
            level: Notification level
            config: Email configuration (smtp_server, from_addr, to_addr, etc.)
        """
        # This is a placeholder for email notification
        # Actual implementation would use smtplib
        logger.info(f"Email notification (not implemented): {message}")

        # Example implementation:
        # import smtplib
        # from email.message import EmailMessage
        #
        # msg = EmailMessage()
        # msg.set_content(message)
        # msg['Subject'] = f"AutoNews Notification - {level.upper()}"
        # msg['From'] = config.get('from_addr')
        # msg['To'] = config.get('to_addr')
        #
        # with smtplib.SMTP(config.get('smtp_server'), config.get('smtp_port', 587)) as server:
        #     server.starttls()
        #     server.login(config.get('username'), config.get('password'))
        #     server.send_message(msg)

    def _notify_webhook(self, message: str, level: str, config: Dict[str, Any]):
        """
        Send webhook notification

        Args:
            message: Notification message
            level: Notification level
            config: Webhook configuration (url, method, headers, etc.)
        """
        # This is a placeholder for webhook notification
        logger.info(f"Webhook notification (not implemented): {message}")

        # Example implementation:
        # import requests
        #
        # payload = {
        #     'message': message,
        #     'level': level,
        #     'timestamp': datetime.now().isoformat()
        # }
        #
        # requests.post(
        #     config.get('url'),
        #     json=payload,
        #     headers=config.get('headers', {})
        # )

    def notify_success(self, message: str):
        """Send success notification"""
        self.notify(message, level='success')

    def notify_error(self, message: str):
        """Send error notification"""
        self.notify(message, level='error')

    def notify_warning(self, message: str):
        """Send warning notification"""
        self.notify(message, level='warning')
