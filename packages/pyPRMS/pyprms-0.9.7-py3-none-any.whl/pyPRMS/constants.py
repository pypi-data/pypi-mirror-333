import numpy as np

from packaging.version import Version
from typing import Dict, List, NamedTuple, Union

# Define aliases for static typing
MetaDataType = Dict[str, Dict]

# Version = NamedTuple('Version', [('major', Union[int, None]),
#                                  ('minor', Union[int, None]),
#                                  ('revision', Union[int, None])])

# Default PRMS version to use for metadata
PRMS_VERSION = Version('5.2.1.1')

# PRMS6 experimental development version
PRMS6_DEV_VERSION = Version('60.0')

# Order to write control file parameters for printing and writing a new control file
ctl_order: List[str] = ['start_time', 'end_time', 'initial_deltat', 'executable_desc', 'executable_model', 'model_mode',
                        'param_file', 'data_file', 'model_output_file', 'print_debug',
                        'et_module', 'precip_module', 'soilzone_module', 'solrad_module', 'srunoff_module',
                        'strmflow_module', 'temp_module', 'transp_module',
                        'init_vars_from_file', 'save_vars_to_file', 'var_init_file', 'var_save_file',
                        'albedo_day', 'cloud_cover_day', 'humidity_day', 'potet_day', 'precip_day', 'precip_grid',
                        'swrad_day', 'tmax_day', 'tmax_grid', 'tmin_day', 'transp_day', 'windspeed_day',
                        'tmin_grid',
                        'albedo_cbh_flag', 'cascade_flag', 'cascadegw_flag', 'cbh_binary_flag', 'cbh_check_flag',
                        'cloud_cover_cbh_flag', 'dprst_flag', 'frozen_flag', 'glacier_flag',
                        'gwflow_cbh_flag', 'gwr_swale_flag', 'humidity_cbh_flag', 'mbInit_flag', 'orad_flag',
                        'parameter_check_flag', 'snarea_curve_flag', 'snow_cbh_flag', 'snow_cloudcover_flag',
                        'soilzone_aet_flag',
                        'stream_temp_flag', 'stream_temp_shade_flag', 'strmtemp_humidity_flag',
                        'subbasin_flag', 'windspeed_cbh_flag',
                        'prms_warmup',
                        'csvON_OFF', 'csv_output_file',
                        'nhruOutON_OFF', 'nhruOutBaseFileName', 'nhruOutVars', 'nhruOutVar_names', 'nhruOut_freq',
                        'nhruOut_format', 'nhruOutNcol', 'outputSelectDatesON_OFF', 'selectDatesFileName',
                        'nsegmentOutON_OFF', 'nsegmentOutBaseFileName', 'nsegmentOutVars', 'nsegmentOutVar_names',
                        'nsegmentOut_freq', 'nsegmentOut_format',
                        'basinOutON_OFF', 'basinOutBaseFileName', 'basinOutVars', 'basinOutVar_names', 'basinOut_freq',
                        'nsubOutON_OFF', 'nsubOutBaseFileName', 'nsubOutVars', 'nsubOutVar_names', 'nsubOut_format',
                        'nsubOut_freq',
                        'statsON_OFF', 'stat_var_file', 'nstatVars', 'statVar_element', 'statVar_names',
                        'dyn_covden_flag', 'dyn_covtype_flag', 'dyn_dprst_flag', 'dyn_fallfrost_flag',
                        'dyn_imperv_flag',
                        'dyn_intcp_flag', 'dyn_potet_flag', 'dyn_radtrncf_flag', 'dyn_snareathresh_flag',
                        'dyn_soil_flag',
                        'dyn_springfrost_flag', 'dyn_sro2dprst_imperv_flag', 'dyn_sro2dprst_perv_flag',
                        'dyn_transp_flag', 'dyn_transp_on_flag',
                        'dynamic_param_log_file',
                        'covden_sum_dynamic', 'covden_win_dynamic', 'covtype_dynamic', 'dprst_depth_dynamic',
                        'dprst_frac_dynamic', 'fallfrost_dynamic', 'imperv_frac_dynamic', 'imperv_stor_dynamic',
                        'potetcoef_dynamic', 'radtrncf_dynamic', 'snareathresh_dynamic', 'snow_intcp_dynamic',
                        'soilmoist_dynamic', 'soilrechr_dynamic', 'springfrost_dynamic', 'srain_intcp_dynamic',
                        'sro2dprst_imperv_dynamic', 'sro2dprst_perv_dynamic',
                        'transp_on_dynamic', 'transpbeg_dynamic', 'transpend_dynamic', 'wrain_intcp_dynamic',
                        'dprst_transferON_OFF', 'dprst_transfer_file', 'external_transferON_OFF',
                        'external_transfer_file', 'gwr_transferON_OFF', 'gwr_transfer_file', 'lake_transferON_OFF',
                        'lake_transfer_file', 'segment_transferON_OFF', 'segment_transfer_file', 'segmentOutON_OFF',
                        'aniOutON_OFF', 'ani_output_file', 'naniOutVars', 'aniOutVar_names',
                        'dispGraphsBuffSize', 'ndispGraphs', 'dispVar_element', 'dispVar_names', 'dispVar_plot',
                        'mapOutON_OFF', 'nmapOutVars', 'mapOutVar_names']

