# Copyright (c) 2024-2025 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from pyavd._eos_cli_config_gen.schema import EosCliConfigGen
from pyavd._eos_designs.structured_config.structured_config_generator import structured_config_contributor
from pyavd._utils import get, get_all

if TYPE_CHECKING:
    from . import AvdStructuredConfigNetworkServicesProtocol


class MetadataMixin(Protocol):
    """
    Mixin Class used to generate structured config for one key.

    Class should only be used as Mixin to a AvdStructuredConfig class.
    """

    @structured_config_contributor
    def metadata(self: AvdStructuredConfigNetworkServicesProtocol) -> None:
        """
        Set the metadata.cv_pathfinder for CV Pathfinder routers.

        Pathfinders will always have applications since we have the default control plane apps.
        Edge routers may have internet_exit_policies but not applications.
        """
        if not self.shared_utils.is_cv_pathfinder_router:
            return
        self.set_cv_pathfinder_metadata_internet_exit_policies()
        self.set_cv_pathfinder_metadata_applications()

    def set_cv_pathfinder_metadata_internet_exit_policies(
        self: AvdStructuredConfigNetworkServicesProtocol,
    ) -> None:
        """Set the metadata.cv_pathfinder.internet_exit_policies if available."""
        if not self._filtered_internet_exit_policies_and_connections:
            return

        for internet_exit_policy, connections in self._filtered_internet_exit_policies_and_connections:
            # Currently only supporting zscaler
            if internet_exit_policy.type != "zscaler":
                continue

            ufqdn, ipsec_key = self._get_ipsec_credentials(internet_exit_policy)
            exit_policy = EosCliConfigGen.Metadata.CvPathfinder.InternetExitPoliciesItem(
                name=internet_exit_policy.name,
                type=internet_exit_policy.type,
                city=self._zscaler_endpoints.device_location.city,
                country=self._zscaler_endpoints.device_location.country,
                upload_bandwidth=internet_exit_policy.zscaler.upload_bandwidth,
                download_bandwidth=internet_exit_policy.zscaler.download_bandwidth,
                firewall=internet_exit_policy.zscaler.firewall.enabled,
                ips_control=internet_exit_policy.zscaler.firewall.ips,
                acceptable_use_policy=internet_exit_policy.zscaler.acceptable_use_policy,
            )
            exit_policy.vpn_credentials.append_new(fqdn=ufqdn, vpn_type="UFQDN", pre_shared_key=ipsec_key)
            for connection in connections:
                exit_policy.tunnels.append_new(
                    name=f"Tunnel{connection['tunnel_id']}",
                    preference="Preferred" if connection["preference"] == "primary" else "Alternate",
                    endpoint=connection["endpoint"],
                )
            self.structured_config.metadata.cv_pathfinder.internet_exit_policies.append(exit_policy)

    def set_cv_pathfinder_metadata_applications(self: AvdStructuredConfigNetworkServicesProtocol) -> None:
        """Set the metadata.cv_pathfinder.applications if available."""
        if not self.shared_utils.is_cv_pathfinder_server or self.application_traffic_recognition is None:
            return

        applications = get(self.application_traffic_recognition, "applications", default=[])
        user_defined_app_names = set(get_all(applications, "ipv4_applications.name") + get_all(applications, "ipv6_applications.name"))
        categories = get(self.application_traffic_recognition, "categories", default=[])
        for profile in get(self.application_traffic_recognition, "application_profiles", default=[]):
            application_profile = EosCliConfigGen.Metadata.CvPathfinder.Applications.ProfilesItem(name=profile["name"])
            protocols = get(profile, "application_transports")
            if protocols:
                application_profile.transport_protocols.extend(protocols)
            for application in get(profile, "applications", default=[]):
                if application["name"] not in user_defined_app_names:
                    services = get_all(application, "service")
                    services_item = EosCliConfigGen.Metadata.CvPathfinder.Applications.ProfilesItem.BuiltinApplicationsItem.Services()
                    for service in services:
                        services_item.append(service)
                    application_profile.builtin_applications.append_new(name=application["name"], services=services_item)
                if application["name"] in user_defined_app_names:
                    application_profile.user_defined_applications.append_new(name=application["name"])
            for category in get(profile, "categories", default=[]):
                services = get_all(category, "service")
                services_item = EosCliConfigGen.Metadata.CvPathfinder.Applications.ProfilesItem.CategoriesItem.Services()
                for service in services:
                    services_item.append(service)
                application_profile.categories.append_new(category=category["name"], services=services_item)
            self.structured_config.metadata.cv_pathfinder.applications.profiles.append(application_profile)
        for category in categories:
            for application in get(category, "applications", default=[]):
                if application["name"] not in user_defined_app_names:
                    services_item = EosCliConfigGen.Metadata.CvPathfinder.Applications.Categories.BuiltinApplicationsItem.Services()
                    services = get(category, "service", default=[])
                    for service in services:
                        services_item.append(service)
                    self.structured_config.metadata.cv_pathfinder.applications.categories.builtin_applications.append_new(
                        name=application["name"], category=category["name"], services=services_item
                    )

                if application["name"] in user_defined_app_names:
                    self.structured_config.metadata.cv_pathfinder.applications.categories.user_defined_applications.append_new(
                        name=application["name"], category=category["name"]
                    )
