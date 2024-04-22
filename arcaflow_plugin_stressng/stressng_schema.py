#!/usr/bin/env python3

import typing
import enum
from dataclasses import dataclass

from arcaflow_plugin_sdk import plugin, schema
from arcaflow_plugin_sdk import annotations


class Stressors(str, enum.Enum):
    CPU = "cpu"
    VM = "vm"
    MATRIX = "matrix"
    MQ = "mq"
    HDD = "hdd"


@dataclass
class CommonStressorParams:
    stressor: typing.Annotated[
        Stressors,
        schema.name("Stressor"),
        schema.description("Stressor for the benchmark workload"),
    ]

    workers: typing.Annotated[
        int,
        schema.name("Worker Count"),
        schema.description("Number of workers for the stressor"),
    ]


@dataclass
class CpuStressorParams(CommonStressorParams):
    cpu_method: typing.Annotated[
        typing.Optional[str],
        schema.name("CPU Stressor Method"),
        schema.description(
            "Fine grained control of which "
            "CPU stressors to use (ackermann, "
            "cfloat etc.)"
        ),
    ] = "all"

    cpu_load: typing.Annotated[
        typing.Optional[int],
        schema.name("CPU Load"),
        schema.description("Load CPU by percentage"),
    ] = None

    def to_jobfile(self) -> str:
        result = "cpu {}\n".format(self.workers)
        if self.cpu_method is not None:
            result = result + "cpu-method {}\n".format(self.cpu_method)
        if self.cpu_load is not None:
            result = result + "cpu-load {}\n".format(self.cpu_load)
        return result


@dataclass
class VmStressorParams(CommonStressorParams):
    vm_bytes: typing.Annotated[
        str,
        schema.name("VM Memory"),
        schema.description("Amount of memory a single VM stressor will use"),
    ]

    mmap: typing.Annotated[
        typing.Optional[str],
        schema.name("Mmap"),
        schema.description("Number of stressors per CPU"),
    ] = None

    mmap_bytes: typing.Annotated[
        typing.Optional[str], schema.name("Memory Per Stressor")
    ] = None

    def to_jobfile(self) -> str:
        vm = "vm {}\n".format(self.workers)
        vm_bytes = "vm-bytes {}\n".format(self.vm_bytes)
        result = vm + vm_bytes
        if self.mmap is not None:
            result = result + "mmap {}\n".format(self.mmap)
        if self.mmap_bytes is not None:
            result = result + "mmap-bytes {}\n".format(self.mmap_bytes)
        return result


@dataclass
class MatrixStressorParams(CommonStressorParams):
    def to_jobfile(self) -> str:
        matrix = "matrix {}\n".format(self.workers)
        result = matrix
        return result


@dataclass
class MqStressorParams(CommonStressorParams):
    def to_jobfile(self) -> str:
        mq = "mq {}\n".format(self.workers)
        result = mq
        return result


@dataclass
class HDDStressorParams(CommonStressorParams):
    hdd_bytes: typing.Annotated[
        str,
        schema.name("Bytes Per Worker"),
        schema.description(
            "write  N  bytes for each hdd process, the default is 1 GB. "
            "One can specify the size in units of Bytes, KBytes, "
            "MBytes and GBytes using the suffix b, k, m or g."
        ),
    ]

    hdd_write_size: typing.Annotated[
        str,
        schema.name("Write Size"),
        schema.description(
            "specify size of each write "
            "in bytes. Size can be from 1 byte to 4MB"
            "One can specify the size in units of Bytes, KBytes, "
            "MBytes using the suffix b, k, m"
        ),
    ]

    def to_jobfile(self) -> str:
        hdd = "hdd {}\n".format(self.workers)
        hdd_bytes = "hdd-bytes {}\n".format(self.hdd_bytes)
        hdd_write_size = "hdd-write-size {}\n".format(self.hdd_write_size)
        result = hdd + hdd_bytes + hdd_write_size
        return result


