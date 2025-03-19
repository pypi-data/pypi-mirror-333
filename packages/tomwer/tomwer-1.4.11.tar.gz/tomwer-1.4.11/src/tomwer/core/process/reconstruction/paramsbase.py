# coding: utf-8
from __future__ import annotations

import copy
import itertools
from collections import OrderedDict


class _ReconsParam(object):
    """
    Base class of the Reconstruction parameters
    """

    _UNSPLIT_KEYS = tuple()
    """keys that we don't want to treat in `to_unique_recons_set` function"""

    def __init__(self):
        self.__unmanaged_params = {}
        """dict of unmanaged option. Key is param name. Value is Value"""
        self._managed_params = {}
        """tuple of octave parameters we expect to get. Other will be moved to
        unmanaged params"""

    def changed(self):
        """callback function when a parameter value is changed"""
        pass

    @property
    def unmanaged_params(self):
        return self.__unmanaged_params

    @property
    def managed_params(self):
        return self._managed_params

    @property
    def all_params(self):
        res = list(self.managed_params.keys())
        res.extend(self.unmanaged_params.keys())
        return res

    def _add_unmanaged_param(self, param, value):
        self.__unmanaged_params[param] = value

    def _reset_unmanaged_params(self):
        self.__unmanaged_params = {}

    def _remove_unmanaged_param(self, param):
        if param in self.__unmanaged_params:
            del self.__unmanaged_params[param]

    def to_dict(self):
        """convert object to a dict readable by fastomo3"""
        raise NotImplementedError()

    @staticmethod
    def from_dict(_dict):
        """create _ReconsParam from a dict readable / writable by fastomo3"""
        raise NotImplementedError()

    def load_from_dict(self, _dict):
        """Update current paramters values from a dictionary"""
        raise NotImplementedError()

    def _get_parameter_value(self, parameter):
        """Find the parameter value from a dict name, to keep compatibility
        with fastomo3."""
        if parameter in self._managed_params:
            return self._managed_params[parameter].fget(self)
        elif parameter in self.__unmanaged_params:
            return self.unmanaged_params[parameter]
        else:
            raise ValueError("requested parameter is not registered (%s)" % parameter)

    def _set_parameter_value(self, parameter, value):
        """Find the parameter value from a dict name, to keep compatibility
        with fastomo3."""
        if parameter in self._managed_params:
            assert self._managed_params[parameter] is not None
            self._managed_params[parameter].fset(self, value)
        else:
            self.__unmanaged_params[parameter] = value
            self.changed()

    def to_unique_recons_set(self, as_to_dict: bool = False) -> tuple:
        """

        :return: a tuple of unique reconstruction parameters in order to have
                 each parameter as a single value (and no list)
        :param as_to_dict: True if we want to get the same value as if we
                                where exporting it with to_dict function. There
                                is some cast in the to_dict function.
        """
        params_list = OrderedDict()
        dict_values = self.to_dict()
        for parameter in self.all_params:
            value = self._get_parameter_value(parameter)

            if isinstance(value, _ReconsParam):
                value = value.to_unique_recons_set(as_to_dict=as_to_dict)
            elif as_to_dict is True:
                value = dict_values[parameter]
            params_list[parameter] = value
            if parameter in self._UNSPLIT_KEYS:
                params_list[parameter] = [params_list[parameter]]
                continue
            if parameter in ("DB", "DB2") and isinstance(params_list[parameter], str):
                params_list[parameter] = _get_db_fromstr(params_list[parameter])

            if type(params_list[parameter]) not in (list, tuple):
                params_list[parameter] = [params_list[parameter]]
            if not isinstance(params_list[parameter][0], dict):
                params_list[parameter] = set(params_list[parameter])

        res = list()
        for _set_rp in itertools.product(*list(params_list.values())):
            _dict_set = {}
            for key, value in zip(params_list.keys(), _set_rp):
                _dict_set[key] = value
            res.append(_dict_set)

        return tuple(res)

    def __getitem__(self, arg):
        return self._get_parameter_value(arg)

    def __setitem__(self, key, value):
        self._set_parameter_value(parameter=key, value=value)

    def _load_unmanaged_params(self, _dict):
        """reset unmanaged parameters and store all parameters not defined in
        `_managed_params` into __unmanaged_params

        :params dict _dict: dict to parse to find unmanaged parameters
        """
        if not isinstance(_dict, dict):
            raise TypeError(f"{_dict} is expected to be an instance of {dict}")
        self._reset_unmanaged_params()
        for _key in _dict:
            if _key not in self.managed_params:
                _tmp_dict = {_key: _dict[_key]}
                self.__unmanaged_params.update(_tmp_dict)

    def copy(self, other_rp):
        """
        copy parameters value from other_rp

        :param other_rp: reconsparam to copy
        """
        if other_rp is None:
            return

        for parameter_name in other_rp._managed_params:
            value = other_rp._get_parameter_value(parameter=parameter_name)

            if isinstance(value, _ReconsParam) and parameter_name in self:
                self._managed_params[parameter_name].copy(value)
            else:
                self._set_parameter_value(parameter=parameter_name, value=value)

        self._set_unmanaged_params(other_rp.unmanaged_params)

    def _set_unmanaged_params(self, params):
        assert type(params) is dict
        self.__unmanaged_params = copy.copy(params)


def _get_db_fromstr(vals):
    vals = vals.replace(" ", "")
    vals = vals.replace("(", "")
    vals = vals.replace(")", "")
    vals = vals.replace("]", "")
    vals = vals.replace("[", "")
    vals = vals.replace(";", ",").split(",")
    if vals[-1] == "":
        del vals[-1]

    res = []
    [res.append(float(val)) for val in vals]
    if len(res) == 1:
        return res[0]
    else:
        return tuple(res)
