#!/usr/bin/env python3

import typing
import enum
from dataclasses import dataclass

from arcaflow_plugin_sdk import plugin, schema
from arcaflow_plugin_sdk import annotations


def params_to_jobfile(params: dict) -> str:
    result = ""
    for key, value in params.items():
        if not value:
            continue
        if isinstance(value, bool):
            result += f"{key}\n"
        elif isinstance(value, list):
            result += f"{key} {','.join(value)}\n"
        else:
            result += f"{key} {value}\n"
    return result


class Stressors(str, enum.Enum):
    CPU = "cpu"
    VM = "vm"
    MMAP = "mmap"
    MATRIX = "matrix"
    MQ = "mq"
    HDD = "hdd"
    IOMIX = "iomix"
    SOCK = "sock"


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


class HddOpts(str, enum.Enum):
    DIRECT = "direct"
    DSYNC = "dsync"
    FADV_DONTNEED = "fadv-dontneed"
    FADV_NOREUSE = "fadv-noreuse"
    FADV_NORMAL = "fadv-normal"
    FADV_RND = "fadv-rnd"
    FADV_SEQ = "fadv-seq"
    FADV_WILLNEED = "fadv-willneed"
    FSYNC = "fsync"
    FDATASYNC = "fdatasync"
    IOVEC = "iovec"
    NOATIME = "noatime"
    SYNC = "sync"
    RD_RND = "rd-rnd"
    RD_SEQ = "rd-seq"
    SYNCFS = "syncfs"
    UTIMES = "utimes"
    WR_RND = "wr-rnd"
    WR_SEQ = "wr-seq"


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
        schema.description(
            "Number of workers for the stressor; 0 = match the number of on-line CPUs"
        ),
    ]


