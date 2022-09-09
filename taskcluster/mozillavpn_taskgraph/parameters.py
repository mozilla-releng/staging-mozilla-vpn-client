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
        "repackage-signing-msi": "O-X0PytoRVOo7cu8Gq9l4w",
        "repackage-msi": "Ct_3Jy_0SOWN7ALrcicP2w",
        "signing-windows/opt": "O7FpXQiaTY--ldyuK4vaSA",
        "build-windows/opt": "NuZL4GMoQ06MU4pC1FkT6A",
        "build-android-armv7/debug": "T7NRGTMWSXe3Izhqunm6Tw",
        "build-wasm/opt": "CkgReNb8ThagfaNvvlhBNg",
        "build-android-x86/debug": "QqDT8atdTuK1haoO_bO5fw",
        "build-android-arm64/debug": "Cd3MQeMiSyus_YdRpeSGoA",
        "signing-macos/opt": "GRp0RqvbTl-WVkVQDGS48g",
        "build-macos/opt": "Go9BiHT9TK6bP1JmG7LCPQ",
        "build-android-x64/debug": "QmPKuPXzT0G-bdYvbRZ-Fw",
        "build-ios/debug": "dV0rhrm1R5GQiLSOiBmTBw",
        "signing-addons-bundle": "GD1phCRuRNKL8TL3j11QlA",
        "signing-linux/opt": "LTg5GlR9RgiXKxbuyX2v7Q",
        "build-addons-bundle": "T4RJILAlSt2QAPqxl8z7rA",
        "build-linux/opt": "LeD51-ZYThSVtBzLTlOAgQ",
    }
