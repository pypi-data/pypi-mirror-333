#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

""" Various clients """

import socket
from urllib.parse import urlparse

import consul
import josepy as jose
import simple_acme_dns
from acme import client as acme_client
from acme import messages

import lofar_cryptocoryne.dns_client as desec


def get_service_certificates() -> [(str, [str])]:
    """Returns all services having a 'cert' tag"""
    consul_client = consul.Consul()
    (_, services) = consul_client.catalog.services()
    certificates = [
        s
        for (s, tags) in services.items()
        if "cert" in tags and not s.endswith("-sidecar-proxy")
    ]
    return [(f"{cert}.lofar.net", []) for cert in certificates]


class DnsClient:
    """DNS client"""

    DNS_SERVERS = [
        socket.gethostbyname("ns1.desec.io"),
        socket.gethostbyname("ns2.desec.org"),
    ]
    """ Client to access the dns providers API """

    def __init__(self, desec_client: desec.APIClient):
        self.desec_client = desec_client
        self.cleanups = []

    def setup_verification(self, verify_domain: str, tokens: [str]):
        """Setup DNS TXT records to verify given domain with given tokens"""
        zone = self.desec_client.get_authoritative_domain(verify_domain)
        subname = verify_domain.rsplit(zone["name"], 1)[0].rstrip(".")
        self.desec_client.add_record(
            zone["name"], "TXT", subname, [f'"{tokens[0]}"'], 3600
        )
        self.cleanups.append(
            lambda d=zone["name"], sn=subname: self.desec_client.delete_record(
                d, "TXT", sn
            )
        )

    def cleanup(self):
        """Cleanup all records created during verification"""
        for cleanup in self.cleanups:
            cleanup()

        self.cleanups = []


class AcmeClient:  # pylint: disable=too-few-public-methods
    """ACME client"""

    def __init__(self, account: messages.RegistrationResource, account_key: jose.JWK):
        self.account = account
        self.account_key = account_key
        self.directory = urlparse(account.uri)._replace(path="/directory").geturl()

    def new_session(self, domain: str) -> simple_acme_dns.ACMEClient:
        """Create a new ACMEClient to perform actions on given domain"""
        client = simple_acme_dns.ACMEClient(
            domains=[domain],
            directory=self.directory,
            nameservers=DnsClient.DNS_SERVERS,
            new_account=False,
            generate_csr=True,
        )
        client.account = self.account
        client.account_key = self.account_key
        client.net = acme_client.ClientNetwork(
            client.account_key, client.account, user_agent="simple_acme_dns/1.0.0"
        )
        client.directory_obj = messages.Directory.from_json(
            client.net.get(client.directory).json()
        )
        client.acme_client = acme_client.ClientV2(client.directory_obj, net=client.net)
        client.account = client.acme_client.query_registration(client.account)
        return client
