# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from taskgraph.parameters import extend_parameters_schema
from voluptuous import All, Any, Range, Required


def get_defaults(repo_root):
    return {
        "pull_request_number": None,
        "shipping_phase": None,
        "version": "",
    }


extend_parameters_schema(
    {
        Required("pull_request_number"): Any(All(int, Range(min=1)), None),
        Required("shipping_phase"): Any(str, None),
        Required("version"): str,
    },
    defaults_fn=get_defaults,
)


def get_decision_parameters(graph_config, parameters):
    head_tag = parameters["head_tag"]
    parameters["version"] = head_tag[1:] if head_tag else ""

    pr_number = os.environ.get("MOZILLAVPN_PULL_REQUEST_NUMBER", None)
    parameters["pull_request_number"] = None if pr_number is None else int(pr_number)
    parameters.update(
        {
            "target_tasks_method": "client-target-tasks",
            "existing_tasks": {
                "beetmover-macos": "O0-eEGsFQYKzctl6ZmxETA",
                "beetmover-windows": "VbQDp2TSTAqd-1s3tSeE8w",
                "build-macos/opt": "c10jdtQZT2mlSWR1sIhMdQ",
                "build-windows/opt": "UTZUAxqkSLiz1Ashq_dy9w",
                "repackage-msi": "ZGAk37KzSySxy5-unnAw4w",
                "repackage-signing-msi": "NJd5IiKuRcm39VVcRYyklw",
                "signing-macos/opt": "cziK2Kz3S5KaCZUis9f2OA",
                "signing-windows/opt": "dJk2WQCpQ5uhsGjogKOp6w",
            },
            "shipping_phase": "promote-client",
        }
    )
