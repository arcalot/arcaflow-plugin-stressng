#!/usr/bin/env python3

import sys
import typing
import tempfile
import subprocess
import os
import yaml

from arcaflow_plugin_sdk import plugin
from stressng_schema import (
    Stressors,
    StressNGParams,
    WorkloadResults,
    WorkloadError,
    system_info_output_schema,
    stressor_schemas,
)


@plugin.step(
    id="workload",
    name="stress-ng workload",
    description="Run the stress-ng workload with the given parameters",
    outputs={"success": WorkloadResults, "error": WorkloadError},
)
def stressng_run(
    params: StressNGParams,
) -> typing.Tuple[str, typing.Union[WorkloadResults, WorkloadError]]:
    print("==>> Generating temporary jobfile...")
    # generic parameters are in the StressNGParams class (e.g. the timeout)
    result = params.to_jobfile()
    # now we need to iterate of the list of stressors
    for item in params.stressors:
        result = result + item.to_jobfile()

    stressng_jobfile = tempfile.mkstemp()
    stressng_outfile = tempfile.mkstemp()

    # write the temporary jobfile
    try:
        with open(stressng_jobfile[1], "w") as jobfile:
            try:
                jobfile.write(result)
            except IOError as error:
                return "error", WorkloadError(
                    f"{error} while trying to write {stressng_jobfile[1]}"
                )
    except EnvironmentError as error:
        return "error", WorkloadError(
            f"{error} while trying to open {stressng_jobfile[1]}"
        )

    stressng_command = [
        "/usr/bin/stress-ng",
        "-j",
        stressng_jobfile[1],
        "--metrics",
        "-Y",
        stressng_outfile[1],
    ]

    print("==>> Running stress-ng with the temporary jobfile...")
    workdir = "/tmp"
    if params.workdir is not None:
        workdir = params.workdir
    try:
        print(
            subprocess.check_output(
                stressng_command,
                cwd=workdir,
                text=True,
                stderr=subprocess.STDOUT,
            )
        )
    except subprocess.CalledProcessError as error:
        return "error", WorkloadError(
            f"""{error.cmd[0]} failed with return code
                {error.returncode}:\n{error.output}"""
        )

    try:
        with open(stressng_outfile[1], "r") as output:
            try:
                stressng_yaml = yaml.safe_load(output)
            except yaml.YAMLError as error:
                print(error)
                return "error", WorkloadError(
                    f"""{error} in
                                                  {stressng_outfile[1]}"""
                )
    except EnvironmentError as error:
        return "error", WorkloadError(
            f"{error} while trying to open {stressng_outfile[1]}"
        )

    system_info = stressng_yaml["system-info"]
    metrics = stressng_yaml["metrics"]

    system_un = system_info_output_schema.unserialize(system_info)
    un = {
        m["stressor"]: stressor_schemas[m["stressor"]].unserialize(m) for m in metrics
    }

    print("==>> Workload run complete!")
    os.close(stressng_jobfile[0])
    os.close(stressng_outfile[0])

    if params.cleanup:
        print("==>> Cleaning up operation files...")
        os.remove(stressng_jobfile[1])

    return "success", WorkloadResults(
        test_config=params,
        systeminfo=system_un,
        vminfo=un.get(Stressors.VM),
        mmapinfo=un.get(Stressors.MMAP),
        cpuinfo=un.get(Stressors.CPU),
        matrixinfo=un.get(Stressors.MATRIX),
        mqinfo=un.get(Stressors.MQ),
        hddinfo=un.get(Stressors.HDD),
        iomixinfo=un.get(Stressors.IOMIX),
        sockinfo=un.get(Stressors.SOCK),
    )


if __name__ == "__main__":
    sys.exit(
        plugin.run(
            plugin.build_schema(
                stressng_run,
            )
        )
    )
