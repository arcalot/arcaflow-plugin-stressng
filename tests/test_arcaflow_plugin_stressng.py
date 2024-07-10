#!/usr/bin/env python3

import unittest
import math
import yaml
import stressng_schema
import stressng_plugin
from arcaflow_plugin_sdk import plugin


test_time = 5


class StressNGTest(unittest.TestCase):
    @staticmethod
    def test_serialization():
        plugin.test_object_serialization(
            stressng_schema.StressNGParams(
                timeout=10,
                stressors=[
                    stressng_schema.CpuStressorParams(
                        stressor=stressng_schema.Stressors.CPU,
                        workers=2,
                    ),
                    stressng_schema.VmStressorParams(
                        stressor=stressng_schema.Stressors.VM,
                        workers=2,
                        vm_bytes="2G",
                        vm_method=stressng_schema.VmMethod.ALL,
                    ),
                ],
                page_in=True,
                taskset="0,2-3,6,7-11",
                verbose=True,
                metrics_brief=True,
                workdir="/tmp",
                cleanup=True,
            )
        )

        plugin.test_object_serialization(
            stressng_schema.CpuStressorParams(
                stressor=stressng_schema.Stressors.CPU,
                workers=2,
                cpu_load=50,
                cpu_method=stressng_schema.CpuMethod.FFT,
            )
        )

        plugin.test_object_serialization(
            stressng_schema.VmStressorParams(
                stressor=stressng_schema.Stressors.VM,
                workers=2,
                vm_bytes="2G",
                vm_method=stressng_schema.VmMethod.ALL,
            )
        )

        plugin.test_object_serialization(
            stressng_schema.MmapStressorParams(
                stressor=stressng_schema.Stressors.MMAP,
                workers=2,
                mmap_bytes="20%",
                mmap_async=True,
            )
        )

        plugin.test_object_serialization(
            stressng_schema.MatrixStressorParams(
                stressor=stressng_schema.Stressors.MATRIX,
                workers=2,
                matrix_method=stressng_schema.MatrixMethod.ADD,
            )
        )

        plugin.test_object_serialization(
            stressng_schema.MqStressorParams(
                stressor=stressng_schema.Stressors.MQ,
                workers=2,
                mq_ops=4,
            )
        )

        plugin.test_object_serialization(
            stressng_schema.HDDStressorParams(
                stressor=stressng_schema.Stressors.HDD,
                workers=2,
                hdd_opts=[
                    stressng_schema.HddOpts.DIRECT,
                    stressng_schema.HddOpts.SYNC,
                ],
            )
        )

        plugin.test_object_serialization(
            stressng_schema.IomixStressorParams(
                stressor=stressng_schema.Stressors.IOMIX,
                workers=2,
                iomix_bytes="50g",
            )
        )

        plugin.test_object_serialization(
            stressng_schema.SockStressorParams(
                stressor=stressng_schema.Stressors.SOCK,
                workers=2,
                sock_domain=stressng_schema.SockDomain.IPV4,
                sock_opts=stressng_schema.SockOpts.SEND,
            )
        )

    def test_functional_cpu(self):
        # idea is to run a small cpu bound benchmark and
        # compare its output with a known-good output
        # this is clearly not perfect, as we're limited to the
        # field names and can't do a direct
        # comparison of the returned values

        cpu = stressng_schema.CpuStressorParams(
            stressor="cpu",
            workers=2,
            cpu_ops=1000,
            cpu_load=5,
            cpu_method=stressng_schema.CpuMethod.ALL,
        )

        stress = stressng_schema.StressNGParams(
            timeout=test_time,
            stressors=[cpu],
            taskset="0,1-2",
        )

        reference_jobfile = "tests/reference_jobfile_cpu"

        result = stress.to_jobfile()

        for item in stress.stressors:
            result = result + item.to_jobfile()

        with open(reference_jobfile, "r") as file:
            reference = yaml.safe_load(file)

        self.assertEqual(yaml.safe_load(result), reference)
        res = stressng_plugin.stressng_run(self.id(), stress)
        print(res)
        self.assertIn("success", res)
        self.assertEqual(res[1].cpuinfo.stressor, "cpu")
        self.assertGreaterEqual(math.ceil(res[1].cpuinfo.wall_clock_time), test_time)

    def test_functional_vm(self):
        vm = stressng_schema.VmStressorParams(
            stressor="vm",
            workers=1,
            vm_bytes="100M",
            vm_ops=1000,
            vm_hang=1,
            vm_keep=True,
            vm_locked=True,
            vm_method=stressng_schema.VmMethod.ALL,
            vm_populate=True,
        )

        stress = stressng_schema.StressNGParams(
            timeout=test_time,
            stressors=[vm],
            page_in=True,
        )

        reference_jobfile = "tests/reference_jobfile_vm"

        result = stress.to_jobfile()

        for item in stress.stressors:
            result = result + item.to_jobfile()

        with open(reference_jobfile, "r") as file:
            reference = yaml.safe_load(file)

        self.assertEqual(yaml.safe_load(result), reference)
        res = stressng_plugin.stressng_run(self.id(), stress)
        print(res)
        self.assertIn("success", res)
        self.assertEqual(res[1].vminfo.stressor, "vm")
        self.assertGreaterEqual(math.ceil(res[1].vminfo.wall_clock_time), test_time)

    def test_functional_mmap(self):
        mmap = stressng_schema.MmapStressorParams(
            stressor="mmap",
            workers=1,
            mmap_ops=10000000,
            mmap_async=True,
            mmap_bytes="10G",
            mmap_file=True,
            mmap_mmap2=True,
            mmap_mprotect=True,
            mmap_odirect=True,
            mmap_osync=True,
        )

        stress = stressng_schema.StressNGParams(
            timeout=test_time,
            stressors=[mmap],
            cleanup=True,
        )

        reference_jobfile = "tests/reference_jobfile_mmap"

        result = stress.to_jobfile()

        for item in stress.stressors:
            result = result + item.to_jobfile()

        with open(reference_jobfile, "r") as file:
            reference = yaml.safe_load(file)

        self.assertEqual(yaml.safe_load(result), reference)
        res = stressng_plugin.stressng_run(self.id(), stress)
        print(res)
        self.assertIn("success", res)
        self.assertEqual(res[1].mmapinfo.stressor, "mmap")
        self.assertGreaterEqual(math.ceil(res[1].mmapinfo.wall_clock_time), test_time)

    def test_functional_matrix(self):
        matrix = stressng_schema.MatrixStressorParams(
            stressor="matrix",
            workers=1,
            matrix_ops=1000,
            matrix_method=stressng_schema.MatrixMethod.ALL,
            matrix_size=1000,
            matrix_yx=True,
        )

        stress = stressng_schema.StressNGParams(
            timeout=test_time,
            stressors=[matrix],
            verbose=True,
        )

        reference_jobfile = "tests/reference_jobfile_matrix"

        result = stress.to_jobfile()

        for item in stress.stressors:
            result = result + item.to_jobfile()

        with open(reference_jobfile, "r") as file:
            reference = yaml.safe_load(file)

        self.assertEqual(yaml.safe_load(result), reference)
        res = stressng_plugin.stressng_run(self.id(), stress)
        print(res)
        self.assertIn("success", res)
        self.assertEqual(res[1].matrixinfo.stressor, "matrix")
        self.assertGreaterEqual(math.ceil(res[1].matrixinfo.wall_clock_time), test_time)

    def test_functional_mq(self):
        mq = stressng_schema.MqStressorParams(
            stressor="mq",
            workers=1,
            mq_ops=10000000,
            mq_size=32,
        )

        stress = stressng_schema.StressNGParams(
            timeout=test_time,
            stressors=[mq],
            metrics_brief=True,
        )

        reference_jobfile = "tests/reference_jobfile_mq"

        result = stress.to_jobfile()

        for item in stress.stressors:
            result = result + item.to_jobfile()

        with open(reference_jobfile, "r") as file:
            reference = yaml.safe_load(file)

        self.assertEqual(yaml.safe_load(result), reference)
        res = stressng_plugin.stressng_run(self.id(), stress)
        print(res)
        self.assertIn("success", res)
        self.assertEqual(res[1].mqinfo.stressor, "mq")
        self.assertGreaterEqual(math.ceil(res[1].mqinfo.wall_clock_time), test_time)

    def test_functional_hdd(self):
        hdd = stressng_schema.HDDStressorParams(
            stressor="hdd",
            workers=1,
            hdd_bytes="100M",
            hdd_opts=[
                stressng_schema.HddOpts.DIRECT,
                stressng_schema.HddOpts.FSYNC,
                stressng_schema.HddOpts.WR_RND,
            ],
            hdd_ops=10000,
            hdd_write_size="4M",
        )

        stress = stressng_schema.StressNGParams(
            timeout=test_time,
            stressors=[hdd],
            workdir="/",
        )

        reference_jobfile = "tests/reference_jobfile_hdd"

        result = stress.to_jobfile()

        for item in stress.stressors:
            result = result + item.to_jobfile()

        with open(reference_jobfile, "r") as file:
            reference = yaml.safe_load(file)

        self.assertEqual(yaml.safe_load(result), reference)
        res = stressng_plugin.stressng_run(self.id(), stress)
        print(res)
        self.assertIn("success", res)
        self.assertEqual(res[1].hddinfo.stressor, "hdd")
        self.assertGreaterEqual(math.ceil(res[1].hddinfo.wall_clock_time), test_time)

    def test_functional_iomix(self):
        iomix = stressng_schema.IomixStressorParams(
            stressor="iomix",
            workers=1,
            iomix_bytes="100M",
            iomix_ops=1000000,
        )

        stress = stressng_schema.StressNGParams(timeout=test_time, stressors=[iomix])

        reference_jobfile = "tests/reference_jobfile_iomix"

        result = stress.to_jobfile()

        for item in stress.stressors:
            result = result + item.to_jobfile()

        with open(reference_jobfile, "r") as file:
            reference = yaml.safe_load(file)

        self.assertEqual(yaml.safe_load(result), reference)
        res = stressng_plugin.stressng_run(self.id(), stress)
        print(res)
        self.assertIn("success", res)
        self.assertEqual(res[1].iomixinfo.stressor, "iomix")
        self.assertGreaterEqual(math.ceil(res[1].iomixinfo.wall_clock_time), test_time)

    def test_functional_sock(self):
        sock = stressng_schema.SockStressorParams(
            stressor="sock",
            workers=1,
            sock_domain=stressng_schema.SockDomain.IPV4,
            sock_opts=stressng_schema.SockOpts.SEND,
        )

        stress = stressng_schema.StressNGParams(timeout=test_time, stressors=[sock])

        reference_jobfile = "tests/reference_jobfile_sock"

        result = stress.to_jobfile()

        for item in stress.stressors:
            result = result + item.to_jobfile()

        with open(reference_jobfile, "r") as file:
            reference = yaml.safe_load(file)

        self.assertEqual(yaml.safe_load(result), reference)
        res = stressng_plugin.stressng_run(self.id(), stress)
        print(res)
        self.assertIn("success", res)
        self.assertEqual(res[1].sockinfo.stressor, "sock")
        self.assertGreaterEqual(math.ceil(res[1].sockinfo.wall_clock_time), test_time)


if __name__ == "__main__":
    unittest.main()
