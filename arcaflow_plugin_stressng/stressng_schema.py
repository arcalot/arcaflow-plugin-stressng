#!/usr/bin/env python3

import typing
import enum
from dataclasses import dataclass

from arcaflow_plugin_sdk import plugin, schema
from arcaflow_plugin_sdk import annotations


class Stressors(str, enum.Enum):
    CPU = "cpu"
    VM = "vm"
    MMAP = "mmap"
    MATRIX = "matrix"
    MQ = "mq"
    HDD = "hdd"


class CpuMethod(str, enum.Enum):
    ALL = "all"
    ACKERMANN = "ackermann"
    APERY = "apery"
    BITOPS = "bitops"
    CALLFUNC = "callfunc"
    CFLOAT = "cfloat"
    CDOUBLE = "cdouble"
    CLONGDOUBLE = "clongdouble"
    COLLATZ = "collatz"
    CORRELATE = "correlate"
    CPUID = "cpuid"
    CRC16 = "crc16"
    DECIMAL32 = "decimal32"
    DECIMAL64 = "decimal64"
    DECIMAL128 = "decimal128"
    DITHER = "dither"
    DIV64 = "div64"
    DJB2A = "djb2a"
    DOUBLE = "double"
    EULER = "euler"
    EXPLOG = "explog"
    FACTORIAL = "factorial"
    FIBONACCI = "fibonacci"
    FFT = "fft"
    FLETCHER16 = "fletcher16"
    FLOAT = "float"
    FLOAT16 = "float16"
    FLOAT32 = "float32"
    FLOAT80 = "float80"
    FLOAT128 = "float128"
    FLOATCONVERSION = "floatconversion"
    FNV1A = "fnv1a"
    GAMMA = "gamma"
    GCD = "gcd"
    GRAY = "gray"
    HAMMING = "hamming"
    HANOI = "hanoi"
    HYPERBOLIC = "hyperbolic"
    IDCT = "idct"
    INT8 = "int8"
    INT16 = "int16"
    INT32 = "int32"
    INT64 = "int64"
    INT128 = "int128"
    INT32FLOAT = "int32float"
    INT32DOUBLE = "int32double"
    INT32LONGDOUBLE = "int32longdouble"
    INT64FLOAT = "int64float"
    INT64DOUBLE = "int64double"
    INT64LONGDOUBLE = "int64longdouble"
    INT128FLOAT = "int128float"
    INT128DOUBLE = "int128double"
    INT128LONGDOUBLE = "int128longdouble"
    INT128DECIMAL32 = "int128decimal32"
    INT128DECIMAL64 = "int128decimal64"
    INT128DECIMAL128 = "int128decimal128"
    INTCONVERSION = "intconversion"
    IPV4CHECKSUM = "ipv4checksum"
    JENKIN = "jenkin"
    JMP = "jmp"
    LN2 = "ln2"
    LONGDOUBLE = "longdouble"
    LOOP = "loop"
    MATRIXPROD = "matrixprod"
    MURMUR3_32 = "murmur3_32"
    NHASH = "nhash"
    NSQRT = "nsqrt"
    OMEGA = "omega"
    PARITY = "parity"
    PHI = "phi"
    PI = "pi"
    PJW = "pjw"
    PRIME = "prime"
    PSI = "psi"
    QUEENS = "queens"
    RAND = "rand"
    RAND48 = "rand48"
    RGB = "rgb"
    SDBM = "sdbm"
    SIEVE = "sieve"
    STATS = "stats"
    SQRT = "sqrt"
    TRIG = "trig"
    UNION = "union"
    ZETA = "zeta"


class MatrixMethod(str, enum.Enum):
    ALL = "all"
    ADD = "add"
    COPY = "copy"
    DIV = "div"
    FROBENIUS = "frobenius"
    HADAMARD = "hadamard"
    IDENTITY = "identity"
    MEAN = "mean"
    MULT = "mult"
    NEGATE = "negate"
    PROD = "prod"
    SUB = "sub"
    SQUARE = "square"
    TRANS = "trans"
    ZERO = "zero"


