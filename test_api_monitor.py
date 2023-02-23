"""
Basic test to confirm that the api monitor is able to appropriately trigger
emails when the api checker reports a state change.
"""

# pylint: disable=invalid-name

from threading import Thread
import time
from unittest.mock import MagicMock

from api_monitor import ApiMonitor


def test_apiMonitorTriggersOutageEmailAppropriately():
    """
    This test gets the api monitor to trigger a state change from healthy
    to unhealthy and then confirms that the email service was triggered
    once with the correct parameters.
    """
    # pylint: disable=pointless-string-statement

    """Arrange"""
    # Build Unit Under Test
    monitor = ApiMonitor("fakeAssUrl.nothing", sleep_time=0.1)

    # Setup Mock Email
    email_service = MagicMock()
    monitor.email_service = email_service

    # Setup Mock api_checker
    api_checker = MagicMock(side_effect=[True, True, True]+[False for _ in range(100)])
    monitor.api_checker = api_checker

    """Act"""
    thread = Thread(target=monitor.start_monitoring)
    thread.start()
    time.sleep(1)
    monitor.monitor = False
    thread.join()

    """Assert"""
    email_service.assert_called_once_with(monitor.recipient,
                                          monitor.fail_subject,
                                          monitor.build_outage_body())
