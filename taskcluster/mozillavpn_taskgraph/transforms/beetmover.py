# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import os.path

from taskgraph.transforms.base import TransformSequence

transforms = TransformSequence()


@transforms.add
def add_beetmover_worker_config(config, tasks):
    for task in tasks:
        app_name = "vpn"
        attributes = task["attributes"]
        worker_type = task["worker-type"]
        task_name = task["name"]
        task_label = f"{worker_type}-{task_name}"
        run_on_tasks_for = task["run-on-tasks-for"]
        build_id = config.params["moz_build_date"]
        build_type = attributes["build-type"]
        build_os = os.path.dirname(build_type)
        dependencies = task["dependencies"]
        app_version = config.params["version"]
        candidates_path = os.path.join(
            "pub", app_name, "candidates", app_version, build_id, build_os
        )
        destination_paths = [candidates_path]
        task_description = f"Upload the {app_name} {app_version} {build_type} build artifacts to {candidates_path}"
        branch = config.params["head_ref"]
        upstream_artifacts = task["worker"]["upstream-artifacts"]
        artifact_map = []
        for artifact in upstream_artifacts:
            artifact_map.append(
                {
                    "taskId": artifact["taskId"],
                    "paths": {
                        path: {
                            "destinations": [
                                os.path.join(destination_path, os.path.basename(path))
                                for destination_path in destination_paths
                            ]
                        }
                        for path in artifact["paths"]
                    },
                }
            )
        worker = {
            "upstream-artifacts": upstream_artifacts,
            "action": "direct-push-to-bucket",
            "release-properties": {
                "app-name": app_name,
                "app-version": app_version,
                "branch": branch,
                "build-id": build_id,
                "platform": build_type,
            },
            "artifact-map": artifact_map,
        }
        task_def = {
            "label": task_label,
            "name": task_label,
            "description": task_description,
            "dependencies": dependencies,
            "worker-type": worker_type,
            "worker": worker,
            "attributes": attributes,
            "run-on-tasks-for": run_on_tasks_for,
        }
        yield task_def
