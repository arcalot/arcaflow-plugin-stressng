#!/usr/bin/env python3

import typing
import enum
import dataclasses
from dataclasses import dataclass, field

from arcaflow_plugin_sdk import plugin
from arcaflow_plugin_sdk import annotations


class Stressors(enum.Enum):
    CPU = "cpu"
    VM = "vm"
    MATRIX = "matrix"
    MQ = "mq"
    HDD = "hdd"


@dataclass
class CpuStressorParams:
    """
    The parameters for the CPU stressor
    """

    stressor: str
    cpu_count: int = field(
        metadata={
            "name": "CPU count",
            "description": "Number of CPU cores to be used (0 means all)",
        }
    )
    cpu_method: typing.Optional[str] = field(
        default="all",
        metadata={
            "name": "CPU stressor method",
            "description": (
                "fine grained control of which "
                "cpu stressors to use (ackermann, "
                "cfloat etc."
            ),
        },
    )

    cpu_load: typing.Optional[int] = field(
        default=None,
        metadata={
            "name": "CPU load",
            "description": "load CPU by percentage",
        },
    )

    def to_jobfile(self) -> str:
        result = "cpu {}\n".format(self.cpu_count)
        if self.cpu_method is not None:
            result = result + "cpu-method {}\n".format(self.cpu_method)
        if self.cpu_load is not None:
            result = result + "cpu-load {}\n".format(self.cpu_load)
        return result


@dataclass
class VmStressorParams:
    """
    The parameters for the vm (virtual memory) stressor
    vm: number of virtual-memory stressors
    vm_bytes: amount of vm stressor memory
    """

    stressor: str
    vm: int = field(
        metadata={
            "name": "VM count",
            "description": (
                "Number of VM stressors to be "
                "run (0 means 1 stressor per CPU"
            ),
        }
    )
    vm_bytes: str = field(
        metadata={
            "name": "VM memory",
            "description": "Amount of memory a single VM stressor will use",
        }
    )

    mmap: typing.Optional[str] = field(
        default=None,
        metadata={
            "name": "mmap",
            "description": "Number of stressors per CPU",
        },
    )
    mmap_bytes: typing.Optional[str] = field(
        default=None, metadata={"name": "Allocation of memory per stressor"}
    )

    def to_jobfile(self) -> str:
        vm = "vm {}\n".format(self.vm)
        vm_bytes = "vm-bytes {}\n".format(self.vm_bytes)
        result = vm + vm_bytes
        if self.mmap is not None:
            result = result + "mmap {}\n".format(self.mmap)
        if self.mmap_bytes is not None:
            result = result + "mmap-bytes {}\n".format(self.mmap_bytes)
        return result


@dataclass
class MatrixStressorParams:
    """
    This is the data structure that holds the results for the Matrix stressor.
    This stressor is a good way to exercise the CPU floating point operations
    as well as memory and processor data cache
    """

    stressor: str
    matrix: int = field(
        metadata={
            "name": "Matrix count",
            "description": (
                "Number of Matrix stressors to be "
                "run (0 means 1 stressor per CPU"
            ),
        }
    )

    def to_jobfile(self) -> str:
        matrix = "matrix {}\n".format(self.matrix)
        result = matrix
        return result


@dataclass
class MqStressorParams:
    """
    This is the data structure that holds the results for the MQ stressor
    """

    stressor: str
    mq: int = field(
        metadata={
            "name": "MQ count",
            "description": (
                "Number of MQ stressors to be run "
                "(0 means 1 stressor per CPU)"
            ),
        }
    )

    def to_jobfile(self) -> str:
        mq = "mq {}\n".format(self.mq)
        result = mq
        return result


@dataclass
class HDDStressorParams:
    stressor: str
    hdd: int = field(
        metadata={
            "name": "HDD workers",
            "description": (
                "start N workers continually writing, "
                "reading and removing temporary files"
            ),
        }
    )

    hdd_bytes: str = field(
        metadata={
            "name": "Bytes per worker",
            "description": (
                "write  N  bytes for each hdd process, the default is 1 GB. "
                "One can specify the size in units of Bytes, KBytes, "
                "MBytes and GBytes using the suffix b, k, m or g."
            ),
        }
    )

    hdd_write_size: str = field(
        metadata={
            "name": "Write Size",
            "description": (
                "specify size of each write "
                "in bytes. Size can be from 1 byte to 4MB"
                "One can specify the size in units of Bytes, KBytes, "
                "MBytes using the suffix b, k, m"
            ),
        }
    )

    def to_jobfile(self) -> str:
        hdd = "hdd {}\n".format(self.hdd)
        hdd_bytes = "hdd-bytes {}\n".format(self.hdd_bytes)
        hdd_write_size = "hdd-write-size {}\n".format(self.hdd_write_size)
        result = hdd + hdd_bytes + hdd_write_size
        return result


