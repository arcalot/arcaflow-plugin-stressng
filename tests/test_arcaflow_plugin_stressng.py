#!/usr/bin/env python3

import unittest
import math
import yaml
import stressng_schema
import stressng_plugin
from arcaflow_plugin_sdk import plugin


class StressNGTest(unittest.TestCase):
    @staticmethod
    def test_serialization():
        plugin.test_object_serialization(
            stressng_schema.CpuStressorParams(
                stressor=stressng_schema.Stressors.CPU, workers=2
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
            stressng_schema.MatrixStressorParams(
                stressor=stressng_schema.Stressors.MATRIX, workers=2
            )
        )
        plugin.test_object_serialization(
            stressng_schema.MqStressorParams(
                stressor=stressng_schema.Stressors.MQ, workers=2
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

        stress = stressng_schema.StressNGParams(timeout="5s", stressors=[cpu])

        reference_jobfile = "tests/reference_jobfile_cpu"

        result = stress.to_jobfile()

        for item in stress.stressors:
            result = result + item.to_jobfile()

        with open(reference_jobfile, "r") as file:
            try:
                reference = yaml.safe_load(file)
            except yaml.YAMLError as e:
                print(e)

        self.assertEqual(yaml.safe_load(result), reference)
        res = stressng_plugin.stressng_run(self.id(), stress)
        self.assertIn("success", res)
        self.assertEqual(res[1].cpuinfo.stressor, "cpu")
        self.assertGreaterEqual(math.ceil(res[1].cpuinfo.wall_clock_time), 5)

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

        stress = stressng_schema.StressNGParams(timeout="5s", stressors=[vm])

        reference_jobfile = "tests/reference_jobfile_vm"

        result = stress.to_jobfile()

        for item in stress.stressors:
            result = result + item.to_jobfile()

        with open(reference_jobfile, "r") as file:
            try:
                reference = yaml.safe_load(file)
            except yaml.YAMLError as e:
                print(e)

        self.assertEqual(yaml.safe_load(result), reference)
        res = stressng_plugin.stressng_run(self.id(), stress)
        self.assertIn("success", res)
        self.assertEqual(res[1].vminfo.stressor, "vm")
        self.assertGreaterEqual(math.ceil(res[1].vminfo.wall_clock_time), 5)

    def test_functional_mmap(self):
        mmap = stressng_schema.MmapStressorParams(
            stressor="mmap",
            workers=1,
            mmap_ops=1000,
            mmap_async=True,
            mmap_bytes="100M",
            mmap_file=True,
            mmap_mmap2=True,
            mmap_mprotect=True,
            mmap_odirect=True,
            mmap_osync=True,
        )

        stress = stressng_schema.StressNGParams(timeout="5s", stressors=[mmap])

        reference_jobfile = "tests/reference_jobfile_mmap"

        result = stress.to_jobfile()

        for item in stress.stressors:
            result = result + item.to_jobfile()

        with open(reference_jobfile, "r") as file:
            try:
                reference = yaml.safe_load(file)
            except yaml.YAMLError as e:
                print(e)

        self.assertEqual(yaml.safe_load(result), reference)
        res = stressng_plugin.stressng_run(self.id(), stress)
        self.assertIn("success", res)
        self.assertEqual(res[1].mmapinfo.stressor, "mmap")
        self.assertGreaterEqual(math.ceil(res[1].mmapinfo.wall_clock_time), 5)

    def test_functional_matrix(self):
        matrix = stressng_schema.MatrixStressorParams(
            stressor="matrix",
            workers=1,
            matrix_ops=1000,
            matrix_method=stressng_schema.MatrixMethod.ALL,
            matrix_size=1000,
            matrix_yx=True,
        )

        stress = stressng_schema.StressNGParams(timeout="5s", stressors=[matrix])

        reference_jobfile = "tests/reference_jobfile_matrix"

        result = stress.to_jobfile()

        for item in stress.stressors:
            result = result + item.to_jobfile()

        with open(reference_jobfile, "r") as file:
            try:
                reference = yaml.safe_load(file)
            except yaml.YAMLError as e:
                print(e)

        self.assertEqual(yaml.safe_load(result), reference)
        res = stressng_plugin.stressng_run(self.id(), stress)
        self.assertIn("success", res)
        self.assertEqual(res[1].matrixinfo.stressor, "matrix")
        self.assertGreaterEqual(math.ceil(res[1].matrixinfo.wall_clock_time), 5)

    def test_functional_mq(self):
        mq = stressng_schema.MqStressorParams(
            stressor="mq", workers=1, mq_ops=10000000, mq_size=32
        )

        stress = stressng_schema.StressNGParams(timeout="5s", stressors=[mq])

        reference_jobfile = "tests/reference_jobfile_mq"

        result = stress.to_jobfile()

        for item in stress.stressors:
            result = result + item.to_jobfile()

        with open(reference_jobfile, "r") as file:
            try:
                reference = yaml.safe_load(file)
            except yaml.YAMLError as e:
                print(e)

        self.assertEqual(yaml.safe_load(result), reference)
        res = stressng_plugin.stressng_run(self.id(), stress)
        self.assertIn("success", res)
        self.assertEqual(res[1].mqinfo.stressor, "mq")
        self.assertGreaterEqual(math.ceil(res[1].mqinfo.wall_clock_time), 5)

    # def test_functional_hdd(self):
    #     hdd = stressng_schema.HDDStressorParams(
    #         stressor="hdd",
    #         workers=1,
    #         hdd_bytes="100M",
    #         hdd_opts=stressng_schema.HDDOptsParams(
    #             [
    #                 stressng_schema.HddOpts.DIRECT,
    #                 stressng_schema.HddOpts.FSYNC,
    #                 stressng_schema.HddOpts.WR_RND,
    #             ]
    #         ),
    #         hdd_ops=10000,
    #         hdd_write_size="4M",
    #     )

    #     stress = stressng_schema.StressNGParams(timeout="5s", stressors=[hdd])

    #     reference_jobfile = "tests/reference_jobfile_hdd"

    #     result = stress.to_jobfile()

    #     for item in stress.stressors:
    #         result = result + item.to_jobfile()

    #     with open(reference_jobfile, "r") as file:
    #         try:
    #             reference = yaml.safe_load(file)
    #         except yaml.YAMLError as e:
    #             print(e)

    #     self.assertEqual(yaml.safe_load(result), reference)
    #     res = stressng_plugin.stressng_run(self.id(), stress)
    #     self.assertIn("success", res)
    #     self.assertEqual(res[1].hddinfo.stressor, "hdd")
    #     self.assertGreaterEqual(math.ceil(res[1].hddinfo.wall_clock_time), 5)


if __name__ == "__main__":
    unittest.main()
