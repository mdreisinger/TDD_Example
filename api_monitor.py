"""
The main application file.
Utilizes api_checker to monitor the api so that it can
trigger the email_service when the api goes down or recovers.
"""

import sys
import time

from api_checker import get
from email_service import send_email


class ApiMonitor: # pylint: disable=too-many-instance-attributes
    """
    The main object which is responsible for triggering the email service
    when the api checker reports an outage or recovery.
    """
    def __init__(self, url, support_email="testymctester653@gmail.com", sleep_time=5):
        self.url = url
        self.recipient = support_email
        self.fail_subject = f"URGENT: API ({self.url}) is down!"
        self.recovery_subject = f"API ({self.url}) has recovered from an outage!"
        self.sleep_time=sleep_time
        self.email_service = send_email
        self.api_checker = get
        self.monitor = True

    def start_monitoring(self):
        """
        This is the main method used for this application. It triggers the email_service
        when the api_checker reports an outage or recovery.
        """
        last_state = True # initialize, assuming API is up
        change = False

        try:
            while self.monitor:
                status = self.api_checker(self.url)
                print(f"STATUS: {status}")
                if status != last_state:
                    if change is True: # state change
                        last_state = status
                        if status:
                            self.send_email(self.email_service,
                                            self.recipient,
                                            self.recovery_subject,
                                            self.build_recovery_body())
                            print("API recovered from outage.")
                        else:
                            self.send_email(self.email_service,
                                            self.recipient,
                                            self.fail_subject,
                                            self.build_outage_body())
                            print("API is DOWN!")

                    else: # First change
                        change = True

                if status == last_state: # No change
                    change = False

                time.sleep(self.sleep_time)

        except KeyboardInterrupt:
            print("Bye")
            sys.exit()

    def send_email(self, e_service, recipient, subject, body_text):
        """
        This method uses the email service to send an email.
        It is written this way to accomodate unit testing.
        """
        e_service(recipient, subject, body_text)

    def build_outage_body(self):
        """
        This method returns a string which is intended to be used as the body
        of the email sent when an outage occurs.
        """
        return f"""
        This is an URGENT email. The API @ {self.url} is DOWN!
        """

    def build_recovery_body(self):
        """
        This method returns a string which is intended to be used as the body
        of the email sent when the API recovers from an outage.
        """
        return f"""
        The API @ {self.url} has recovered from an outage!
        """