@dataclass
class StressNGParams:
    """
    The parameters in this schema will be passed through to the stressng
    command unchanged
    """

    timeout: str = field(
        metadata={
            "name": "Runtime",
            "description": "Time to run the benchmark test",
        }
    )

    items: typing.List[
        typing.Annotated[
            typing.Union[
                typing.Annotated[
                    CpuStressorParams, annotations.discriminator_value("cpu")
                ],
                typing.Annotated[
                    VmStressorParams, annotations.discriminator_value("vm")
                ],
                typing.Annotated[
                    MatrixStressorParams,
                    annotations.discriminator_value("matrix"),
                ],
                typing.Annotated[
                    MqStressorParams, annotations.discriminator_value("mq")
                ],
                typing.Annotated[
                    HDDStressorParams, annotations.discriminator_value("hdd")
                ],
            ],
            annotations.discriminator("stressor"),
        ]
    ]
    verbose: typing.Optional[bool] = field(
        default=None,
        metadata={"name": "verbose", "description": "verbose output"},
    )
    metrics_brief: typing.Optional[bool] = field(
        default=None,
        metadata={
            "name": "brief metrics",
            "description": "Brief version of the metrics output",
        },
    )

    workdir: typing.Optional[str] = field(
        default=None,
        metadata={
            "name": "Working Dir",
            "description": (
                "Path were stress-ng will be "
                "executed (example to target a specific volume)"
            ),
        },
    )

    def to_jobfile(self) -> str:
        result = "timeout {}\n".format(self.timeout)
        if self.verbose is not None:
            result = result + "verbose {}\n".format(self.verbose)
        if self.metrics_brief is not None:
            result = result + "metrics-brief {}\n".format(self.metrics_brief)
        return result


@dataclass
class WorkloadParams:
    """
    This is the data structure for the input parameters of the step
    defined below
    """

    StressNGParams: StressNGParams
    cleanup: bool = field(
        metadata={
            "name": "Cleanup",
            "description": "Cleanup after the benchmark run",
        }
    )


@dataclass
class SystemInfoOutput:
    """
    This is the data structure that holds the generic info for the
    tested system
    """

    stress_ng_version: str = dataclasses.field(
        metadata={
            "id": "stress-ng-version",
            "name": "stress_ng_version",
            "description": "version of the stressng tool used",
        }
    )
    run_by: str = dataclasses.field(
        metadata={
            "id": "run-by",
            "name": "run_by",
            "description": "username of the person who ran the test",
        }
    )
    date: str = dataclasses.field(
        metadata={
            "id": "date-yyyy-mm-dd",
            "name": "data",
            "description": "date on which the test was run",
        }
    )
    time: str = dataclasses.field(
        metadata={
            "id": "time-hh-mm-ss",
            "name": "time",
            "description": "time at which the test was run",
        }
    )
    epoch: int = dataclasses.field(
        metadata={
            "id": "epoch-secs",
            "name": "epoch",
            "description": "epoch at which the test was run",
        }
    )
    hostname: str = field(
        metadata={
            "name": "hostname",
            "description": "host on which the test was run",
        }
    )
    sysname: str = field(
        metadata={"name": "system name", "description": "System name"}
    )
    nodename: str = field(
        metadata={
            "name": "nodename",
            "description": "name of the node on which the test was run",
        }
    )
    release: str = field(
        metadata={
            "name": "release",
            "description": "kernel release on which the test was run",
        }
    )
    version: str = field(
        metadata={
            "name": "version",
            "description": "version on which the test was run",
        }
    )
    machine: str = field(
        metadata={
            "name": "machine",
            "description": "machine type on which the test was run",
        }
    )
    uptime: int = field(
        metadata={
            "name": "uptime",
            "description": "uptime of the machine the test was run on",
        }
    )
    totalram: int = field(
        metadata={
            "name": "totalram",
            "description": "total amount of RAM the test machine had",
        }
    )
    freeram: int = field(
        metadata={
            "name": "freeram",
            "description": "amount of free RAM the test machine had",
        }
    )
    sharedram: int = field(
        metadata={
            "name": "sharedram",
            "description": "amount of shared RAM the test machine had",
        }
    )
    bufferram: int = field(
        metadata={
            "name": "bufferram",
            "description": "amount of buffer RAM the test machine had",
        }
    )
    totalswap: int = field(
        metadata={
            "name": "totalswap",
            "description": "total amount of swap the test machine had",
        }
    )
    freeswap: int = field(
        metadata={
            "name": "bufferram",
            "description": "amount of free swap the test machine had",
        }
    )
    pagesize: int = field(
        metadata={
            "name": "pagesize",
            "description": "memory page size the test machine used",
        }
    )
    cpus: int = field(
        metadata={
            "name": "cpus",
            "description": "number of CPU cores the test machine had",
        }
    )
    cpus_online: int = dataclasses.field(
        metadata={
            "id": "cpus-online",
            "name": "cpus_online",
            "description": "number of online CPUs the test machine had",
        }
    )
    ticks_per_second: int = dataclasses.field(
        metadata={
            "id": "ticks-per-second",
            "name": "ticks_per_second",
            "description": "ticks per second used on the test machine",
        }
    )


