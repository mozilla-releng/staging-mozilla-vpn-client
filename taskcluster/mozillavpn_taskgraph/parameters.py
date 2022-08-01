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
        "build-android-arm64/debug": "EdMeHxgPSyCU_a4oHPSCPA",
        "build-android-armv7/debug": "MeanU8ewmSQCSoaY0PnrlhQ",
        "build-android-x64/debug": "a_MV7swEQK-TQ5otPwUcOQ",
        "build-android-x86/debug": "YFVgUS3VSN63rV2BC7sd3Q",
        "build-ios/debug": "R9h3Vbw-RQK2NSbotFc60A",
        "build-linux/opt": "LvJ3BFX9Sw--qtL92Gce3w",
        "build-macos/opt": "aHKPXSztQ3-h_r2X3O-tSQ",
        "build-wasm/opt": "GsMtW8ohQC-vLE0jbbz63Q",
        "build-windows/opt": "AYzjU7bbTKSMC0r7DV7_-A",
        "signing-macos/opt": "Hm4fAljHQiG1-vl6AoGQPA",
    }
