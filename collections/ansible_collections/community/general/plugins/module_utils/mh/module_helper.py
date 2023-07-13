# -*- coding: utf-8 -*-
# (c) 2020, Alexei Znamensky <russoz@gmail.com>
# Copyright (c) 2020, Ansible Project
# Simplified BSD License (see LICENSES/BSD-2-Clause.txt or https://opensource.org/licenses/BSD-2-Clause)
# SPDX-License-Identifier: BSD-2-Clause

from __future__ import absolute_import, division, print_function
__metaclass__ = type


from ansible.module_utils.common.dict_transformations import dict_merge

# (TODO: remove AnsibleModule!) pylint: disable-next=unused-import
from ansible_collections.community.general.plugins.module_utils.mh.base import ModuleHelperBase, AnsibleModule  # noqa: F401
from ansible_collections.community.general.plugins.module_utils.mh.mixins.cmd import CmdMixin
from ansible_collections.community.general.plugins.module_utils.mh.mixins.state import StateMixin
from ansible_collections.community.general.plugins.module_utils.mh.mixins.deps import DependencyMixin
from ansible_collections.community.general.plugins.module_utils.mh.mixins.vars import VarsMixin
from ansible_collections.community.general.plugins.module_utils.mh.mixins.deprecate_attrs import DeprecateAttrsMixin


class ModuleHelper(DeprecateAttrsMixin, VarsMixin, DependencyMixin, ModuleHelperBase):
    facts_name = None
    output_params = ()
    diff_params = ()
    change_params = ()
    facts_params = ()

    def __init__(self, module=None):
        super(ModuleHelper, self).__init__(module)
        for name, value in self.module.params.items():
            self.vars.set(
                name, value,
                diff=name in self.diff_params,
                output=name in self.output_params,
                change=None if not self.change_params else name in self.change_params,
                fact=name in self.facts_params,
            )

    def update_output(self, **kwargs):
        self.update_vars(meta={"output": True}, **kwargs)

    def update_facts(self, **kwargs):
        self.update_vars(meta={"fact": True}, **kwargs)

    def _vars_changed(self):
        return any(self.vars.has_changed(v) for v in self.vars.change_vars())

    def has_changed(self):
        return self.changed or self._vars_changed()

    @property
    def output(self):
        result = dict(self.vars.output())
        if self.facts_name:
            facts = self.vars.facts()
            if facts is not None:
                result['ansible_facts'] = {self.facts_name: facts}
        if self.diff_mode:
            diff = result.get('diff', {})
            vars_diff = self.vars.diff() or {}
            result['diff'] = dict_merge(dict(diff), vars_diff)

        return result


class StateModuleHelper(StateMixin, ModuleHelper):
    pass


class CmdModuleHelper(CmdMixin, ModuleHelper):
    """
    THIS CLASS IS BEING DEPRECATED.
    See the deprecation notice in ``CmdMixin.__init__()``.
    """
    pass


class CmdStateModuleHelper(CmdMixin, StateMixin, ModuleHelper):
    """
    THIS CLASS IS BEING DEPRECATED.
    See the deprecation notice in ``CmdMixin.__init__()``.
    """
    pass