class VmMethod(str, enum.Enum):
    ALL = "all"
    FLIP = "flip"
    GALPAT_0 = "galpat-0"
    GALPAT_1 = "galpat-1"
    GRAY = "gray"
    INCDEC = "incdec"
    INC_NYBBLE = "inc-nybble"
    RAND_SET = "rand-set"
    RAND_SUM = "rand-sum"
    READ64 = "read64"
    ROR = "ror"
    SWAP = "swap"
    MOVE_INV = "move-inv"
    MODULO_X = "modulo-x"
    PRIME_0 = "prime-0"
    PRIME_1 = "prime-1"
    PRIME_GRAY_0 = "prime-gray-0"
    PRIME_GRAY_1 = "prime-gray-1"
    ROWHAMMER = "rowhammer"
    WALK_0D = "walk-0d"
    WALK_1D = "walk-1d"
    WALK_0A = "walk-0a"
    WALK_1A = "walk-1a"
    WRITE64 = "write64"
    ZERO_ONE = "zero-one"


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
    cpu_ops: typing.Annotated[
        typing.Optional[int],
        schema.id("cpu-ops"),
        schema.name("CPU Operations"),
        schema.description("Stop CPU stress workers after N bogo operations"),
    ] = None

    cpu_load: typing.Annotated[
        typing.Optional[int],
        schema.id("cpu-load"),
        schema.name("CPU Load"),
        schema.description(
            "Load CPU with P percent loading for the CPU stress workers"
        ),
    ] = None

    cpu_method: typing.Annotated[
        typing.Optional[CpuMethod],
        schema.id("cpu-method"),
        schema.name("CPU Stressor Method"),
        schema.description(
            "Specify a cpu stress method; by default, all stress methods "
            "are exercised sequentially"
        ),
    ] = CpuMethod.ALL


    def to_jobfile(self) -> str:
        result = f"cpu {self.workers}\n"
        if self.cpu_ops is not None:
            result += f"cpu-ops {self.cpu_ops}\n"
        if self.cpu_load is not None:
            result += f"cpu-load {self.cpu_load}\n"
        if self.cpu_method is not None:
            result += f"cpu-method {CpuMethod(self.cpu_method)}\n"
        return result


@dataclass
class VmStressorParams(CommonStressorParams):
    vm_bytes: typing.Annotated[
        typing.Optional[str],
        schema.id("vm-bytes"),
        schema.name("VM Memory Bytes"),
        schema.description("mmap N bytes per vm worker, the default is 256MB"),
    ] = None

    vm_ops: typing.Annotated[
        typing.Optional[int],
        schema.id("vm-ops"),
        schema.name("VM Operations"),
        schema.description("Stop vm workers after N bogo operations"),
    ] = None

    vm_hang: typing.Annotated[
        typing.Optional[int],
        schema.id("vm-hang"),
        schema.name("VM Hang"),
        schema.description(
            "Sleep N seconds before unmapping memory, the default is zero seconds"
        ),
    ] = None

    vm_keep: typing.Annotated[
        typing.Optional[bool],
        schema.id("vm-keep"),
        schema.name("VM Keep"),
        schema.description(
            "Do not continually unmap and map memory, just keep on re-writing to it"
        ),
    ] = None

    vm_locked: typing.Annotated[
        typing.Optional[bool],
        schema.id("vm-locked"),
        schema.name("VM Locked"),
        schema.description(
            "Lock the pages of the mapped region into memory using mmap "
            "MAP_LOCKED (since Linux 2.5.37)"
        ),
    ] = None

    vm_method: typing.Annotated[
        typing.Optional[VmMethod],
        schema.id("vm-method"),
        schema.name("VM Method"),
        schema.description(
            "Specify a vm stress method; by default, all the stress methods "
            "are exercised sequentially"
        ),
    ] = VmMethod.ALL

    vm_populate: typing.Annotated[
        typing.Optional[bool],
        schema.id("vm-populate"),
        schema.name("VM Populate"),
        schema.description(
            "populate (prefault) page tables for the memory mappings; "
            "this can stress swapping"
        ),
    ] = None

    def to_jobfile(self) -> str:
        result = f"vm {self.workers}\n"
        if self.vm_bytes is not None:
            result += f"vm-bytes {self.vm_bytes}\n"
        if self.vm_ops is not None:
            result += f"vm-ops {self.vm_ops}\n"
        if self.vm_hang is not None:
            result += f"vm-hang {self.vm_hang}\n"
        if self.vm_keep is True:
            result += "vm-keep\n"
        if self.vm_locked is True:
            result += "vm-locked\n"
        if self.vm_method is not None:
            result += f"vm-method {VmMethod(self.vm_method)}\n"
        if self.vm_populate is True:
            result += "vm-populate\n"
        return result


