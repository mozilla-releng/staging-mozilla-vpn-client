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
        "build-wasm/opt": "J-J05CO0RMuSpPLNT3m7jg",
        "repackage-signing-msi": "BPSVHoLtSL-smKKSQ-4r9w",
        "repackage-msi": "S9h1ZGCPRLKcscAIckaZaA",
        "signing-windows/opt": "N9_vyuvIThKLJy17E6i5NQ",
        "build-ios/debug": "WAlqeWZzSTady1NAQC771g",
        "build-windows/opt": "LmLnJoSUSy2_l7cMAOjIWw",
        "signing-macos/opt": "CUujtsjkRkeyCHqM5iLsaA",
        "build-macos/opt": "Ms9OwhjaQ6Sdzkw6tvywGA",
        "build-android-x64/debug": "RSZ7mBZnSByrWkxWC57-KQ",
        "build-android-arm64/debug": "ROA_SsYoS26u4eYZqtNEeQ",
        "build-android-armv7/debug": "f25xoxAbSy2xDcXRqwxMaw",
        "signing-addons-bundle": "CdyioDVOT6W2GRILZ3WfOw",
        "signing-linux/opt": "FDKapgtQQB27z9f3hOyyNA",
        "build-android-x86/debug": "DSVHUbbPRzGwJviaNdG_QQ",
        "build-addons-bundle": "Q1BlaTctRzejbagfW8eRkA",
        "build-linux/opt": "WcYUZ8KuT4-h2l59vbt82A",
    }
