# vim: set ts=4
#
# Copyright 2022-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from tuxrun.tests import Test


class RCUTorture(Test):
    devices = ["qemu-*", "fvp-aemva", "avh-imx93", "avh-rpi4b"]
    name = "rcutorture"
    timeout = 15
    need_test_definition = True

    def render(self, **kwargs):
        kwargs["name"] = self.name
        kwargs["timeout"] = self.timeout

        return self._render("rcutorture.yaml.jinja2", **kwargs)
