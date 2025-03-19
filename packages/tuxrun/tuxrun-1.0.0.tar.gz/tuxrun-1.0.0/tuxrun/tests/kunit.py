# vim: set ts=4
#
# Copyright 2021-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from tuxrun.tests import Test


class KUnit(Test):
    devices = ["qemu-*", "fvp-aemva", "avh-imx93", "avh-rpi4b"]
    name = "kunit"
    timeout = 20
    need_test_definition = True

    def render(self, **kwargs):
        kwargs["name"] = self.name
        kwargs["timeout"] = self.timeout

        return self._render("kunit.yaml.jinja2", **kwargs)
