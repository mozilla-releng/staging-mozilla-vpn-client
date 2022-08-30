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
        "build-wasm/opt": "EY0UkEMsQsi-8NrSuTCXuA",
        "build-android-x86/debug": "RAGq5PNMRw2bYa-Hy5YQdA",
        "build-android-x64/debug": "Gl4v7eOzRIStoVtpZIX-PQ",
        "build-android-arm64/debug": "HSDVE4e_STup1Fv_4TSapg",
        "build-android-armv7/debug": "FVQZTBUSR7GoSA5nNP90iA",
        "build-macos/opt": "O1-OpQclSgWS1ej2NMsnWg",
        "build-windows/opt": "SmMUf1M_QzS1aiILD7KxxA",
        "build-ios/debug": "HOXynK56QCWEH0zTCnKAPg",
        "signing-linux/opt": "cRYUFpKEQ6GLRV-BUwLSnw",
        "build-linux/opt": "Xtn072RKR4O01rFmI-ASvg",
        "signing-macos/opt": "fzLOQWT3TSSkIJiaMlon1Q",
        "signing-windows/opt": "HZYGUI2ZRg-kYSNQ1Xt8nA",
        "repackage-signing-msi": "LBVX4AC-SMGJpITuTC19Fg",
        "repackage-msi": "YBp4B7pcTXanvJ79qjA1AA",
        "push-addon-stage/deploy": "Rnm9Nx36SKGY1h_DVMdx4w",
        "addons-bundle": "fA00WPg2SW674fyRtYxF6A",
    }