@dataclass
class CpuStressorParams(CommonStressorParams):
    cpu_ops: typing.Annotated[
        typing.Optional[int],
        schema.id("cpu-ops"),
        schema.name("CPU Operations"),
        schema.description(
            "Number of bogo operations after which to stop the CPU stress workers"
        ),
    ] = None

    cpu_load: typing.Annotated[
        typing.Optional[int],
        schema.id("cpu-load"),
        schema.name("CPU Load"),
        schema.description(
            "Percentage per-worker loading for the CPU; 100 = 1 full CPU core"
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
        return f"cpu {self.workers}\n" + params_to_jobfile(
            {
                "cpu-ops": self.cpu_ops,
                "cpu-load": self.cpu_load,
                "cpu-method": self.cpu_method,
            }
        )


@dataclass
class VmStressorParams(CommonStressorParams):
    vm_bytes: typing.Annotated[
        typing.Optional[str],
        schema.id("vm-bytes"),
        schema.name("VM Memory Bytes"),
        schema.description(
            "Number of bytes per vm worker to mmap; the default is 256MB"
        ),
    ] = None

    vm_ops: typing.Annotated[
        typing.Optional[int],
        schema.id("vm-ops"),
        schema.name("VM Operations"),
        schema.description(
            "Number of bogo operations after which to stop the vm workers"
        ),
    ] = None

    vm_hang: typing.Annotated[
        typing.Optional[int],
        schema.id("vm-hang"),
        schema.name("VM Hang"),
        schema.description(
            "Number of seconds to sleep before unmapping memory; "
            "the default is zero seconds"
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
            "Populate (prefault) page tables for the memory mappings; "
            "this can stress swapping"
        ),
    ] = None

    def to_jobfile(self) -> str:
        return f"vm {self.workers}\n" + params_to_jobfile(
            {
                "vm-bytes": self.vm_bytes,
                "vm-ops": self.vm_ops,
                "vm-hang": self.vm_hang,
                "vm-keep": self.vm_keep,
                "vm-locked": self.vm_locked,
                "vm-method": self.vm_method,
                "vm-populate": self.vm_populate,
            }
        )


@dataclass
class MmapStressorParams(CommonStressorParams):
    mmap_ops: typing.Annotated[
        typing.Optional[int],
        schema.id("mmap-ops"),
        schema.name("Mmap Operations"),
        schema.description(
            "Number of bogo operations after which to stop the mmap stress workers"
        ),
    ] = None

    mmap_async: typing.Annotated[
        typing.Optional[bool],
        schema.id("mmap-async"),
        schema.name("Mmap Async"),
        schema.description(
            "Enable file based memory mapping and use asynchronous msync'ing "
            "on each page"
        ),
    ] = None

    mmap_bytes: typing.Annotated[
        typing.Optional[str],
        schema.id("mmap-bytes"),
        schema.name("Mmap Bytes"),
        schema.description(
            "Number of bytes per mmap stress worker to allocate; the default is 256MB"
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
        return f"mmap {self.workers}\n" + params_to_jobfile(
            {
                "mmap-ops": self.mmap_ops,
                "mmap-async": self.mmap_async,
                "mmap-bytes": self.mmap_bytes,
                "mmap-file": self.mmap_file,
                "mmap-mmap2": self.mmap_mmap2,
                "mmap-mprotect": self.mmap_mprotect,
                "mmap-odirect": self.mmap_odirect,
                "mmap-osync": self.mmap_osync,
            }
        )


@dataclass
class MatrixStressorParams(CommonStressorParams):
    matrix_ops: typing.Annotated[
        typing.Optional[int],
        schema.id("matrix-ops"),
        schema.name("Matrix Operations"),
        schema.description(
            "Number of bogo operations after which to stop the matrix stress workers"
        ),
    ] = None

    matrix_method: typing.Annotated[
        typing.Optional[MatrixMethod],
        schema.id("matrix-method"),
        schema.name("Matrix Stressor Method"),
        schema.description(
            "Fine grained control of which matrix stressors to use (add, copy, etc.)"
        ),
    ] = MatrixMethod.ALL

    matrix_size: typing.Annotated[
        typing.Optional[int],
        schema.id("matrix-size"),
        schema.name("Matrix Size"),
        schema.description("Size of the matrices (matrix_size x matrix_size)"),
    ] = None

    matrix_yx: typing.Annotated[
        typing.Optional[bool],
        schema.id("matrix-yx"),
        schema.name("Matrix YX"),
        schema.description(
            "Perform matrix operations in order Y by X rather than the "
            "default X by Y"
        ),
    ] = None

    def to_jobfile(self) -> str:
        return f"matrix {self.workers}\n" + params_to_jobfile(
            {
                "matrix-ops": self.matrix_ops,
                "matrix-method": self.matrix_method,
                "matrix-size": self.matrix_size,
                "matrix-yx": self.matrix_yx,
            }
        )


@dataclass
class MqStressorParams(CommonStressorParams):
    mq_ops: typing.Annotated[
        typing.Optional[int],
        schema.id("mq-ops"),
        schema.name("MQ Operations"),
        schema.description(
            "Number of bogo POSIX message send operations completed after which "
            "to stop the mq stress workers"
        ),
    ] = None

    mq_size: typing.Annotated[
        typing.Optional[int],
        schema.id("mq-size"),
        schema.name("MQ Size"),
        schema.description(
            "Specify size of POSIX message queue; the default size is "
            "10 messages and most Linux systems this is the maximum allowed "
            "size for normal users"
        ),
    ] = None

    def to_jobfile(self) -> str:
        return f"mq {self.workers}\n" + params_to_jobfile(
            {
                "mq-ops": self.mq_ops,
                "mq-size": self.mq_size,
            }
        )


@dataclass
class HDDStressorParams(CommonStressorParams):
    hdd_bytes: typing.Annotated[
        typing.Optional[str],
        schema.id("hdd-bytes"),
        schema.name("Bytes Per Worker"),
        schema.description(
            "Number of bytes to write for each hdd process; the default is 1 GB"
        ),
    ] = None

    hdd_opts: typing.Annotated[
        typing.Optional[typing.List[HddOpts]],
        schema.id("hdd-opts"),
        schema.name("HDD Options"),
        schema.description("Various stress test options as a list"),
    ] = None

    hdd_ops: typing.Annotated[
        typing.Optional[int],
        schema.id("hdd-ops"),
        schema.name("HDD Operations"),
        schema.description(
            "Number of bogo operations after which to stop the hdd stress workers"
        ),
    ] = None

    hdd_write_size: typing.Annotated[
        typing.Optional[str],
        schema.id("hdd-write-size"),
        schema.name("HDD Write Size"),
        schema.description("Size of each write in bytes"),
    ] = None

    def to_jobfile(self) -> str:
        return f"hdd {self.workers}\n" + params_to_jobfile(
            {
                "hdd-bytes": self.hdd_bytes,
                "hdd-opts": self.hdd_opts,
                "hdd-ops": self.hdd_ops,
                "hdd-write-size": self.hdd_write_size,
            }
        )


@dataclass
class IomixStressorParams(CommonStressorParams):
    iomix_bytes: typing.Annotated[
        typing.Optional[str],
        schema.id("iomix-bytes"),
        schema.name("IOMix bytes"),
        schema.description(
            "Number of bytes to write for each iomix worker process; "
            "the default is 1 GB"
        ),
    ] = None

    iomix_ops: typing.Annotated[
        typing.Optional[int],
        schema.id("iomix-ops"),
        schema.name("IOMix operations"),
        schema.description(
            "Number of bogo iomix I/O operations after which to stop the stress workers"
        ),
    ] = None

    def to_jobfile(self) -> str:
        return f"iomix {self.workers}\n" + params_to_jobfile(
            {
                "iomix-bytes": self.iomix_bytes,
                "iomix-ops": self.iomix_ops,
            }
        )

@dataclass
class SockStressorParams(CommonStressorParams):
    sock_domain: typing.Annotated[
        typing.Optional[str],
        schema.id("sock-domain"),
        schema.name("Sock domain"),
        schema.description(
            "Specify the domain to use, the default is ipv4. Currently ipv4, ipv6 and unix are supported "
        ),
    ] = None

    sock_opts: typing.Annotated[
        typing.Optional[str],
        schema.id("sock-opts"),
        schema.name("Sock opts"),
        schema.description(
            "This option allows one to specify the sending method using send(2),sendmsg(2) or sendmmsg(2)"
        ),
    ] = None

    sock_ops: typing.Annotated[
        typing.Optional[int],
        schema.id("sock-ops"),
        schema.name("Sock operations"),
        schema.description(
            "Number of bogo sock operations after which to stop socket stress workers"
        ),
    ] = None

    def to_jobfile(self) -> str:
        return f"sock {self.workers}\n" + params_to_jobfile(
            {
                "sock-domain": self.sock_domain,
                "sock-opts": self.sock_opts,
                "sock-ops": self.sock_ops,
            }
        )
    
@dataclass
class StressNGParams:
    timeout: typing.Annotated[
        int,
        schema.name("Timeout"),
        schema.description("Number of seconds after which to stop the stress test"),
    ]

    stressors: typing.List[
        typing.Annotated[
            typing.Union[
                typing.Annotated[
                    CpuStressorParams,
                    annotations.discriminator_value(Stressors.CPU.value),
                    schema.name("CPU Stressor Parameters"),
                    schema.description("Parameters for running the cpu stressor"),
                ],
                typing.Annotated[
                    VmStressorParams,
                    annotations.discriminator_value(Stressors.VM.value),
                    schema.name("VM Stressor Parameters"),
                    schema.description("Parameters for running the vm stressor"),
                ],
                typing.Annotated[
                    MmapStressorParams,
                    annotations.discriminator_value(Stressors.MMAP.value),
                    schema.name("Mmap Stressor Parameters"),
                    schema.description("Parameters for running the mmap stressor"),
                ],
                typing.Annotated[
                    MatrixStressorParams,
                    annotations.discriminator_value(Stressors.MATRIX.value),
                    schema.name("Matrix Stressor Parameters"),
                    schema.description("Parameters for running the matrix stressor"),
                ],
                typing.Annotated[
                    MqStressorParams,
                    annotations.discriminator_value(Stressors.MQ.value),
                    schema.name("MQ Stressor Parameters"),
                    schema.description("Parameters for running the mq stressor"),
                ],
                typing.Annotated[
                    HDDStressorParams,
                    annotations.discriminator_value(Stressors.HDD.value),
                    schema.name("HDD Stressor Parameters"),
                    schema.description("Parameters for running the hdd stressor"),
                ],
                typing.Annotated[
                    IomixStressorParams,
                    annotations.discriminator_value(Stressors.IOMIX.value),
                    schema.name("IOMix Stressor Parameters"),
                    schema.description("Parameters for running the iomix stressor"),
                ],
                typing.Annotated[
                    SockStressorParams,
                    annotations.discriminator_value(Stressors.SOCK.value),
                    schema.name("Sock Stressor Parameters"),
                    schema.description("Parameters for running the socket stressor"),
                ],
            ],
            annotations.discriminator("stressor", discriminator_inlined=True),
            schema.name("Stressors List"),
            schema.description("List of stress-ng stressors and parameters"),
        ]
    ]

    page_in: typing.Annotated[
        typing.Optional[bool],
        schema.id("page-in"),
        schema.name("Page in"),
        schema.description(
            "Touch allocated pages that are not in core, forcing them to be paged "
            "back in. This is a useful option to force all the allocated pages to "
            "be paged in when using the bigheap, mmap and vm stressors."
        ),
    ] = None

    verbose: typing.Annotated[
        typing.Optional[bool],
        schema.name("Verbose"),
        schema.description("Verbose output"),
    ] = None

    metrics_brief: typing.Annotated[
        typing.Optional[bool],
        schema.id("metrics-brief"),
        schema.name("Brief Metrics"),
        schema.description("Brief version of the metrics output"),
    ] = None

    workdir: typing.Annotated[
        typing.Optional[str],
        schema.name("Working Dir"),
        schema.description(
            "Directory in which stress-ng will be executed "
            "(for example, to target a specific volume)"
        ),
    ] = None

    cleanup: typing.Annotated[
        typing.Optional[bool],
        schema.name("Cleanup"),
        schema.description("Cleanup artifacts after the plugin run"),
    ] = False


    def to_jobfile(self) -> str:
        return params_to_jobfile(
            {
                "timeout": self.timeout,
                "verbose": self.verbose,
                "metrics-brief": self.metrics_brief,
            }
        )


@dataclass
class SystemInfoOutput:
    stress_ng_version: typing.Annotated[
        str,
        schema.id("stress-ng-version"),
        schema.name("stress_ng_version"),
        schema.description("Version of the stressng tool used"),
    ]

    compiler: typing.Annotated[
        str,
        schema.name("compiler"),
        schema.description("Compiler used to build the stressng tool"),
    ]

    run_by: typing.Annotated[
        str,
        schema.id("run-by"),
        schema.name("run_by"),
        schema.description("Username of the person who ran the test"),
    ]

    date: typing.Annotated[
        str,
        schema.id("date-yyyy-mm-dd"),
        schema.name("date"),
        schema.description("Date on which the test was run"),
    ]

    time: typing.Annotated[
        str,
        schema.id("time-hh-mm-ss"),
        schema.name("time"),
        schema.description("Time at which the test was run"),
    ]

    epoch: typing.Annotated[
        int,
        schema.id("epoch-secs"),
        schema.name("epoch"),
        schema.description("Epoch at which the test was run"),
    ]

    hostname: typing.Annotated[
        str,
        schema.name("hostname"),
        schema.description("Host on which the test was run"),
    ]

    sysname: typing.Annotated[
        str,
        schema.name("System name"),
        schema.description("Name of the system on which the test was run"),
    ]

    nodename: typing.Annotated[
        str,
        schema.name("nodename"),
        schema.description("Name of the node on which the test was run"),
    ]

    release: typing.Annotated[
        str,
        schema.name("release"),
        schema.description("Kernel release on which the test was run"),
    ]

    version: typing.Annotated[
        str,
        schema.name("version"),
        schema.description("Version on which the test was run"),
    ]

    machine: typing.Annotated[
        str,
        schema.name("machine"),
        schema.description("Machine type on which the test was run"),
    ]

    uptime: typing.Annotated[
        int,
        schema.name("uptime"),
        schema.description("Uptime of the machine the test was run on"),
    ]

    totalram: typing.Annotated[
        int,
        schema.name("totalram"),
        schema.description("Total amount of RAM the test machine had"),
    ]

    freeram: typing.Annotated[
        int,
        schema.name("freeram"),
        schema.description("Amount of free RAM the test machine had"),
    ]

    sharedram: typing.Annotated[
        int,
        schema.name("sharedram"),
        schema.description("Amount of shared RAM the test machine had"),
    ]

    bufferram: typing.Annotated[
        int,
        schema.name("bufferram"),
        schema.description("Amount of buffer RAM the test machine had"),
    ]

    totalswap: typing.Annotated[
        int,
        schema.name("totalswap"),
        schema.description("Total amount of swap the test machine had"),
    ]

    freeswap: typing.Annotated[
        int,
        schema.name("freeswap"),
        schema.description("Amount of free swap the test machine had"),
    ]

    pagesize: typing.Annotated[
        int,
        schema.name("pagesize"),
        schema.description("Memory page size the test machine used"),
    ]

    cpus: typing.Annotated[
        int,
        schema.name("cpus"),
        schema.description("Number of CPU cores the test machine had"),
    ]

    cpus_online: typing.Annotated[
        int,
        schema.id("cpus-online"),
        schema.name("cpus_online"),
        schema.description("Number of online CPUs the test machine had"),
    ]

    ticks_per_second: typing.Annotated[
        int,
        schema.id("ticks-per-second"),
        schema.name("ticks_per_second"),
        schema.description("CPU ticks per second on the test machine"),
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
        schema.description("Number of iterations of the stressor during the run"),
    ]

    bogo_ops_per_second_usr_sys_time: typing.Annotated[
        float,
        schema.id("bogo-ops-per-second-usr-sys-time"),
        schema.name("Bogus operations per second in user and sys time"),
        schema.description(
            "Total bogo operations per second based on cumulative user and system time"
        ),
    ]

    bogo_ops_per_second_real_time: typing.Annotated[
        float,
        schema.id("bogo-ops-per-second-real-time"),
        schema.name("Bogus operations per second in real time"),
        schema.description(
            "Total bogo operations per second based on wall clock run time"
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
        schema.description(
            "Total percentage of CPU used divided by number of stressor instances; "
            "100% is 1 full CPU"
        ),
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
        typing.Optional[float],
        schema.id("add-matrix-ops-per-sec"),
        schema.name("Add matrix operations per second"),
    ] = None

    copy_matrix_ops_per_sec: typing.Annotated[
        typing.Optional[float],
        schema.id("copy-matrix-ops-per-sec"),
        schema.name("Copy matrix operations per second"),
    ] = None

    div_matrix_ops_per_sec: typing.Annotated[
        typing.Optional[float],
        schema.id("div-matrix-ops-per-sec"),
        schema.name("Div matrix operations per second"),
    ] = None

    frobenius_matrix_ops_per_sec: typing.Annotated[
        typing.Optional[float],
        schema.id("frobenius-matrix-ops-per-sec"),
        schema.name("Frobenius matrix operations per second"),
    ] = None

    hadamard_matrix_ops_per_sec: typing.Annotated[
        typing.Optional[float],
        schema.id("hadamard-matrix-ops-per-sec"),
        schema.name("Hadamard matrix operations per second"),
    ] = None

    identity_matrix_ops_per_sec: typing.Annotated[
        typing.Optional[float],
        schema.id("identity-matrix-ops-per-sec"),
        schema.name("Identity matrix operations per second"),
    ] = None

    mean_matrix_ops_per_sec: typing.Annotated[
        typing.Optional[float],
        schema.id("mean-matrix-ops-per-sec"),
        schema.name("Mean matrix operations per second"),
    ] = None

    mult_matrix_ops_per_sec: typing.Annotated[
        typing.Optional[float],
        schema.id("mult-matrix-ops-per-sec"),
        schema.name("Mult matrix operations per second"),
    ] = None

    negate_matrix_ops_per_sec: typing.Annotated[
        typing.Optional[float],
        schema.id("negate-matrix-ops-per-sec"),
        schema.name("Negate matrix operations per second"),
    ] = None

    prod_matrix_ops_per_sec: typing.Annotated[
        typing.Optional[float],
        schema.id("prod-matrix-ops-per-sec"),
        schema.name("Prod matrix operations per second"),
    ] = None

    sub_matrix_ops_per_sec: typing.Annotated[
        typing.Optional[float],
        schema.id("sub-matrix-ops-per-sec"),
        schema.name("Sub matrix operations per second"),
    ] = None

    square_matrix_ops_per_sec: typing.Annotated[
        typing.Optional[float],
        schema.id("square-matrix-ops-per-sec"),
        schema.name("Square matrix operations per second"),
    ] = None

    trans_matrix_ops_per_sec: typing.Annotated[
        typing.Optional[float],
        schema.id("trans-matrix-ops-per-sec"),
        schema.name("Trans matrix operations per second"),
    ] = None

    zero_matrix_ops_per_sec: typing.Annotated[
        typing.Optional[float],
        schema.id("zero-matrix-ops-per-sec"),
        schema.name("Zero matrix operations per second"),
    ] = None


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
class IOMixOutput(CommonOutput):
    """
    This is the data structure that holds the results for the IOMix stressor
    """


iomix_output_schema = plugin.build_object_schema(IOMixOutput)

@dataclass
class SockOutput(CommonOutput):
    """
    This is the data structure that holds the results for the Sock stressor
    """


sock_output_schema = plugin.build_object_schema(SockOutput)

@dataclass
class WorkloadResults:
    test_config: typing.Annotated[
        StressNGParams,
        schema.name("Test configuration"),
        schema.description("The stressng test parameters"),
    ]

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

    iomixinfo: typing.Annotated[
        typing.Optional[IOMixOutput],
        schema.name("IOMix Output"),
        schema.description("IOMix stressor output object"),
    ] = None

    sockinfo: typing.Annotated[
        typing.Optional[SockOutput],
        schema.name("Sock Output"),
        schema.description("Sock stressor output object"),
    ] = None

@dataclass
class WorkloadError:
    error: str