system_info_output_schema = plugin.build_object_schema(SystemInfoOutput)


@dataclass
class VMOutput:
    """
    This is the data structure that holds the results for the VM stressor
    """

    stressor: str
    bogo_ops: int = dataclasses.field(metadata={"id": "bogo-ops"})
    bogo_ops_per_second_usr_sys_time: float = dataclasses.field(
        metadata={"id": "bogo-ops-per-second-usr-sys-time"}
    )
    bogo_ops_per_second_real_time: float = dataclasses.field(
        metadata={"id": "bogo-ops-per-second-real-time"}
    )
    wall_clock_time: float = dataclasses.field(
        metadata={"id": "wall-clock-time"}
    )
    user_time: float = dataclasses.field(metadata={"id": "user-time"})
    system_time: float = dataclasses.field(metadata={"id": "system-time"})
    cpu_usage_per_instance: float = dataclasses.field(
        metadata={"id": "cpu-usage-per-instance"}
    )


vm_output_schema = plugin.build_object_schema(VMOutput)


@dataclass
class CPUOutput:
    """
    This is the data structure that holds the results for the CPU stressor
    """

    stressor: str
    bogo_ops: int = dataclasses.field(metadata={"id": "bogo-ops"})
    bogo_ops_per_second_usr_sys_time: float = dataclasses.field(
        metadata={
            "id": "bogo-ops-per-second-usr-sys-time",
            "name": "Bogus operations per second per user and sys time",
            "description": (
                "is the bogo-ops rate divided by the user + system time."
                "This is the real per CPU throughput "
                "taking into consideration "
                "all the CPUs used and all the time consumed "
                "by the stressor and kernel time."
            ),
        }
    )
    bogo_ops_per_second_real_time: float = dataclasses.field(
        metadata={
            "id": "bogo-ops-per-second-real-time",
            "name": "Bogus operations per second in real time",
            "description": (
                "real time measurement is how long the run took based "
                "on the wall clock time "
                "(that is, the time the stressor took to run)."
            ),
        }
    )
    wall_clock_time: float = dataclasses.field(
        metadata={
            "id": "wall-clock-time",
            "name": "Wall clock time",
            "description": "the time the stressor took to run",
        }
    )
    user_time: float = dataclasses.field(metadata={"id": "user-time"})
    system_time: float = dataclasses.field(metadata={"id": "system-time"})
    cpu_usage_per_instance: float = dataclasses.field(
        metadata={
            "id": "cpu-usage-per-instance",
            "name": "CPU usage per instance",
            "description": (
                "is the amount of CPU " "used by each stressor instance"
            ),
        }
    )


cpu_output_schema = plugin.build_object_schema(CPUOutput)


@dataclass
class MatrixOutput:
    """
    This is the data structure that holds the results for the Matrix stressor
    """

    stressor: str
    bogo_ops: int = dataclasses.field(metadata={"id": "bogo-ops"})
    bogo_ops_per_second_usr_sys_time: float = dataclasses.field(
        metadata={
            "id": "bogo-ops-per-second-usr-sys-time",
            "name": "Bogus operations per second per user and sys time",
            "description": (
                "is the bogo-ops rate divided by the user + system time."
                "This is the real per CPU "
                "throughput taking into consideration "
                "all the CPUs used and all the time consumed "
                "by the stressor and kernel time."
            ),
        }
    )
    bogo_ops_per_second_real_time: float = dataclasses.field(
        metadata={
            "id": "bogo-ops-per-second-real-time",
            "name": "Bogus operations per second in real time",
            "description": (
                "real time measurement is how long the run took based "
                "on the wall clock time "
                "(that is, the time the stressor took to run)."
            ),
        }
    )
    wall_clock_time: float = dataclasses.field(
        metadata={
            "id": "wall-clock-time",
            "name": "Wall clock time",
            "description": "the time the stressor took to run",
        }
    )
    user_time: float = dataclasses.field(
        metadata={
            "id": "user-time",
            "name": "user time",
            "description": (
                "is the amount of CPU used running as a normal user process."
                "Note with 4 CPUs this is about 4 x the wall clock time "
                "(since no sys time is being used)."
            ),
        }
    )
    system_time: float = dataclasses.field(
        metadata={
            "id": "system-time",
            "name": "system tyme",
            "description": (
                "measurement is the amount of CPU used in the kernel"
            ),
        }
    )
    cpu_usage_per_instance: float = dataclasses.field(
        metadata={
            "id": "cpu-usage-per-instance",
            "name": "CPU usage per instance",
            "description": (
                "is the amount of CPU used by each stressor instance"
            ),
        }
    )


