# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from taskgraph.parameters import extend_parameters_schema
from taskgraph.target_tasks import _target_task
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


@_target_task("test")
def target_tasks_test(full_task_graph, parameters, graph_config):
    return ["build-addons-bundle", "signing-addons-bundle", "beetmover-addons-bundle", "beetmover-addons-manifest"]


def get_decision_parameters(graph_config, parameters):
    head_tag = parameters["head_tag"]
    parameters["version"] = head_tag[1:] if head_tag else ""

    pr_number = os.environ.get("MOZILLAVPN_PULL_REQUEST_NUMBER", None)
    parameters["pull_request_number"] = None if pr_number is None else int(pr_number)

    parameters["target_tasks_method"] = "test"

    parameters["existing_tasks"] = {
        "build-addons-bundle": "PJ5mF6RCQTeOCpGIEgPUdQ",
        "signing-addons-bundle": "J-blE2UCSTCfmqQi_VJ44Q",
    }
