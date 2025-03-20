import unittest
from ssl_analyzer.analyzer import SSLAnalyzer

class TestSSLAnalyzer(unittest.TestCase):
    def test_fetch_certificate(self):
        analyzer = SSLAnalyzer("www.google.com")
        self.assertIsNotNone(analyzer.cert)

    def test_certificate_info(self):
        analyzer = SSLAnalyzer("www.google.com")
        cert_info = analyzer.get_certificate_info()
        self.assertIn("Issuer", cert_info)

if __name__ == '__main__':
    unittest.main()
