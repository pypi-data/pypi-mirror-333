"""
    MONEI API v1

    <p>The MONEI API is organized around <a href=\"https://en.wikipedia.org/wiki/Representational_State_Transfer\">REST</a> principles. Our API is designed to be intuitive and developer-friendly.</p> <h3>Base URL</h3> <p>All API requests should be made to:</p> <pre><code>https://api.monei.com/v1 </code></pre> <h3>Environment</h3> <p>MONEI provides two environments:</p> <ul> <li><strong>Test Environment</strong>: For development and testing without processing real payments</li> <li><strong>Live Environment</strong>: For processing real transactions in production</li> </ul> <h3>Client Libraries</h3> <p>We provide official SDKs to simplify integration:</p> <ul> <li><a href=\"https://github.com/MONEI/monei-php-sdk\">PHP SDK</a></li> <li><a href=\"https://github.com/MONEI/monei-python-sdk\">Python SDK</a></li> <li><a href=\"https://github.com/MONEI/monei-node-sdk\">Node.js SDK</a></li> <li><a href=\"https://postman.monei.com/\">Postman Collection</a></li> </ul> <p>Our SDKs handle authentication, error handling, and request formatting automatically.</p> <p>You can download the OpenAPI specification from the <a href=\"https://js.monei.com/api/v1/openapi.json\">https://js.monei.com/api/v1/openapi.json</a> and generate your own client library using the <a href=\"https://openapi-generator.tech/\">OpenAPI Generator</a>.</p> <h3>Important Requirements</h3> <ul> <li>All API requests must be made over HTTPS</li> <li>If you are not using our official SDKs, you <strong>must provide a valid <code>User-Agent</code> header</strong> with each request</li> <li>Requests without proper authentication will return a <code>401 Unauthorized</code> error</li> </ul> <h3>Error Handling</h3> <p>The API returns consistent error codes and messages to help you troubleshoot issues. Each response includes a <code>statusCode</code> attribute indicating the outcome of your request.</p> <h3>Rate Limits</h3> <p>The API implements rate limiting to ensure stability. If you exceed the limits, requests will return a <code>429 Too Many Requests</code> status code.</p>   # noqa: E501

    The version of the OpenAPI document: 1.5.3
    Generated by: https://openapi-generator.tech
"""


import unittest

import Monei
from Monei.api.subscriptions_api import SubscriptionsApi  # noqa: E501


class TestSubscriptionsApi(unittest.TestCase):
    """SubscriptionsApi unit test stubs"""

    def setUp(self):
        self.api = SubscriptionsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_activate(self):
        """Test case for activate

        Activate Subscription  # noqa: E501
        """
        pass

    def test_cancel(self):
        """Test case for cancel

        Cancel Subscription  # noqa: E501
        """
        pass

    def test_create(self):
        """Test case for create

        Create Subscription  # noqa: E501
        """
        pass

    def test_get(self):
        """Test case for get

        Get Subscription  # noqa: E501
        """
        pass

    def test_pause(self):
        """Test case for pause

        Pause Subscription  # noqa: E501
        """
        pass

    def test_resume(self):
        """Test case for resume

        Resume Subscription  # noqa: E501
        """
        pass

    def test_send_link(self):
        """Test case for send_link

        Send Subscription Link  # noqa: E501
        """
        pass

    def test_send_status(self):
        """Test case for send_status

        Send Subscription Status  # noqa: E501
        """
        pass

    def test_update(self):
        """Test case for update

        Update Subscription  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