# ctl_variable_modules: List[str] = ['et_module', 'precip_module', 'soilzone_module', 'solrad_module',
#                                    'srunoff_module', 'strmflow_module', 'temp_module', 'transp_module']

# ctl_summary_modules: List[str] = ['basin_sum', 'basin_summary', 'map_results',
#                                   'nhru_summary', 'nsegment_summary', 'nsub_summary', 'subbasin']

ctl_implicit_modules: Dict[str, str] = {'basin_module': 'basin',
                                        'intcp_module': 'intcp',
                                        'obs_module': 'obs',
                                        'snow_module': 'snowcomp',
                                        'gw_module': 'gwflow',
                                        'soilzone_module': 'soilzone'}

# This is a map between what is in the control file and what is in the parameters.xml file
internal_module_map = dict(et_module={'climate_hru': 'potet_hru'},
                           precip_module={'climate_hru': 'precipitation_hru'},
                           solrad_module={'climate_hru': 'solar_radiation_hru'},
                           temp_module={'climate_hru': 'temperature_hru'},
                           transp_module={'climate_hru': 'transpiration_hru'})

# This maps the internal parameters.xml names to the external control file module names
external_module_map = dict(potet_hru='climate_hru',
                           precipitation_hru='climate_hru',
                           solar_radiation_hru='climate_hru',
                           temperature_hru='climate_hru',
                           transpiration_hru='climate_hru')

# Constants related to parameter files
DIMENSIONS_HDR: str = 'Dimensions'
PARAMETERS_HDR: str = 'Parameters'
CATEGORY_DELIM: str = '**'  # Delimiter for categories of variables
VAR_DELIM: str = '####'  # Used to delimit dimensions and parameters
# DATA_TYPES: Dict[int, str] = {1: 'integer', 2: 'float', 3: 'double', 4: 'string'}

# Valid dimensions names for PRMS
# DIMENSION_NAMES: List[str] = ['mxnsos', 'ncascade', 'ncascdgw', 'nconsumed', 'ndays', 'ndepl',
#                               'ndeplval', 'ngate', 'ngate2', 'ngate3', 'ngate4',
#                               'nevap', 'nexternal', 'ngw', 'ngwcell', 'nhru', 'nhrucell', 'nhumid',
#                               'nlake', 'nlakeelev', 'nlapse', 'nmonths', 'nobs', 'npoigages', 'nrain',
#                               'nratetbl', 'nsegment', 'nsnow', 'nsol', 'nssr', 'nsub', 'ntemp',
#                               'numlakes', 'nwateruse', 'nwind', 'one',
#                               'nstage', 'nstage2', 'nstage3', 'nstage4']

# These dimensions are related and should have same size
# NOTE: 2025-02-05 PAN - this is currently needed by Bandit
HRU_DIMS: List[str] = ['nhru', 'ngw', 'nssr']

# Constants for NhmParamDb
REGIONS: List[str] = ['r01', 'r02', 'r03', 'r04', 'r05', 'r06', 'r07', 'r08', 'r09',
                      'r10L', 'r10U', 'r11', 'r12', 'r13', 'r14', 'r15', 'r16', 'r17', 'r18']
PARAMETERS_XML: str = 'parameters.xml'
DIMENSIONS_XML: str = 'dimensions.xml'

# 2025-01-24 PAN - used by Parameters.write_parameter_netcdf()
NETCDF_DATATYPES: Dict[int, str] = {1: 'i4', 2: 'f4', 3: 'f8', 4: 'S1'}

# 2025-01-24 PAN - used by Parameters.xml_global_parameters()
NHM_DATATYPES: Dict[str, int] = {'I': 1, 'F': 2, 'D': 3, 'S': 4}

# 2025-01-24 PAN - used by ControlFile._read() and ParameterFile._read()
PTYPE_TO_DTYPE = {1: np.int32, 2: np.float32, 3: np.float64, 4: np.str_}

NEW_PTYPE_TO_DTYPE = {'int32': np.int32, 'float32': np.float32, 'float64': np.float64, 'string': np.str_, 'datetime': np.datetime64}
PTYPE_TO_PRMS_TYPE: Dict[str, int] = {'int32': 1, 'float32': 2, 'float64': 3, 'string': 4, 'datetime': 1}

# PARNAME_DATATYPES = {'long': 1, 'float': 2, 'double': 3, 'string': 4}
# DATATYPE_TO_DTYPE = {1: int, 2: np.float32, 3: np.float64, 4: np.str_}