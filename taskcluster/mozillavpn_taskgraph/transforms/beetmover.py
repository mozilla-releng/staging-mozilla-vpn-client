# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import os.path

from taskgraph.transforms.base import TransformSequence

transforms = TransformSequence()


@transforms.add
def add_beetmover_worker_config(config, tasks):
    for task in tasks:
        worker_type = task["worker-type"]
        is_relpro = (
            config.params["level"] == "3"
            and config.params["tasks_for"] in task["run-on-tasks-for"]
        )
        bucket = "release" if is_relpro else "dep"
        moz_build_date = config.params["moz_build_date"]
        build_type = task["attributes"]["build-type"]
        build_os = os.path.dirname(build_type)
        shipping_phase = config.params["shipping_phase"]

        def get_version_from_release_branch_head_ref():
            return config.params["head_ref"].split("/")[-1]

        app_version = (
            config.params["version"]
            if config.params["version"]
            else get_version_from_release_branch_head_ref()
        )

        def get_candidates_path():
            if build_type == "addons/opt":
                return os.path.join(
                    "pub",
                    "vpn",
                    "addons",
                    "releases" if shipping_phase.startswith("ship") else "candidates",
                    moz_build_date,
                )
            return os.path.join(
                "pub",
                "vpn",
                "candidates",
                f"{app_version}-candidates",
                f"build{config.params['build_number']}",
                build_os,
            )

        candidates_path = get_candidates_path()
        destination_paths = [candidates_path]

        if shipping_phase == "ship-addons":
            destination_paths.append(
                os.path.join(
                    "pub",
                    "vpn",
                    "addons",
                    "releases",
                    "latest",
                )
            )

        archive_url = (
            "https://ftp.mozilla.org/" if is_relpro else "https://ftp.stage.mozaws.net/"
        )

        def get_task_description():
            if build_type == "addons/opt":
                return f"This {worker_type} task will upload the {task['name']} to {archive_url}{candidates_path}/"
            if shipping_phase == 'ship-client':
                return f"This {worker_type} task will copy build {config.params['build_number']} from candidates to releases"
            return f"This {worker_type} task will upload a {build_os} release candidate for v{app_version} to {archive_url}{candidates_path}/"

        task_description = get_task_description()
        branch = config.params["head_ref"]

        upstream_artifacts = []
        for dep in task["dependencies"]:
            upstream_artifacts.append(
                {
                    "taskId": {"task-reference": f"<{dep}>"},
                    "taskType": dep if dep == "build" else "scriptworker",
                    "paths": [
                        release_artifact["name"]
                        for release_artifact in task["attributes"]["release-artifacts"]
                    ],
                }
            )

        artifact_map = []
        for artifact in upstream_artifacts:
            artifact_map.append(
                {
                    "taskId": artifact["taskId"],
                    "paths": {
                        path: {
                            "destinations": [
                                os.path.join(
                                    destination_path,
                                    os.path.basename(path),
                                )
                                for destination_path in destination_paths
                            ]
                        }
                        for path in artifact["paths"]
                    },
                }
            )
        attributes = {
            **task["attributes"],
            "shipping-phase": shipping_phase,
        }
        worker = {
            "upstream-artifacts": upstream_artifacts,
            "bucket": bucket,
            "action": "push-to-candidates"
            if shipping_phase.endswith("addons") or shipping_phase.startswith("promote")
            else "push-to-releases",
            "release-properties": {
                "app-name": "vpn",
                "app-version": app_version,
                "branch": branch,
                "build-id": moz_build_date,
                "platform": build_type,
            },
            "artifact-map": artifact_map,
            "build-number": config.params["build_number"],
        }
        task_def = {
            "name": task["name"],
            "description": task_description,
            "dependencies": task["dependencies"],
            "worker-type": worker_type,
            "worker": worker,
            "attributes": attributes,
            "run-on-tasks-for": task["run-on-tasks-for"],
        }
        yield task_def
