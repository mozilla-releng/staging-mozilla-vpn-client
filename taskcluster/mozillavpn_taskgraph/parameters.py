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
        "repackage-signing-msi": "cLhmqc95SFisEdFpKBdNlg",
        "repackage-msi": "ciVCCUGySby_aMBjnkazuw",
        "signing-windows/opt": "MOm81GjES-i1EG4UuwgOFQ",
        "build-windows/opt": "VYqW2Oa_QgyOoUcVNW3ayw",
        "build-wasm/opt": "D5t7PJ17RNuzEpNomw3z7w",
        "build-android-x86/debug": "G9CFQ2XjRcm9ptDY4gAiJA",
        "build-android-x64/debug": "OaoEaXKqSgWmYvJ7J5XboA",
        "build-android-armv7/debug": "f57lFIj2QUKst9XELcMwRQ",
        "build-macos/opt": "IvatMZ1fQ4yDeDRdeerROg",
        "signing-macos/opt": "apbK_GozTx2-1NJJkMd80w",
        "build-android-arm64/debug": "KVuraRN9TfWxjC3k_JUfyQ",
        "build-ios/debug": "ckYCm8qLS7CfCKhDxc9qRw",
        "signing-linux/opt": "JfnCn3v6Rei1iSarkZuB7g",
        "build-linux/opt": "JARWCWEORkyd41n3Fgl1AQ",
    }
