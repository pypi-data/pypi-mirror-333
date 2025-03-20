#  Copyright (C) 2023 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

""" Cryptocoryne certbot cli entrypoint """

import acme.errors
import hvac

import lofar_cryptocoryne.dns_client as desec
from lofar_cryptocoryne import storage
from lofar_cryptocoryne.client import AcmeClient, get_service_certificates, DnsClient


def main():
    """Main entry point for l2ss-cryptocoryne-certbot"""

    vault_store = storage.VaultStore(hvac.Client())
    acme_client = AcmeClient(vault_store.account, vault_store.account_key)
    dns_client = DnsClient(desec.APIClient(vault_store.desec_token))

    for domain, _ in get_service_certificates():
        print(f"Check certificate {domain}...")
        certificate = vault_store.get_certificate(domain)

        if not certificate.should_renew():
            print(f"Certificate {domain} still valid, don't renew")
            continue

        print(f"Certificate {domain} scheduled for renewal, renew")
        try:
            client = acme_client.new_session(domain)
            client.generate_private_key_and_csr(key_type="ec384")

            for verify_domain, tokens in client.request_verification_tokens().items():
                print(f"{verify_domain} -> {tokens}")
                dns_client.setup_verification(verify_domain, tokens)

            print("Waiting for DNS to propagate...")
            if client.check_dns_propagation(timeout=1200):
                print("Succeed. Request certificate")
                client.request_certificate(wait=10)
                certificate.fullchain = client.certificate
                certificate.key = client.private_key
                vault_store.put_certificate(certificate)
                print("Done")
            else:
                print("Failed to issue certificate for " + str(client.domains))

        except acme.errors.ValidationError as ve:
            print(f"ValidationError: {ve.failed_authzrs}")
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"{type(e)}: {e}")
        finally:
            dns_client.cleanup()
