import datetime
import os
import numpy as np
import pandas as pd   # type: ignore
import netCDF4 as nc   # type: ignore
# from collections import OrderedDict

from typing import Dict, List, Union, Optional

from ..constants import REGIONS

CBH_VARNAMES = ['prcp', 'tmin', 'tmax']
CBH_INDEX_COLS = [0, 1, 2, 3, 4, 5]
TS_FORMAT = '%Y %m %d %H %M %S' # 1915 1 13 0 0 0
NA_VALS_DEFAULT = ['-99.0', '-999.0', 'NaN', 'inf']

class CbhAscii(object):

    """Class for handling classic climate-by-hru (CBH) files.
    """

    # Author: Parker Norton (pnorton@usgs.gov)
    # Create date: 2019-04

    # This class assumes it is dealing with regional cbh files (not a CONUS-level NHM file)
    # TODO: As currently written the type of data (e.g. tmax, tmin, prcp) is ignored.
    # TODO: Verify that given data type size matches number of columns

    # 2016-12-20 PAN:
    # As written this works with CBH files that were created with
    # java class gov.usgs.mows.GCMtoPRMS.GDPtoCBH
    # This program creates the CBH files in the format needed by PRMS
    # and also verifies the correctness of the data including:
    #    tmax is never less than tmin
    #    prcp is never negative
    #    any missing data/missing date is filled with (?? avg of bracketing dates??)

    def __init__(self, src_path: Optional[str] = None,
                 st_date: Optional[datetime.datetime] = None,
                 en_date: Optional[datetime.datetime] = None,
                 indices: Optional[Dict] = None,
                 nhm_hrus: Optional[List] = None,
                 mapping: Optional[Dict] = None):
        """Create CbhAscii object.

        :param src_path: path to by-region CBH ASCII source files
        :param st_date: start date for extraction
        :param en_date: end date for extraction
        :param indices: ordered dictionary of nhm_id, local_id pairs
        :param nhm_hrus: list NHM HRUs to extract
        :param mapping: dictionary mapping regions to nhm_id ranges
        """

        self.__src_path = src_path

        # self.__indices = [str(kk) for kk in indices]
        self.__indices = indices    # OrdereDict: nhm_ids -> local_ids

        self.__data = None
        self.__stdate = st_date
        self.__endate = en_date
        self.__nhm_hrus = nhm_hrus
        self.__mapping = mapping
        self.__dataframe = None

    def read_cbh(self):
        """Reads an entire CBH file.
        """

        # incl_cols = list(self.__indices.values())
        # for xx in CBH_INDEX_COLS[:-1]:
        #     incl_cols.insert(0, xx)

        incl_cols = list(CBH_INDEX_COLS)

        for xx in self.__indices.values():
            incl_cols.append(xx+5)  # include an offset for the datetime info
        # print(incl_cols)

        # Columns 0-5 always represent date/time information
        self.__data = pd.read_csv(self.__src_path, sep=' ', skipinitialspace=True, usecols=incl_cols,
                                  skiprows=3, engine='c', memory_map=True,
                                  parse_dates={'time': CBH_INDEX_COLS},
                                  index_col='time', header=None, na_values=[-99.0, -999.0])

        self.__data.index = pd.to_datetime(self.__data.index, exact=True, cache=True, format=TS_FORMAT)

        if self.__stdate is not None and self.__endate is not None:
            self.__data = self.__data[self.__stdate:self.__endate]

        # self.__data.reset_index(drop=True, inplace=True)

        # Rename columns with NHM HRU ids
        ren_dict = {v + 5: k for k, v in self.__indices.items()}

        # NOTE: The rename is an expensive operation
        self.__data.rename(columns=ren_dict, inplace=True)

    def read_cbh_full(self):
        """Read entire CBH file.
        """

        # incl_cols = list(self.__indices.values())
        # for xx in CBH_INDEX_COLS[:-1]:
        #     incl_cols.insert(0, xx)

        print('READING')
        # Columns 0-5 always represent date/time information
        self.__data = pd.read_csv(self.__src_path, sep=' ', skipinitialspace=True,
                                  skiprows=3, engine='c', memory_map=True,
                                  parse_dates={'time': CBH_INDEX_COLS},
                                  # date_parser=dparse, parse_dates={'time': CBH_INDEX_COLS},
                                  index_col='time', header=None, na_values=[-99.0, -999.0])

        self.__data.index = pd.to_datetime(self.__data.index, exact=True, cache=True, format=TS_FORMAT)

        if self.__stdate is not None and self.__endate is not None:
            self.__data = self.__data[self.__stdate:self.__endate]

        # self.__data.reset_index(drop=True, inplace=True)

        # Rename columns with NHM HRU ids
        # ren_dict = {v + 5: k for k, v in self.__indices.items()}

        # NOTE: The rename is an expensive operation
        # self.__data.rename(columns=ren_dict, inplace=True)
        self.__data['year'] = self.__data.index.year
        self.__data['month'] = self.__data.index.month
        self.__data['day'] = self.__data.index.day
        self.__data['hour'] = 0
        self.__data['minute'] = 0
        self.__data['second'] = 0

    def read_ascii_file(self, filename: str,
                        columns: Optional[List] = None) -> pd.DataFrame:
        """Reads a single CBH file.

        :param filename: name of the CBH file
        :param columns: columns to read
        :returns: dataframe of CBH variable
        """
        # Columns 0-5 always represent date/time information
        time_col_names = {0: 'year', 1: 'month', 2: 'day', 3: 'hour', 4: 'minute', 5: 'second'}

        if columns is not None:
            df = pd.read_csv(filename, sep=' ', skipinitialspace=True,
                             skiprows=3, engine='c', memory_map=True,
                             header=None, na_values=NA_VALS_DEFAULT,
                             usecols=columns)
        else:
            df = pd.read_csv(filename, sep=' ', skipinitialspace=True,
                             skiprows=3, engine='c', memory_map=True,
                             header=None, na_values=NA_VALS_DEFAULT)

        # Rename columns with time information
        df.rename(columns=time_col_names, inplace=True)

        # Rename columns with local model indices
        ren_dict = {k + 6: k + 1 for k in range(len(df.columns))}
        df.rename(columns=ren_dict, inplace=True)

        df['time'] = pd.to_datetime(df[time_col_names.values()], yearfirst=True)
        df.drop(columns=time_col_names.values(), inplace=True)
        df.set_index('time', inplace=True)

        return df

    def check_region(self, region: str) -> Union[Dict[int, int], None]:
        """Get the range of nhm_id values for selected region.

        :param region: HUC2 region number (1 to 18)
        :returns: dictionary of local_id, nhm_id pairs
        """
        if self.__indices is not None:
            # Get the range of nhm_ids for the region
            rvals = self.__mapping[region]

            # print('Examining {} ({} to {})'.format(rr, rvals[0], rvals[1]))
            if rvals[0] >= rvals[1]:
                raise ValueError('Lower HRU bound is greater than upper HRU bound.')

            idx_retrieve = OrderedDict()

            for yy in self.__indices.keys():
                if rvals[0] <= yy <= rvals[1]:
                    idx_retrieve[self.__indices[yy]] = yy  # {local_ids: nhm_ids}

            return idx_retrieve
        return None

    def read_cbh_multifile(self, var: Optional[str] = None) -> Union[pd.DataFrame, None]:
        """Read cbh data from multiple csv files.

        :param var: name of variable to read
        :returns: dataframe of extracted variable
        """

        if var is None:
            raise ValueError('Variable name (var) must be provided')

        first = True
        self.__dataframe = None

        for rr in REGIONS:
            idx_retrieve = self.check_region(region=rr)

            if len(idx_retrieve) > 0:
                # Build the list of columns to load
                # The given local ids must be adjusted by 5 to reflect:
                #     1) the presence of 6 columns of time information
                #     2) 0-based column names
                load_cols = list(CBH_INDEX_COLS)
                load_cols.extend([xx+5 for xx in idx_retrieve.keys()])
            else:
                load_cols = None

            if len(idx_retrieve) > 0:
                # The current region contains HRUs in the model subset
                # Read in the data for those HRUs
                cbh_file = f'{self.__src_path}/{rr}_{var}.cbh.gz'

                print(f'\tLoad {len(idx_retrieve)} HRUs from {rr}')

                if not os.path.isfile(cbh_file):
                    # Missing data file for this variable and region
                    raise IOError(f'Required CBH file, {cbh_file}, is missing.')

                # df = self.read_ascii_file(cbh_file, columns=load_cols)

                # Small read to get number of columns
                df = pd.read_csv(cbh_file, sep=' ', skipinitialspace=True,
                                 usecols=load_cols, nrows=2,
                                 skiprows=3, engine='c', memory_map=True,
                                 parse_dates={'time': CBH_INDEX_COLS},
                                 # date_parser=dparse, parse_dates={'time': CBH_INDEX_COLS},
                                 index_col='time', header=None, na_values=[-99.0, -999.0, 'NaN', 'inf'])


                # Override Pandas' rather stupid default of float64
                col_dtypes = {xx: np.float32 for xx in df.columns}

                # Now read the whole file using float32 instead of float64
                df = pd.read_csv(cbh_file, sep=' ', skipinitialspace=True,
                                 usecols=load_cols, dtype=col_dtypes,
                                 skiprows=3, engine='c', memory_map=True,
                                 parse_dates={'time': CBH_INDEX_COLS},
                                 # date_parser=dparse, parse_dates={'time': CBH_INDEX_COLS},
                                 index_col='time', header=None, na_values=[-99.0, -999.0, 'NaN', 'inf'])

                df.index = pd.to_datetime(df.index, exact=True, cache=True, format=TS_FORMAT)

                if self.__stdate is not None and self.__endate is not None:
                    # Restrict the date range
                    df = df[self.__stdate:self.__endate]

                # Rename columns with NHM HRU ids
                ren_dict = {k+5: v for k, v in idx_retrieve.items()}

                # NOTE: The rename is an expensive operation
                df.rename(columns=ren_dict, inplace=True)

                if first:
                    self.__dataframe = df.copy()
                    first = False
                else:
                    self.__dataframe = self.__dataframe.join(df, how='left')
        return self.__dataframe

    def get_var(self, var: str) -> Union[pd.DataFrame, None]:
        """Get CBH variable.

        :param var: name of CBH variable
        :returns: dataframe of CBH variable values
        """

        data = self.read_cbh_multifile(var=var)
        return data

    def write_ascii(self, pathname: Optional[str] = None,
                    fileprefix: Optional[str] = None,
                    variables: Optional[List[str]] = None):
        """Write ASCII CBH file for selected variable.

        By default CBH filenames are saved in the current working directory and
        are named for the selected variable with an extension of .cbh

        :param pathname: path to save files to
        :param fileprefix: prefix to add to CBH output filename
        :param variables: variables to write to CBH files
        """

        # For out_order the first six columns contain the time information and
        # are always output for the cbh files
        out_order = [kk for kk in self.__nhm_hrus]
        for cc in ['second', 'minute', 'hour', 'day', 'month', 'year']:
            out_order.insert(0, cc)

        var_list = []
        if variables is None:
            var_list = CBH_VARNAMES
        elif isinstance(list, variables):
            var_list = variables

        for cvar in var_list:
            data = self.get_var(var=cvar)

            # Add time information as columns
            data['year'] = data.index.year
            data['month'] = data.index.month
            data['day'] = data.index.day
            data['hour'] = 0
            data['minute'] = 0
            data['second'] = 0

            # Output ASCII CBH files
            if fileprefix is None:
                outfile = f'{cvar}.cbh'
            else:
                outfile = f'{fileprefix}_{cvar}.cbh'

            if pathname is not None:
                outfile = f'{pathname}/{outfile}'

            out_cbh = open(outfile, 'w')
            out_cbh.write('Written by Bandit\n')
            out_cbh.write(f'{cvar} {len(self.__nhm_hrus)}\n')
            out_cbh.write('########################################\n')

            data.to_csv(out_cbh, columns=out_order, na_rep='-999', float_format='%0.3f',
                        sep=' ', index=False, header=False, encoding=None, chunksize=50)
            out_cbh.close()

    def write_netcdf(self, filename: str,
                     variables: Optional[List[str]] = None):
        """Write CBH to netcdf format file

        :param filename: name of netCDF output file
        :param variables: list of variables to write to output file
        """

        # NetCDF-related variables
        var_desc = {'tmax': 'Maximum Temperature', 'tmin': 'Minimum temperature', 'prcp': 'Precipitation'}
        var_units = {'tmax': 'C', 'tmin': 'C', 'prcp': 'inches'}

        # Create a netCDF file for the CBH data
        nco = nc.Dataset(filename, 'w', clobber=True)
        nco.createDimension('hru', len(self.__nhm_hrus))
        nco.createDimension('time', None)

        timeo = nco.createVariable('time', 'f4', ('time'))
        timeo.calendar = 'standard'
        # timeo.bounds = 'time_bnds'

        # FIXME: Days since needs to be set to the starting date of the model pull
        timeo.units = 'days since 1980-01-01 00:00:00'

        hruo = nco.createVariable('hru', 'i4', ('hru'))
        hruo.long_name = 'Hydrologic Response Unit ID (HRU)'

        var_list = []
        if variables is None:
            var_list = CBH_VARNAMES
        elif isinstance(list, variables):
            var_list = variables

        for cvar in var_list:
            varo = nco.createVariable(cvar, 'f4', ('time', 'hru'), fill_value=nc.default_fillvals['f4'], zlib=True)
            varo.long_name = var_desc[cvar]
            varo.units = var_units[cvar]

        nco.setncattr('Description', 'Climate by HRU')
        # nco.setncattr('Bandit_version', __version__)
        # nco.setncattr('NHM_version', nhmparamdb_revision)

        # Write the HRU ids
        hruo[:] = self.__nhm_hrus

        first = True
        for cvar in var_list:
            data = self.get_var(var=cvar)

            if first:
                timeo[:] = nc.date2num(data.index.tolist(),
                                       units='days since 1980-01-01 00:00:00',
                                       calendar='standard')
                first = False

            # Write the CBH values
            nco.variables[cvar][:, :] = data[self.__nhm_hrus].values

        nco.close()

    # def write_cbh_subset(self, outdir):
    #     outdata = None
    #     first = True
    #
    #     for vv in CBH_VARNAMES:
    #         outorder = list(CBH_INDEX_COLS)
    #
    #         for rr, rvals in iteritems(self.__mapping):
    #             idx_retrieve = {}
    #
    #             for yy in self.__nhm_hrus.keys():
    #                 if rvals[0] <= yy <= rvals[1]:
    #                     idx_retrieve[yy] = self.__nhm_hrus[yy]
    #
    #             if len(idx_retrieve) > 0:
    #                 self.__src_path = '{}/{}_{}.cbh.gz'.format(self.__cbhdb_dir, rr, vv)
    #                 self.read_cbh()
    #                 if first:
    #                     outdata = self.__data
    #                     first = False
    #                 else:
    #                     outdata = pd.merge(outdata, self.__data, how='left', left_index=True, right_index=True)
    #
    #         # Append the HRUs as ordered for the subset
    #         outorder.extend(self.__nhm_hrus)
    #
    #         out_cbh = open('{}/{}.cbh'.format(outdir, vv), 'w')
    #         out_cbh.write('Written by pyPRMS.Cbh\n')
    #         out_cbh.write('{} {}\n'.format(vv, len()))

    # def read_cbh_parq(self, src_dir):
    #     """Read CBH files stored in the parquet format"""
    #     if self.__indices:
    #         pfile = fp.ParquetFile('{}/daymet_{}.parq'.format(src_dir, self.__var))
    #         self.__data = pfile.to_pandas(self.__indices)
    #
    #         if self.__stdate is not None and self.__endate is not None:
    #             # Given a date range to restrict the output
    #             self.__data = self.__data[self.__stdate:self.__endate]
    #
    #     self.__data['year'] = self.__data.index.year
    #     self.__data['month'] = self.__data.index.month
    #     self.__data['day'] = self.__data.index.day
    #     self.__data['hour'] = 0
    #     self.__data['minute'] = 0
    #     self.__data['second'] = 0
    #
    # def read_cbh_hdf(self, src_dir):
    #     """Read CBH files stored in HDF5 format"""
    #     if self.__indices:
    #         # self.__data = pd.read_hdf('{}/daymet_{}.h5'.format(src_dir, self.__var), columns=self.__indices)
    #         self.__data = pd.read_hdf('{}/daymet_{}.h5'.format(src_dir, self.__var))
    #
    #         if self.__stdate is not None and self.__endate is not None:
    #             # Given a date range to restrict the output
    #             self.__data = self.__data[self.__stdate:self.__endate]
    #
    #         self.__data = self.__data[self.__indices]
    #
    #     self.__data['year'] = self.__data.index.year
    #     self.__data['month'] = self.__data.index.month
    #     self.__data['day'] = self.__data.index.day
    #     self.__data['hour'] = 0
    #     self.__data['minute'] = 0
    #     self.__data['second'] = 0
    #
