
import urllib.parse
from urllib.parse import quote

from payment_page_sdk.signature_handler import SignatureHandler
from payment_page_sdk.payment import Payment
from payment_page_sdk.cipher import AESCipher

class PaymentPage(object):
    """Class PaymentPage for URL building

    Attributes:
        __signatureHandler - Signature Handler (check, sign)
    """
    __signatureHandler = None

    def __init__(self, signature_handler: SignatureHandler):
        """
        PaymentPage constructor

        :param signature_handler:
        """
        self.__signatureHandler = signature_handler

    def get_url(self, base_url: str, payment: Payment, encryption_key: str ='') -> str:
        """
        Get full URL for payment

        :param Payment payment:
        :return:
        """
        payload = '/payment?' + urllib.parse.urlencode(payment.get_params(), quote_via=quote) \
            + '&signature=' + urllib.parse.quote_plus(self.__signatureHandler.sign(payment.get_params()))
        
        if encryption_key:
            crypt = AESCipher(encryption_key)
            encrypted = crypt.encrypt(payload)
            return base_url + '/' + payment.project_id + '/' + encrypted
        

        return base_url + payload