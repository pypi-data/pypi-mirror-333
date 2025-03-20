#  Copyright (C) 2024 ASTRON (Netherlands Institute for Radio Astronomy)
#  SPDX-License-Identifier: Apache-2.0

""" DNS related client extensions """

import desec


class APIClient(desec.APIClient):
    """Extension of desec.APIClient to allow authoritative domain lookup"""

    def get_authoritative_domain(self, qname):
        """Returns the domain for given qname"""
        domains = self.list_domains()
        for domain in domains:
            if qname.endswith(domain["name"]):
                return domain
        raise desec.APIExpectationError(f"Could not find suitable domain for {qname}")
