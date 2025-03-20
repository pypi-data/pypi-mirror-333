import ssl
import json
import socket
import hashlib
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec, dsa

class SSLAnalyzer:
    """Class to analyze SSL certificates."""

    def __init__(self, hostname, port=443):
        self.hostname = hostname
        self.port = port
        self.cert = None
        self.public_key = None
        self.fetch_certificate()

    def fetch_certificate(self):
        """Fetches SSL certificate from the server."""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.hostname, self.port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    cert_bin = ssock.getpeercert(binary_form=True)
                    self.cert = x509.load_der_x509_certificate(cert_bin, default_backend())
                    self.public_key = self.cert.public_key()
        except Exception as e:
            raise ValueError(f"Error fetching SSL certificate: {e}")

    def get_cert_subject(self, cert_subject):
        """Extract formatted Subject or Issuer details."""
        attributes = {
            "Common Name": x509.NameOID.COMMON_NAME,
            "Organization": x509.NameOID.ORGANIZATION_NAME,
            "Country": x509.NameOID.COUNTRY_NAME,
            "State / Province": x509.NameOID.STATE_OR_PROVINCE_NAME,
            "Locality": x509.NameOID.LOCALITY_NAME,
        }
        return {key: cert_subject.get_attributes_for_oid(oid)[0].value if cert_subject.get_attributes_for_oid(oid) else "N/A" for key, oid in attributes.items()}

    def get_public_key_details(self):
        """Extract public key details."""
        key_info = {
            "Key Type": type(self.public_key).__name__,
            "Key Size": self.public_key.key_size if hasattr(self.public_key, "key_size") else "N/A",
            "PEM Public Key": self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()
        }
        return key_info

    def get_certificate_info(self):
        """Fetch and return SSL certificate details."""
        return {
            "Issuer": self.get_cert_subject(self.cert.issuer),
            "Subject": self.get_cert_subject(self.cert.subject),
            "Valid From": self.cert.not_valid_before.strftime("%Y-%m-%d %H:%M:%S"),
            "Valid Until": self.cert.not_valid_after.strftime("%Y-%m-%d %H:%M:%S"),
            "Signature Algorithm": self.cert.signature_hash_algorithm.name,
            "Public Key": self.get_public_key_details(),
            "SHA-256 Fingerprint": self.cert.fingerprint(hashes.SHA256()).hex(),
        }

    def analyze(self, output_json=False):
        """Return SSL certificate details."""
        details = self.get_certificate_info()
        return json.dumps(details, indent=4) if output_json else details
