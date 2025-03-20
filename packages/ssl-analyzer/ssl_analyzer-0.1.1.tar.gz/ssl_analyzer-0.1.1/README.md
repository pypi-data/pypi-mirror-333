# **SSL Analyzer**
[![PyPI version](https://badge.fury.io/py/ssl-analyzer.svg)](https://pypi.org/project/ssl-analyzer/)  
A Python-based SSL/TLS certificate analysis tool that retrieves detailed information about SSL certificates, including expiration, issuer, key details, and security attributes.

---

## **🔹 Features**
👉 Extracts SSL/TLS version and cipher suite details  
👉 Retrieves certificate issuer, subject, validity period  
👉 Detects **OCSP Must-Staple** & self-signed certificates  
👉 Analyzes **public key strength** (RSA, ECC, DSA)  
👉 Extracts **Subject Alternative Names (SAN)**  
👉 Calculates **SHA-1 & SHA-256 fingerprints**  
👉 Supports **CLI and JSON-formatted output**  

---

## **📛 Installation**
Install the package via **pip**:
```bash
pip install ssl-analyzer
```

---

## **🚀 Usage**
You can use `ssl-analyzer` via CLI or as a Python module.

### **🔹 CLI Usage**
```bash
ssl-analyzer example.com
```
#### **🔹 Output in JSON Format**
```bash
ssl-analyzer example.com --json
```

---

### **🔹 As a Python Module**
You can also use it programmatically:

```python
from ssl_analyzer import SSLAnalyzer

analyzer = SSLAnalyzer("example.com")
ssl_details = analyzer.analyze()
print(ssl_details)
```

---

## **📚 Example Output**
### **🔹 Default CLI Output**
```
SSL CERTIFICATE ANALYZER
========================

----------------------------------------
ISSUER
----------------------------------------
Common Name = DigiCert Global G3 TLS ECC SHA384 2020 CA1
Organization = DigiCert Inc
Country = US
State / Province = N/A
Locality = N/A

----------------------------------------
SUBJECT
----------------------------------------
Common Name = *.example.com
Organization = Internet Corporation for Assigned Names and Numbers
Country = US
State / Province = California
Locality = Los Angeles

----------------------------------------
SERIAL NUMBER
----------------------------------------
14416812407440461216471976375640436634

----------------------------------------
VERSION
----------------------------------------
v3

----------------------------------------
VALID FROM
----------------------------------------
2025-01-15T00:00:00+00:00

----------------------------------------
VALID UNTIL
----------------------------------------
2026-01-15T23:59:59+00:00

----------------------------------------
SIGNATURE ALGORITHM
----------------------------------------
sha384

----------------------------------------
SAN
----------------------------------------
*.example.com
example.com

----------------------------------------
PUBLIC KEY
----------------------------------------
Key Type = ECPublicKey
Key Size = 256
PEM Public Key = 
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEmkiXhC1hbAjJahSgyDiA5gDAh/qZ
Vw4bAOLYh5JX5wj7PF6w04QoN8EkEY7TIHF0vZOPTgkDzgI7sORmc8+v7g==
-----END PUBLIC KEY-----

Curve = secp256r1
X Coordinate = 6978443739...
Y Coordinate = 1136371893...
Key Algorithm = Elliptic Curve (ECC)
Supported Key Uses = ['Digital Signature', 'Key Agreement']
Weak Key Check = Key appears strong

----------------------------------------
KEY USAGE
----------------------------------------
digital_signature = True
content_commitment = False
key_encipherment = False
data_encipherment = False
key_agreement = True
key_cert_sign = False
crl_sign = False
encipher_only = False
decipher_only = False


----------------------------------------
EXTENDED KEY USAGE
----------------------------------------
1.3.6.1.5.5.7.3.1
1.3.6.1.5.5.7.3.2

----------------------------------------
OCSP MUST-STAPLE
----------------------------------------
False

----------------------------------------
SELF-SIGNED
----------------------------------------
False

----------------------------------------
SHA-1 FINGERPRINT
----------------------------------------
N/A

----------------------------------------
SHA-256 FINGERPRINT
----------------------------------------
N/A

```

### **🔹 JSON Output**
```json
{
    "Issuer": {
        "Common Name": "DigiCert Global G3 TLS ECC SHA384 2020 CA1",
        "Organization": "DigiCert Inc",
        "Country": "US",
        "State / Province": "N/A",
        "Locality": "N/A"
    },
    "Subject": {
        "Common Name": "*.example.com",
        "Organization": "Internet Corporation for Assigned Names and Numbers",
        "Country": "US",
        "State / Province": "California",
        "Locality": "Los Angeles"
    },
    "Serial Number": 14416812407440461216471976375640436634,
    "Version": "v3",
    "Valid From": "2025-01-15T00:00:00+00:00",
    "Valid Until": "2026-01-15T23:59:59+00:00",
    "Signature Algorithm": "sha384",
    "SAN": [
        "*.example.com",
        "example.com"
    ],
    "Public Key": {
        "Key Type": "ECPublicKey",
        "Key Size": 256,
        "PEM Public Key": "\n-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEmkiXhC1hbAjJahSgyDiA5gDAh/qZ\nVw4bAOLYh5JX5wj7PF6w04QoN8EkEY7TIHF0vZOPTgkDzgI7sORmc8+v7g==\n-----END PUBLIC KEY-----\n",
        "Curve": "secp256r1",
        "X Coordinate": "6978443739...",
        "Y Coordinate": "1136371893...",
        "Key Algorithm": "Elliptic Curve (ECC)",
        "Supported Key Uses": [
            "Digital Signature",
            "Key Agreement"
        ],
        "Weak Key Check": "Key appears strong"
    },
    "Key Usage": {
        "digital_signature": true,
        "content_commitment": false,
        "key_encipherment": false,
        "data_encipherment": false,
        "key_agreement": true,
        "key_cert_sign": false,
        "crl_sign": false,
        "encipher_only": false,
        "decipher_only": false
    },
    "Extended Key Usage": [
        "1.3.6.1.5.5.7.3.1",
        "1.3.6.1.5.5.7.3.2"
    ],
    "OCSP Must-Staple": false,
    "Self-Signed": false,
    "SHA-1 Fingerprint": "N/A",
    "SHA-256 Fingerprint": "N/A"
}
```

---

## **🛠️ Development & Contribution**
### **🔹 Clone the Repository**
```bash
git clone https://github.com/yourusername/ssl-analyzer.git
cd ssl-analyzer
pip install -r requirements.txt
```

### **🔹 Run Tests**
```bash
pytest tests/
```

### **🔹 Contribute**
- Open an **issue** for bugs/feature requests
- Submit a **pull request** with improvements

---

## **💌 License**
This project is licensed under the **MIT License**.

---

## **🔗 Links**
- 📌 **GitHub**: [https://github.com/TirumalaKrishnaMohanG](https://github.com/TirumalaKrishnaMohanG)
- 📌 **PyPI**: [https://pypi.org/project/ssl-analyzer/](https://pypi.org/project/ssl-analyzer/) 
- 📌 **Author**: Tirumala Krishna Mohan Gudimalla

---

This **README.md** ensures clarity, professionalism, and usability. Let me know if you want any modifications! 🚀