@dataclass
class StressNGParams:
    timeout: typing.Annotated[
        str,
        schema.name("Runtime"),
        schema.description("Time to run the benchmark test"),
    ]

    stressors: typing.List[
        typing.Annotated[
            typing.Union[
                typing.Annotated[
                    CpuStressorParams,
                    annotations.discriminator_value("cpu"),
                    schema.name("CPU Stressor Parameters"),
                    schema.description("Parameters for running the cpu stressor"),
                ],
                typing.Annotated[
                    VmStressorParams,
                    annotations.discriminator_value("vm"),
                    schema.name("VM Stressor Parameters"),
                    schema.description("Parameters for running the vm stressor"),
                ],
                typing.Annotated[
                    MatrixStressorParams,
                    annotations.discriminator_value("matrix"),
                    schema.name("Matrix Stressor Parameters"),
                    schema.description("Parameters for running the matrix stressor"),
                ],
                typing.Annotated[
                    MqStressorParams,
                    annotations.discriminator_value("mq"),
                    schema.name("MQ Stressor Parameters"),
                    schema.description("Parameters for running the mq stressor"),
                ],
                typing.Annotated[
                    HDDStressorParams,
                    annotations.discriminator_value("hdd"),
                    schema.name("HDD Stressor Parameters"),
                    schema.description("Parameters for running the hdd stressor"),
                ],
            ],
            annotations.discriminator("stressor"),
            schema.name("Stressors List"),
            schema.description("List of stress-ng stressors and parameters"),
        ]
    ]

    verbose: typing.Annotated[
        typing.Optional[bool],
        schema.name("Verbose"),
        schema.description("verbose output"),
    ] = None

    metrics_brief: typing.Annotated[
        typing.Optional[bool],
        schema.name("Brief Metrics"),
        schema.description("Brief version of the metrics output"),
    ] = None

    workdir: typing.Annotated[
        typing.Optional[str],
        schema.name("Working Dir"),
        schema.description(
            "Path were stress-ng will be "
            "executed (example to target a specific volume)"
        ),
    ] = None

    cleanup: typing.Annotated[
        typing.Optional[bool],
        schema.name("Cleanup"),
        schema.description("Cleanup artifacts after the plugin run"),
    ] = False

    def to_jobfile(self) -> str:
        result = "timeout {}\n".format(self.timeout)
        if self.verbose is not None:
            result = result + "verbose {}\n".format(self.verbose)
        if self.metrics_brief is not None:
            result = result + "metrics-brief {}\n".format(self.metrics_brief)
        return result


@dataclass
class SystemInfoOutput:
    stress_ng_version: typing.Annotated[
        str,
        schema.id("stress-ng-version"),
        schema.name("stress_ng_version"),
        schema.description("version of the stressng tool used"),
    ]

    run_by: typing.Annotated[
        str,
        schema.id("run-by"),
        schema.name("run_by"),
        schema.description("username of the person who ran the test"),
    ]

    date: typing.Annotated[
        str,
        schema.id("date-yyyy-mm-dd"),
        schema.name("date"),
        schema.description("date on which the test was run"),
    ]

    time: typing.Annotated[
        str,
        schema.id("time-hh-mm-ss"),
        schema.name("time"),
        schema.description("time at which the test was run"),
    ]

    epoch: typing.Annotated[
        int,
        schema.id("epoch-secs"),
        schema.name("epoch"),
        schema.description("epoch at which the test was run"),
    ]

    hostname: typing.Annotated[
        str,
        schema.name("hostname"),
        schema.description("host on which the test was run"),
    ]

    sysname: typing.Annotated[
        str, schema.name("system name"), schema.description("System name")
    ]

    nodename: typing.Annotated[
        str,
        schema.name("nodename"),
        schema.description("name of the node on which the test was run"),
    ]

    release: typing.Annotated[
        str,
        schema.name("release"),
        schema.description("kernel release on which the test was run"),
    ]

    version: typing.Annotated[
        str,
        schema.name("version"),
        schema.description("version on which the test was run"),
    ]

    machine: typing.Annotated[
        str,
        schema.name("machine"),
        schema.description("machine type on which the test was run"),
    ]

    uptime: typing.Annotated[
        int,
        schema.name("uptime"),
        schema.description("uptime of the machine the test was run on"),
    ]

    totalram: typing.Annotated[
        int,
        schema.name("totalram"),
        schema.description("total amount of RAM the test machine had"),
    ]

    freeram: typing.Annotated[
        int,
        schema.name("freeram"),
        schema.description("amount of free RAM the test machine had"),
    ]

    sharedram: typing.Annotated[
        int,
        schema.name("sharedram"),
        schema.description("amount of shared RAM the test machine had"),
    ]

    bufferram: typing.Annotated[
        int,
        schema.name("bufferram"),
        schema.description("amount of buffer RAM the test machine had"),
    ]

    totalswap: typing.Annotated[
        int,
        schema.name("totalswap"),
        schema.description("total amount of swap the test machine had"),
    ]

    freeswap: typing.Annotated[
        int,
        schema.name("freeswap"),
        schema.description("amount of free swap the test machine had"),
    ]

    pagesize: typing.Annotated[
        int,
        schema.name("pagesize"),
        schema.description("memory page size the test machine used"),
    ]

    cpus: typing.Annotated[
        int,
        schema.name("cpus"),
        schema.description("number of CPU cores the test machine had"),
    ]

    cpus_online: typing.Annotated[
        int,
        schema.id("cpus-online"),
        schema.name("cpus_online"),
        schema.description("number of online CPUs the test machine had"),
    ]

    ticks_per_second: typing.Annotated[
        int,
        schema.id("ticks-per-second"),
        schema.name("ticks_per_second"),
        schema.description("ticks per second used on the test machine"),
    ]


