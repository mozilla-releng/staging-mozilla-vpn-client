# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from taskgraph.target_tasks import _target_task


@_target_task("promote-addons")
def target_tasks_promote_addons(full_task_graph, parameters, graph_config):
    def filter(task):
        if task.attributes.get("shipping-phase") == "promote-addons":
            return True

    return [label for label, task in full_task_graph.tasks.items() if filter(task)]


@_target_task("ship-addons")
def target_tasks_ship_addons(full_task_graph, parameters, graph_config):
    def filter(task):
        if task.attributes.get("shipping-phase") == "ship-addons":
            return True


    return [label for label, task in full_task_graph.tasks.items() if filter(task)]


@_target_task("promote-client")
def target_tasks_promote_client(full_task_graph, parameters, graph_config):
    def filter(task):
        if task.attributes.get("shipping-phase") == "promote-client":
            return True


    return [label for label, task in full_task_graph.tasks.items() if filter(task)]


@_target_task("ship-client")
def target_tasks_ship_client(full_task_graph, parameters, graph_config):
    def filter(task):
        if task.attributes.get("shipping-phase") == "ship-client":
            return True


    return [label for label, task in full_task_graph.tasks.items() if filter(task)]
