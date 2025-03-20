#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

""" Abstraction for Certificate and Vault storage handling """

import logging
from datetime import datetime, timedelta

import hvac
import pytz
from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding as CryptEncoding
from hvac.exceptions import InvalidPath
import josepy as jose
from acme import messages

logger = logging.getLogger(__name__)

renew_before_expiry = timedelta(days=30)


class Certificate:
    """Models a PEM certificate"""

    def __init__(self, domain: str, cert_data: dict) -> None:
        self.domain = domain
        self.is_new = False
        self.cert: bytes = b""
        self.key: bytes = b""
        self.chain: bytes = b""

        for k in ["cert", "chain", "key"]:
            if k not in cert_data:
                self.is_new = True
                break
            data = cert_data[k]
            if isinstance(data, str):
                data = data.encode()
            setattr(self, k, data)

    @property
    def fullchain(self) -> bytes:
        """Returns the full certificate + chain"""
        return self.cert + b"\n" + self.chain

    @fullchain.setter
    def fullchain(self, certs: bytes):
        """Updates cert and chain from fullchain"""
        certs = x509.load_pem_x509_certificates(certs)
        self.cert = certs[0].public_bytes(CryptEncoding.PEM)
        self.chain = certs[1].public_bytes(CryptEncoding.PEM)

    @property
    def not_valid_after(self) -> datetime:
        """Returns not valid after date of certificate"""
        cert = x509.load_pem_x509_certificate(self.cert)
        return cert.not_valid_after_utc

    def should_renew(self) -> bool:
        """Determines if the certificate should be renewed.
        Always True for new certificates"""
        if self.is_new:
            return True

        if self.not_valid_after < (datetime.now(pytz.UTC) + renew_before_expiry):
            return True
        return False


class VaultStore:
    """Abstraction of Vault Storage access"""

    CERTIFICATE_SUB_DIR = "certificates"
    ACCOUNT_SUB_DIR = "account"

    def __init__(self, vault_client: hvac.Client, mount_point="lets-encrypt") -> None:
        self.vault_client = vault_client
        self.mount_point = mount_point

    def get_certificate(self, domain) -> Certificate:
        """Returns certificate for given domain"""
        try:
            secret = self.vault_client.secrets.kv.v2.read_secret(
                path=f"{self.CERTIFICATE_SUB_DIR}/{domain}",
                mount_point=self.mount_point,
            )
            return Certificate(domain, secret["data"]["data"])
        except InvalidPath:
            return Certificate(domain, {})

    def put_certificate(self, cert: Certificate):
        """Updates given certificate in the vault storage"""
        self.vault_client.secrets.kv.v2.create_or_update_secret(
            mount_point=self.mount_point,
            path=f"{self.CERTIFICATE_SUB_DIR}/{cert.domain}",
            secret={
                "cert": cert.cert.decode(),
                "chain": cert.chain.decode(),
                "key": cert.key.decode(),
            },
        )

    @property
    def desec_token(self):
        """Returns the desec DNS auth token from the vault"""
        desec_token = self.vault_client.secrets.kv.v2.read_secret(
            path="dns_desec_token",
            mount_point=self.mount_point,
        )
        return desec_token["data"]["data"]["token"]

    @property
    def account_key(self) -> jose.JWK:
        """Returns the letsencrypt account key from the vault"""
        account_private_key = self.vault_client.secrets.kv.v2.read_secret(
            path=f"{self.ACCOUNT_SUB_DIR}/private_key",
            mount_point=self.mount_point,
        )

        return jose.JWKRSA.fields_from_json(account_private_key["data"]["data"])

    @property
    def account(self) -> messages.RegistrationResource:
        """Returns the letsencrypt account info from the vault"""
        account_reg = self.vault_client.secrets.kv.v2.read_secret(
            path=f"{self.ACCOUNT_SUB_DIR}/regr",
            mount_point=self.mount_point,
        )

        return messages.RegistrationResource.from_json(account_reg["data"]["data"])