system_info_output_schema = plugin.build_object_schema(SystemInfoOutput)


@dataclass
class CommonOutput:
    stressor: typing.Annotated[
        str,
        schema.name("Stressor"),
        schema.description("Type of stressor for workload"),
    ]

    max_rss: typing.Annotated[
        int,
        schema.id("max-rss"),
        schema.name("Max RSS"),
        schema.description("Maximum resident set size"),
    ]

    bogo_ops: typing.Annotated[
        int,
        schema.id("bogo-ops"),
        schema.name("Bogus Operations"),
        schema.description("Number of stressor loop iterations"),
    ]

    bogo_ops_per_second_usr_sys_time: typing.Annotated[
        float,
        schema.id("bogo-ops-per-second-usr-sys-time"),
        schema.name("Bogus operations per second per user and sys time"),
        schema.description(
            "is the bogo-ops rate divided by the user + system time."
            "This is the real per CPU throughput "
            "taking into consideration "
            "all the CPUs used and all the time consumed "
            "by the stressor and kernel time."
        ),
    ]

    bogo_ops_per_second_real_time: typing.Annotated[
        float,
        schema.id("bogo-ops-per-second-real-time"),
        schema.name("Bogus operations per second in real time"),
        schema.description(
            "real time measurement is how long the run took based "
            "on the wall clock time "
            "(that is, the time the stressor took to run)."
        ),
    ]

    wall_clock_time: typing.Annotated[
        float,
        schema.id("wall-clock-time"),
        schema.name("Wall Clock Time"),
        schema.description("The time the stressor took to run"),
    ]

    user_time: typing.Annotated[
        float,
        schema.id("user-time"),
        schema.name("CPU User Time"),
        schema.description("The CPU time spent in user space"),
    ]

    system_time: typing.Annotated[
        float,
        schema.id("system-time"),
        schema.name("CPU System Time"),
        schema.description("The CPU time spent in kernel space"),
    ]

    cpu_usage_per_instance: typing.Annotated[
        float,
        schema.id("cpu-usage-per-instance"),
        schema.name("CPU usage per instance"),
        schema.description("is the amount of CPU used by each stressor instance"),
    ]


@dataclass
class VMOutput(CommonOutput):
    """
    This is the data structure that holds the results for the VM stressor
    """


vm_output_schema = plugin.build_object_schema(VMOutput)


@dataclass
class CPUOutput(CommonOutput):
    """
    This is the data structure that holds the results for the CPU stressor
    """


cpu_output_schema = plugin.build_object_schema(CPUOutput)


@dataclass
class MatrixOutput(CommonOutput):
    """
    This is the data structure that holds the results for the Matrix stressor
    """


matrix_output_schema = plugin.build_object_schema(MatrixOutput)


@dataclass
class MQOutput(CommonOutput):
    """
    This is the data structure that holds the results for the MQ stressor
    """


mq_output_schema = plugin.build_object_schema(MQOutput)


@dataclass
class HDDOutput(CommonOutput):
    """
    This is the data structure that holds the results for the HDD stressor
    """


hdd_output_schema = plugin.build_object_schema(HDDOutput)


@dataclass
class WorkloadResults:
    systeminfo: typing.Annotated[
        SystemInfoOutput,
        schema.name("System Info"),
        schema.description("System info output object"),
    ]

    vminfo: typing.Annotated[
        typing.Optional[VMOutput],
        schema.name("VM Output"),
        schema.description("VM stressor output object"),
    ] = None

    cpuinfo: typing.Annotated[
        typing.Optional[CPUOutput],
        schema.name("CPU Output"),
        schema.description("CPU stressor output object"),
    ] = None

    matrixinfo: typing.Annotated[
        typing.Optional[MatrixOutput],
        schema.name("Matrix Output"),
        schema.description("Matrix stressor output object"),
    ] = None

    mqinfo: typing.Annotated[
        typing.Optional[MQOutput],
        schema.name("MQ Output"),
        schema.description("MQ stressor output object"),
    ] = None

    hddinfo: typing.Annotated[
        typing.Optional[HDDOutput],
        schema.name("HDD Output"),
        schema.description("HDD stressor output object"),
    ] = None


@dataclass
class WorkloadError:
    error: str