@dataclass
class MmapStressorParams(CommonStressorParams):
    mmap_ops: typing.Annotated[
        typing.Optional[int],
        schema.id("mmap-ops"),
        schema.name("Mmap Operations"),
        schema.description("Stop mmap stress workers after N bogo operations"),
    ] = None

    mmap_async: typing.Annotated[
        typing.Optional[bool],
        schema.id("mmap-async"),
        schema.name("Mmap Async"),
        schema.description(
            "Enable file based memory mapping and use asynchronous msync'ing on each page"
        ),
    ] = None

    mmap_bytes: typing.Annotated[
        typing.Optional[str],
        schema.id("mmap-bytes"),
        schema.name("Mmap Bytes"),
        schema.description(
            "allocate N bytes per mmap stress worker, the default is 256MB"
        ),
    ] = None

    mmap_file: typing.Annotated[
        typing.Optional[bool],
        schema.id("mmap-file"),
        schema.name("Mmap File"),
        schema.description(
            "Enable file based memory mapping and by default use synchronous "
            "msync'ing on each page"
        ),
    ] = None

    mmap_mmap2: typing.Annotated[
        typing.Optional[bool],
        schema.id("mmap-mmap2"),
        schema.name("Mmap mmap2"),
        schema.description(
            "Use mmap2 for 4K page aligned offsets if mmap2 is available, "
            "otherwise fall back to mmap"
        ),
    ] = None

    mmap_mprotect: typing.Annotated[
        typing.Optional[bool],
        schema.id("mmap-mprotect"),
        schema.name("Mmap mprotect"),
        schema.description(
            "Change protection settings on each page of memory; Each time "
            "a page or a group of pages are mapped or remapped then this "
            "option will make the pages read-only, write-only, exec-only, "
            "and read-write"
        ),
    ] = None

    mmap_odirect: typing.Annotated[
        typing.Optional[bool],
        schema.id("mmap-odirect"),
        schema.name("Mmap odirect"),
        schema.description(
            "Enable file based memory mapping and use O_DIRECT direct I/O"
        ),
    ] = None

    mmap_osync: typing.Annotated[
        typing.Optional[bool],
        schema.id("mmap-osync"),
        schema.name("Mmap osync"),
        schema.description(
            "Enable file based memory mapping and used O_SYNC synchronous "
            "I/O integrity completion"
        ),
    ] = None

    def to_jobfile(self) -> str:
        result = f"mmap {self.workers}\n"
        if self.mmap_ops is not None:
            result += f"mmap-ops {self.mmap_ops}\n"
        if self.mmap_async is True:
            result += "mmap-async\n"
        if self.mmap_bytes is not None:
            result += f"mmap-bytes {self.mmap_bytes}\n"
        if self.mmap_file is True:
            result += "mmap-file\n"
        if self.mmap_mmap2 is True:
            result += "mmap-mmap2\n"
        if self.mmap_mprotect is True:
            result += "mmap-mprotect\n"
        if self.mmap_odirect is True:
            result += "mmap-odirect\n"
        if self.mmap_osync is True:
            result += "mmap-osync\n"
        return result


@dataclass
class MatrixStressorParams(CommonStressorParams):
    matrix_method: typing.Annotated[
        typing.Optional[MatrixMethod],
        schema.id("matrix-method"),
        schema.name("Matrix Stressor Method"),
        schema.description(
            "Fine grained control of which matrix stressors to use (add, copy, etc.)"
        ),
    ] = MatrixMethod.ALL

    def to_jobfile(self) -> str:
        result = f"matrix {self.workers}\n"
        if self.matrix_method is not None:
            result += f"matrix-method {self.matrix_method}\n"
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
                    MmapStressorParams,
                    annotations.discriminator_value("mmap"),
                    schema.name("Mmap Stressor Parameters"),
                    schema.description("Parameters for running the mmap stressor"),
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
            annotations.discriminator("stressor", discriminator_inlined=True),
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

    compiler: typing.Annotated[
        str,
        schema.name("compiler"),
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
        schema.description("The amount of CPU used by each stressor instance"),
    ]


