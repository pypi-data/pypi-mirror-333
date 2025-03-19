# vim: set ts=4
#
# Copyright 2023-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from tuxrun.tests import Test


class VdsoTest(Test):
    devices = ["qemu-*", "fvp-aemva", "avh-imx93", "avh-rpi4b"]
    name = "vdso"
    timeout = 15
    need_test_definition = True

    def render(self, **kwargs):
        kwargs["name"] = self.name
        kwargs["timeout"] = self.timeout

        return self._render("vdso.yaml.jinja2", **kwargs)
