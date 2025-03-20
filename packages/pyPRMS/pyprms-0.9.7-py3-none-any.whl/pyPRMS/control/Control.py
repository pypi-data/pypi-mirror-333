#!/usr/bin/env python3

import io
import numpy as np
import operator
import pandas as pd   # type: ignore
import pkgutil
import re
import xml.etree.ElementTree as xmlET

from typing import Dict, List, Optional, Sequence, Union   # OrderedDict as OrderedDictType,

from networkx.utils.misc import check_create_using

from .ControlVariable import ControlVariable
from ..Exceptions_custom import ControlError
from ..constants import (ctl_order, ctl_implicit_modules, internal_module_map,
                         MetaDataType, VAR_DELIM, PTYPE_TO_PRMS_TYPE)

cond_check = {'=': operator.eq,
              '>': operator.gt,
              '<': operator.lt}

class Control(object):
    """
    Class object for a collection of control variables.
    """

    # Author: Parker Norton (pnorton@usgs.gov)
    # Create date: 2019-04-18

    def __init__(self, metadata: MetaDataType, verbose: Optional[bool] = False):
        """Create Control object.
        """

        # Container to hold dicionary of ControlVariables
        # self.__control_vars = OrderedDict()
        self.__control_vars: Dict = {}
        self.__header: Optional[List[str]] = None
        self.__verbose = verbose

        # Create an entry for each variable in the control section of
        # the metadata dictionary
        # for cvar, cvals in metadata['control'].items():
        #     self.add(name=cvar, meta=cvals)
        for cvar in metadata['control'].keys():
            self.add(name=cvar, meta=metadata['control'])

        if verbose:
            print('Pre-populate control variables done')

    def __getitem__(self, item: str) -> ControlVariable:
        """Get ControlVariable object for a variable.

        :param item: name of control file variable
        :returns: ControlVariable object
        """
        return self.get(item)

    @property
    def additional_modules(self) -> List[str]:
        """Get list of summary modules in PRMS
        """

        # TODO: module_requirements should be added to metadata?
        # NOTE: 20231109 PAN - we always want basin_sum included since the
        #                      print_debug could be set to 4 (which uses the basin_sum module)
        module_requirements = {'basin_sum': 'print_debug < 100',
                               # 'basin_sum': 'print_debug = 4',
                               'basin_summary': 'basinOutON_OFF > 0',
                               'map_results': 'mapOutON_OFF > 0',
                               'nhru_summary': 'nhruOutON_OFF > 0',
                               'nsegment_summary': 'nsegmentOutON_OFF > 0',
                               'nsub_summary': 'nsubOutON_OFF > 0',
                               'stream_temp': 'stream_temp_flag > 0',
                               'subbasin': 'subbasin_flag = 1'}

        active_modules = []

        for cmod, cond in module_requirements.items():
            if self._check_condition(cond):
                active_modules.append(cmod)

        return active_modules

    @property
    def cbh_files(self) -> List[str]:
        """Get list of possible CBH filenames.

        :returns: list of CBH files
        """

        # List of control variables that specify possible CBH files
        ctl_cbh_files = ['albebo_day', 'cloud_cover_day', 'humidity_day', 'potet_day', 'precip_day',
                         'swrad_day', 'tmax_day', 'tmin_day', 'transp_day', 'windspeed_day']
        cbh_files = []

        for cvar in ctl_cbh_files:
            if self.exists(cvar):
                cbh_files.append(self.get(cvar).values)

        return sorted(list(set(cbh_files)))

    @property
    def control_variables(self) -> Dict[str, ControlVariable]:
    # def control_variables(self) -> OrderedDictType[str, ControlVariable]:
        """Get control variable objects.

        :returns: control variable objects
        """
        return self.__control_vars

    @property
    def dynamic_parameters(self) -> List[str]:
        """Get list of parameter names for which a dynamic flag set.

        :returns: list of parameter names
        """

        dyn_params: List[str] = []

        for dv in self.__control_vars.keys():
            cvar = self.get(dv)

            if (cvar.meta.get('valid_value_type', '') == 'parameter' and
                    (isinstance(cvar.values, int | np.int32 | np.int64))):
                # Dynamic parameter flags should always be integers
                if cvar.values > 0:
                    dyn_params.extend(cvar.dyn_param_meaning)
                    # dyn_params.append(self.get(dv).associated_values)
        return dyn_params

    @property
    def has_dynamic_parameters(self) -> bool:
        """Indicates if any dynamic parameters have been requested.

        :returns: True if dynamic parameters are required
        """
        return len(self.dynamic_parameters) > 0

    @property
    def header(self) -> Optional[Sequence[str]]:
        """Get header information defined for a control object.

        This is typically taken from the first two lines of a control file.

        :returns: Header information from control file
        """
        return self.__header

    @header.setter
    def header(self, info: Union[Sequence[str], str, None]):
        """Set the header information.

        :param info: list or string of header line(s)
        """

        if info is None:
            self.__header = None
        elif isinstance(info, list):
            self.__header = info
        elif isinstance(info, str):
            self.__header = [info]

    @property
    def modules(self) -> Dict[str, str]:
        """Get the modules defined in the control file.

        Note: climate_hru is changed to precipitation_hru, temperature_hru,
        potet_hru, or solar_radiation_hru depending on the module type. This
        makes for easier identification of which process(es) is/are actually using
        climate_hru. Interally the module type is still climate_hru.

        :returns: dictionary of control variable, module name pairs
        """

        mod_dict = {}

        for vv in self.control_variables.values():
            if vv.meta.get('valid_value_type', '') == 'module':
                mname = internal_module_map.get(vv.name, {}).get(vv.values, vv.values)

                mod_dict[vv.name] = str(mname)

        # Add the modules that are implicitly included
        for mtype, mname in ctl_implicit_modules.items():
            if mtype not in mod_dict:
                mod_dict[mtype] = mname

        return mod_dict

    def add(self, name: str, meta=None):
        """Add a control variable by name.

        :param name: Name of the control variable
        :param datatype: The datatype of the control variable

        :raises ControlError: if control variable already exists
        """

        if self.exists(name):
            raise ControlError("Control variable already exists")
        self.__control_vars[name] = ControlVariable(name=name, meta=meta)
        # self.__control_vars[name] = ControlVariable(name=name, datatype=datatype, meta=meta)

    def exists(self, name: str) -> bool:
        """Checks if control variable exists.

        :param name: Name of the control variable
        :returns: True if control variable exists otherwise False
        """
        return name in self.__control_vars.keys()

    def get(self, name: str) -> ControlVariable:
        """Returns the given control variable object.

        :param name: Name of the control variable
        :returns: Control variable object

        :raises ValueError: if control variable does not exist
        """

        if self.exists(name):
            return self.__control_vars[name]
        raise ValueError(f'Control variable, {name}, does not exist.')

    def remove(self, name: str):
        """Delete a control variable if it exists.

        :param name: Name of the control variable
        """

        if self.exists(name):
            del self.__control_vars[name]

    def to_dict(self):
        """Dictionary of data for each control variable"""

        return {kk: vv.values for (kk, vv) in self.__control_vars.items()}

    def write(self, filename: str):
        """Write a control file.

        :param filename: Name of control file to create
        """

        outfile = open(filename, 'w')

        if self.__header is not None:
            for hh in self.__header:
                outfile.write(f'{hh}\n')

        order = ['datatype', 'values']

        # Get set of variables in ctl_order that are missing from control_vars
        setdiff = set(self.__control_vars.keys()).difference(set(ctl_order))

        # Add missing control variables (setdiff) in ctl_order to the end of the list
        ctl_order.extend(list(setdiff))

        for kk in ctl_order:
            if self.exists(kk):
                cvar = self.get(kk)

                outfile.write(f'{VAR_DELIM}\n')
                outfile.write(f'{kk}\n')

                for item in order:
                    if cvar.meta['datatype'] == 'datetime':
                        date_tmp = [int(xx) for xx in re.split(r'[-T:.]+', str(cvar.values))[0:6]]

                        if item == 'datatype':
                            outfile.write(f'{len(date_tmp)}\n')
                            outfile.write(f'{PTYPE_TO_PRMS_TYPE[cvar.meta["datatype"]]}\n')
                        if item == 'values':
                            for cval in date_tmp:
                                outfile.write(f'{cval}\n')
                    else:
                        if item == 'datatype':
                            outfile.write(f'{cvar.size}\n')
                            outfile.write(f'{PTYPE_TO_PRMS_TYPE[cvar.meta["datatype"]]}\n')
                        if item == 'values':
                            if cvar.meta['context'] == 'scalar':
                                # Single-values (e.g. int, float, str)
                                # print(type(cvar.values))
                                if isinstance(cvar.values, np.bytes_):
                                    print("BYTES")
                                    outfile.write(f'{cvar.values.decode()}\n')
                                else:
                                    outfile.write(f'{cvar.values}\n')
                            else:
                                # Multiple-values
                                if isinstance(cvar.values, np.ndarray):
                                    for cval in cvar.values:
                                        outfile.write(f'{cval}\n')
                                else:
                                    outfile.write(f'{cvar.values}\n')

        outfile.close()

    def write_metadata_csv(self, filename: str, sep: str = '\t'):
        """Writes the control metadata to a CSV file"""

        out_list = []

        # <control_param name="soilrechr_dynamic" version="5.0">
        #     <default>dyn_soil_rechr.param</default>
        #     <force_default>1</force_default>
        #     <type>4</type>
        #     <numvals>1</numvals>
        #     <desc>Pathname of the time series of pre-processed values for dynamic parameter soil_rechr_max_frac</desc>
        # </control_param>

        for pk in sorted(list(self.__control_vars.keys())):
            cvar = self.get(pk)
            md = cvar.meta
            assert md is not None

            meta_default = md.get('default')
            assert meta_default is not None

            if pk in ['start_time', 'end_time']:
                dt = pd.Timestamp(meta_default)
                out_list.append([cvar.name,
                                 'int32',
                                 md.get('description', ''),
                                 f'{dt.year},{dt.month},{dt.day},{dt.hour},{dt.minute},{dt.second}'])
                                 # pd.Timestamp(meta_default).strftime('%-Y,%-m,%-d,%-H,%-M,%-S')])
            else:
                out_list.append([cvar.name,
                                 md.get('datatype', ''),
                                 md.get('description', ''),
                                 md.get('default')])

        col_names = ['variable_name', 'datatype', 'description', 'default']

        df = pd.DataFrame.from_records(out_list, columns=col_names)
        if sep == ',':   # pragma: no cover
            df.to_csv(filename, sep=sep, quotechar='"', index=False)
        else:
            df.to_csv(filename, sep=sep, index=False)

    def _check_condition(self, cstr: str) -> bool:
        """Takes a string of the form '<control_var> <op> <value>' and checks
        if the condition is True
        """
        # if len(cstr) == 0:
        #     return True
        value: Union[int, str]

        var, op, value = cstr.split(' ')
        value = int(value)

        ctl_val = self.get(var).values
        assert ctl_val is not None

        return cond_check[op](ctl_val, value)

    def _read(self):
        """Abstract function for reading.
        """
        assert False, 'Control._read() must be defined by child class'