matrix_output_schema = plugin.build_object_schema(MatrixOutput)


@dataclass
class MQOutput:
    """
    This is the data structure that holds the results for the MQ stressor
    """

    stressor: str
    bogo_ops: int = dataclasses.field(metadata={"id": "bogo-ops"})
    bogo_ops_per_second_usr_sys_time: float = dataclasses.field(
        metadata={
            "id": "bogo-ops-per-second-usr-sys-time",
            "name": "Bogus operations per second per user and sys time",
            "description": (
                "is the bogo-ops rate divided by the user + system time."
                "This is the real per CPU "
                "throughput taking into consideration "
                "all the CPUs used and all the time consumed "
                "by the stressor and kernel time."
            ),
        }
    )
    bogo_ops_per_second_real_time: float = dataclasses.field(
        metadata={
            "id": "bogo-ops-per-second-real-time",
            "name": "Bogus operations per second in real time",
            "description": (
                "real time measurement is how long the run took based "
                "on the wall clock time "
                "(that is, the time the stressor took to run)."
            ),
        }
    )
    wall_clock_time: float = dataclasses.field(
        metadata={
            "id": "wall-clock-time",
            "name": "Wall clock time",
            "description": "the time the stressor took to run",
        }
    )
    user_time: float = dataclasses.field(
        metadata={
            "id": "user-time",
            "name": "user time",
            "description": (
                "is the amount of CPU used running as a normal user process."
                "Note with 4 CPUs this is about 4 x the wall clock time "
                "(since no sys time is being used)."
            ),
        }
    )
    system_time: float = dataclasses.field(
        metadata={
            "id": "system-time",
            "name": "system tyme",
            "description": (
                "measurement is the amount of CPU used in the kernel"
            ),
        }
    )
    cpu_usage_per_instance: float = dataclasses.field(
        metadata={
            "id": "cpu-usage-per-instance",
            "name": "CPU usage per instance",
            "description": (
                "is the amount of CPU used by each stressor instance"
            ),
        }
    )


mq_output_schema = plugin.build_object_schema(MQOutput)


@dataclass
class HDDOutput:
    """
    This is the data structure that holds the results for the HDD stressor
    """

    stressor: str
    bogo_ops: int = dataclasses.field(metadata={"id": "bogo-ops"})
    bogo_ops_per_second_usr_sys_time: float = dataclasses.field(
        metadata={
            "id": "bogo-ops-per-second-usr-sys-time",
            "name": "Bogus operations per second per user and sys time",
            "description": (
                "is the bogo-ops rate divided by the user + system time."
                "This is the real per CPU throughput "
                "taking into consideration "
                "all the CPUs used and all the time consumed "
                "by the stressor and kernel time."
            ),
        }
    )
    bogo_ops_per_second_real_time: float = dataclasses.field(
        metadata={
            "id": "bogo-ops-per-second-real-time",
            "name": "Bogus operations per second in real time",
            "description": (
                "real time measurement is how long the run took based "
                "on the wall clock time "
                "(that is, the time the stressor took to run)."
            ),
        }
    )
    wall_clock_time: float = dataclasses.field(
        metadata={
            "id": "wall-clock-time",
            "name": "Wall clock time",
            "description": "the time the stressor took to run",
        }
    )
    user_time: float = dataclasses.field(
        metadata={
            "id": "user-time",
            "name": "user time",
            "description": (
                "is the amount of CPU used running as a normal user process."
                "Note with 4 CPUs this is about 4 x the wall clock time "
                "(since no sys time is being used)."
            ),
        }
    )
    system_time: float = dataclasses.field(
        metadata={
            "id": "system-time",
            "name": "system tyme",
            "description": (
                "measurement is the amount of CPU used in the kernel"
            ),
        }
    )
    cpu_usage_per_instance: float = dataclasses.field(
        metadata={
            "id": "cpu-usage-per-instance",
            "name": "CPU usage per instance",
            "description": (
                "is the amount of CPU used by each stressor instance"
            ),
        }
    )


hdd_output_schema = plugin.build_object_schema(HDDOutput)


@dataclass
class WorkloadResults:
    """
    This is the output data structure for the success case
    """

    systeminfo: SystemInfoOutput
    vminfo: typing.Optional[VMOutput] = None
    cpuinfo: typing.Optional[CPUOutput] = None
    matrixinfo: typing.Optional[MatrixOutput] = None
    mqinfo: typing.Optional[MQOutput] = None
    hddinfo: typing.Optional[HDDOutput] = None


@dataclass
class WorkloadError:
    """
    This is the output data structure for the failure case
    """

    error: str