@dataclass
class VMOutput(CommonOutput):
    """
    This is the data structure that holds the results for the VM stressor
    """


vm_output_schema = plugin.build_object_schema(VMOutput)


@dataclass
class MmapOutput(CommonOutput):
    """
    This is the data structure that holds the results for the mmap stressor
    """


mmap_output_schema = plugin.build_object_schema(MmapOutput)


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

    add_matrix_ops_per_sec: typing.Annotated[
        float,
        schema.id("add-matrix-ops-per-sec"),
        schema.name("Add matrix operations per second"),
    ]

    copy_matrix_ops_per_sec: typing.Annotated[
        float,
        schema.id("copy-matrix-ops-per-sec"),
        schema.name("Copy matrix operations per second"),
    ]

    div_matrix_ops_per_sec: typing.Annotated[
        float,
        schema.id("div-matrix-ops-per-sec"),
        schema.name("Div matrix operations per second"),
    ]

    frobenius_matrix_ops_per_sec: typing.Annotated[
        float,
        schema.id("frobenius-matrix-ops-per-sec"),
        schema.name("Frobenius matrix operations per second"),
    ]

    hadamard_matrix_ops_per_sec: typing.Annotated[
        float,
        schema.id("hadamard-matrix-ops-per-sec"),
        schema.name("Hadamard matrix operations per second"),
    ]

    identity_matrix_ops_per_sec: typing.Annotated[
        float,
        schema.id("identity-matrix-ops-per-sec"),
        schema.name("Identity matrix operations per second"),
    ]

    mean_matrix_ops_per_sec: typing.Annotated[
        float,
        schema.id("mean-matrix-ops-per-sec"),
        schema.name("Mean matrix operations per second"),
    ]

    mult_matrix_ops_per_sec: typing.Annotated[
        float,
        schema.id("mult-matrix-ops-per-sec"),
        schema.name("Mult matrix operations per second"),
    ]

    negate_matrix_ops_per_sec: typing.Annotated[
        float,
        schema.id("negate-matrix-ops-per-sec"),
        schema.name("Negate matrix operations per second"),
    ]

    prod_matrix_ops_per_sec: typing.Annotated[
        float,
        schema.id("prod-matrix-ops-per-sec"),
        schema.name("Prod matrix operations per second"),
    ]

    sub_matrix_ops_per_sec: typing.Annotated[
        float,
        schema.id("sub-matrix-ops-per-sec"),
        schema.name("Sub matrix operations per second"),
    ]

    square_matrix_ops_per_sec: typing.Annotated[
        float,
        schema.id("square-matrix-ops-per-sec"),
        schema.name("Square matrix operations per second"),
    ]

    trans_matrix_ops_per_sec: typing.Annotated[
        float,
        schema.id("trans-matrix-ops-per-sec"),
        schema.name("Trans matrix operations per second"),
    ]

    zero_matrix_ops_per_sec: typing.Annotated[
        float,
        schema.id("zero-matrix-ops-per-sec"),
        schema.name("Zero matrix operations per second"),
    ]


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

    mbsec_read_rate: typing.Annotated[
        float,
        schema.id("mbsec-read-rate"),
        schema.name("Read rate in MB/s"),
    ]

    mbsec_write_rate: typing.Annotated[
        float,
        schema.id("mbsec-write-rate"),
        schema.name("Write rate in MB/s"),
    ]

    mbsec_readwrite_combined_rate: typing.Annotated[
        float,
        schema.id("mbsec-readwrite-combined-rate"),
        schema.name("Read-write combined rate in MB/s"),
    ]


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

    mmapinfo: typing.Annotated[
        typing.Optional[MmapOutput],
        schema.name("Mmap Output"),
        schema.description("mmap stressor output object"),
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
