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

    def get_san(self):
        """Extract Subject Alternative Names (SAN) from the certificate."""
        try:
            ext = self.cert.extensions.get_extension_for_oid(x509.ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
            return ext.value.get_values_for_type(x509.DNSName)
        except x509.ExtensionNotFound:
            return "N/A"

    def get_key_usage(self):
        """Extract Key Usage information."""
        try:
            ext = self.cert.extensions.get_extension_for_oid(x509.ExtensionOID.KEY_USAGE)
            return {
                "digital_signature": ext.value.digital_signature,
                "content_commitment": ext.value.content_commitment,
                "key_encipherment": ext.value.key_encipherment,
                "data_encipherment": ext.value.data_encipherment,
                "key_agreement": ext.value.key_agreement,
                "key_cert_sign": ext.value.key_cert_sign,
                "crl_sign": ext.value.crl_sign,
                "encipher_only": ext.value.encipher_only,
                "decipher_only": ext.value.decipher_only,
            }
        except x509.ExtensionNotFound:
            return "N/A"

    def get_extended_key_usage(self):
        """Extract Extended Key Usage information."""
        try:
            ext = self.cert.extensions.get_extension_for_oid(x509.ExtensionOID.EXTENDED_KEY_USAGE)
            return [usage.dotted_string for usage in ext.value]
        except x509.ExtensionNotFound:
            return "N/A"

    def check_ocsp_must_staple(self):
        """Check if OCSP Must-Staple is present in the certificate."""
        try:
            ext = self.cert.extensions.get_extension_for_oid(x509.ExtensionOID.TLS_FEATURE)
            return any(feature == 5 for feature in ext.value)
        except x509.ExtensionNotFound:
            return False

    def check_self_signed(self):
        """Check if the certificate is self-signed."""
        return self.cert.issuer == self.cert.subject

    def get_fingerprint(self, hash_alg):
        """Calculate SHA-1 or SHA-256 fingerprint."""
        try:
            return self.cert.fingerprint(getattr(hashlib, hash_alg)).hex()
        except Exception:
            return "N/A"

    def get_public_key_details(self):
        """Extract details from the public key."""
        key_details = {
            "Key Type": type(self.public_key).__name__,
            "Key Size": self.public_key.key_size if hasattr(self.public_key, "key_size") else "N/A",
            "PEM Public Key": "\n" + self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()
        }

        if isinstance(self.public_key, rsa.RSAPublicKey):
            numbers = self.public_key.public_numbers()
            key_details.update({
                "Modulus (n)": str(numbers.n)[:10] + "...",
                "Exponent (e)": numbers.e,
                "Key Algorithm": "RSA",
                "Supported Key Uses": ["Encryption", "Digital Signature"],
                "Weak Key Check": "Key appears strong" if numbers.n.bit_length() >= 2048 else "Weak RSA Key"
            })

        elif isinstance(self.public_key, ec.EllipticCurvePublicKey):
            numbers = self.public_key.public_numbers()
            key_details.update({
                "Curve": self.public_key.curve.name,
                "X Coordinate": str(numbers.x)[:10] + "...",
                "Y Coordinate": str(numbers.y)[:10] + "...",
                "Key Algorithm": "Elliptic Curve (ECC)",
                "Supported Key Uses": ["Digital Signature", "Key Agreement"],
                "Weak Key Check": "Key appears strong"
            })

        elif isinstance(self.public_key, dsa.DSAPublicKey):
            numbers = self.public_key.public_numbers()
            key_details.update({
                "Key Algorithm": "DSA",
                "Parameter p": str(numbers.parameter_numbers.p)[:10] + "...",
                "Parameter q": numbers.parameter_numbers.q,
                "Parameter g": str(numbers.parameter_numbers.g)[:10] + "...",
                "Public y": str(numbers.y)[:10] + "...",
                "Supported Key Uses": ["Digital Signature"],
                "Weak Key Check": "DSA keys require further validation"
            })

        return key_details

    def get_certificate_info(self):
        """Fetch and return SSL certificate details."""
        return {
            "Issuer": self.get_cert_subject(self.cert.issuer),
            "Subject": self.get_cert_subject(self.cert.subject),
            "Serial Number": self.cert.serial_number,
            "Version": self.cert.version.name,
            "Valid From": self.cert.not_valid_before_utc.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "Valid Until": self.cert.not_valid_after_utc.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "Signature Algorithm": self.cert.signature_hash_algorithm.name,
            "SAN": self.get_san(),
            "Public Key": self.get_public_key_details(),
            "Key Usage": self.get_key_usage(),
            "Extended Key Usage": self.get_extended_key_usage(),
            "OCSP Must-Staple": self.check_ocsp_must_staple(),
            "Self-Signed": self.check_self_signed(),
            "SHA-1 Fingerprint": self.get_fingerprint("sha1"),
            "SHA-256 Fingerprint": self.get_fingerprint("sha256"),
        }

    def analyze(self, output_json=False):
        """Return SSL certificate details."""
        details = self.get_certificate_info()
        return json.dumps(details, indent=4) if output_json else details
