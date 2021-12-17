from datetime import datetime, timedelta
import ipaddress


def generate_selfsigned_cert(hostname, ip_addresses=None, key=None):
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    # Generate key
    if key is None:
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend(),
        )

    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, hostname)
    ])

    alt_names = [x509.DNSName(hostname)]

    if ip_addresses:
        for addr in ip_addresses:
            alt_names.append(x509.DNSName(addr))
            alt_names.append(x509.IPAddress(ipaddress.ip_address(addr)))

    san = x509.SubjectAlternativeName(alt_names)

    basic_contraints = x509.BasicConstraints(ca=True, path_length=0)
    now = datetime.utcnow()
    cert = (
        x509.CertificateBuilder()
            .subject_name(name)
            .issuer_name(name)
            .public_key(key.public_key())
            .serial_number(1000)
            .not_valid_before(now)
            .not_valid_after(now + timedelta(days=10 * 365))
            .add_extension(basic_contraints, False)
            .add_extension(san, False)
            .sign(key, hashes.SHA256(), default_backend())
    )
    cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
    key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return cert_pem, key_pem, key


def return_private_key(key):
    cert_pem, key_pem, key_core = generate_selfsigned_cert('localhost', key=key)
    return key_pem


def return_public_key(key):
    cert_pem, key_pem, key_core = generate_selfsigned_cert('localhost', key=key)
    return cert_pem


def return_key_core():
    cert_pem, key_pem, key = generate_selfsigned_cert('localhost')
    return key
