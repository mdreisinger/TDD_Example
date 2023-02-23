"""
Some basic tests for the api_checker.
Run with: pytest.
"""

# pylint: disable=invalid-name

from unittest.mock import MagicMock, patch

import api_checker

@patch('api_checker.requests')
def test_apiCheckerShouldReturnTrueGivenCorrectConditions(mock_requests):
    """
    Correct conditions for api_checker to return True are:
        1. HTTP response code is 200.
        2. HTTP “return status” with json response is “OK”.
    """
    # pylint: disable=pointless-string-statement

    """Arrange"""
    # Setup our request response object as a MagicMock.
    mock_request_response = MagicMock()

    # Define the 2 conditions of the request response that should result
    # in checker.get() returning True.
    good_response_code = 200
    good_return_status = {'_links': {'self': {'href': '/health'}},
                          'status': 'OK',
                          'message': 'Everything is hunky dory over here, how are you?'}

    # Add parameters to our Mock request response with the 2 good conditions.
    mock_request_response.status_code = good_response_code
    mock_request_response.json.return_value = good_return_status

    # When checker.get() is called, it will usually invoke the requests library get() method.
    # This was mocked out (Patched) In line 11.
    # Now when checker.get() is called, it will call our mock_requests object
    # instead of the real requests library.
    # Lets set the return value of mock_requests to the mock_request response that we just setup.
    mock_requests.get.return_value = mock_request_response

    """Act"""
    actual_result = api_checker.get("www.fake-AF-URL.com")

    """Assert"""
    assert actual_result

@patch('api_checker.requests')
def test_apiCheckerConsidersAnyResponseCodeOtherThan200ToBeAFailure(mock_requests):
    """
    Test that when ONLY one of the conditions for success is met
    (HTTP response_code is 200.), then it returns False.
    """
    # pylint: disable=pointless-string-statement

    """Arrange"""
    # Setup our request response object as a MagicMock.
    mock_request_response = MagicMock()

    # Define the 2 conditions of the request response
    good_response_code = 200
    bad_return_status = {'_links': {'self': {'href': '/health'}},
                          'status': 'NOT_OK_JesusTakeTheWheel',
                          'message': 'Everything is NOT hunky dory over here! SND HLP'}

    # Add parameters to our Mock request response with the 2 conditions.
    mock_request_response.status_code = good_response_code
    mock_request_response.json.return_value = bad_return_status

    # Set the return value of mock_requests.get() to the mock_request response that we just setup.
    mock_requests.get.return_value = mock_request_response

    """Act"""
    actual_result = api_checker.get("fake-AF-url.doesntevenmatter")

    """Assert"""
    assert not actual_result

@patch('api_checker.requests')
def test_apiCheckerConsidersAnyReturnStatusOtherThanOKToBeAFailure(mock_requests):
    """
    Test that when ONLY one of the conditions for success is met
    (HTTP “return status” with json response is “OK”.), then
    it returns False.
    """
    # pylint: disable=pointless-string-statement

    """Arrange"""
    # Setup our request response object as a MagicMock.
    mock_request_response = MagicMock()

    # Define the 2 conditions of the request response
    bad_response_code = 666 # NOT 200 - Hail Saitan.
    good_return_status = {'_links': {'self': {'href': '/health'}},
                          'status': 'OK',
                          'message': 'Everything is hunky dory over here, how are you?'}

    # Add parameters to our Mock request response with the 2 conditions.
    mock_request_response.status_code = bad_response_code
    mock_request_response.json.return_value = good_return_status

    # Set the return value of mock_requests.get() to the mock_request response that we just setup.
    mock_requests.get.return_value = mock_request_response

    """Act"""
    actual_result = api_checker.get("fake-AF-url.doesntevenmatter")

    """Assert"""
    assert not actual_result
