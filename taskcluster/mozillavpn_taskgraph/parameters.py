# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from taskgraph.parameters import extend_parameters_schema
from voluptuous import All, Any, Range, Required


def get_defaults(repo_root):
    return {
        "pull_request_number": None,
        "version": "",
    }


extend_parameters_schema(
    {
        Required("pull_request_number"): Any(All(int, Range(min=1)), None),
        Required("version"): str,
    },
    defaults_fn=get_defaults
)


def get_decision_parameters(graph_config, parameters):
    head_tag = parameters["head_tag"]
    parameters["version"] = head_tag[1:] if head_tag else ""

    pr_number = os.environ.get("MOZILLAVPN_PULL_REQUEST_NUMBER", None)
    parameters["pull_request_number"] = None if pr_number is None else int(pr_number)
    parameters["existing_tasks"] = {
        "build-wasm/opt": "cH3WDrI_TQSJmHWfxwVsHw",
        "signing-macos/opt": "Qq0vD_MzQe6zswjq2ibteA",
        "build-macos/opt": "YJxeN_RFSkOwp6W3A3TiuQ",
        "build-ios/debug": "YAr4bgdWRdyJuwzm3F4GvQ",
        "repackage-signing-msi": "eE41UXg3Qiq6zYCxfc4_eQ",
        "repackage-msi": "b_rGALIVSM6ivGZgaI5cDw",
        "signing-windows/opt": "UY3oRvPGQrG5Cp9DlipWbw",
        "build-windows/opt": "AS1k90f0QyyEistAYCiDMA",
        "build-android-x64/debug": "XZ5Hm7jRSOGkh5s41vH9Sw",
        "build-android-arm64/debug": "SXRZGeCvRV6oMGnl6gTMFQ",
        "signing-addons-bundle": "T7VaCJiFQT-ArUkt77dCEg",
        "build-android-x86/debug": "V1Dgn9uqQXeHMPaNkSK9bQ",
        "build-android-armv7/debug": "dhaYJu89T8mgvf0gh0bU3g",
        "build-addons-bundle": "Ct5ziht3SrOUdUZ6BX8okA",
        "signing-linux/opt": "FLAa8CThRHeZJOtlOOsq_g",
        "build-linux/opt": "R3Xpx0qiQ-Sg_1PQWu_8ig",
    }
