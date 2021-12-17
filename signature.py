from lxml import etree as ETL
from signxml import XMLSigner
from signxml import XMLVerifier


def create_sign(private_key, file):
    xml_obj = ETL.parse(file)
    signed_xml_obj = XMLSigner().sign(data=xml_obj, key=private_key)
    string_signed_xml = ETL.tostring(signed_xml_obj)

    return string_signed_xml


def verify_sign(signed_data, public_key):
    to_verify = ETL.fromstring(signed_data)
    report = XMLVerifier().verify(data=to_verify, require_x509=True, x509_cert=public_key, ignore_ambiguous_key_info=True)

    return report
