
import xarray as xr
from typing import Optional

from .Parameters import Parameters


NCF_TO_NHM_TYPES = {'int32': 1, 'float32': 2, 'float64': 3, '|S1': 4}


class ParameterNetCDF(Parameters):
    """Read parameter database stored in netCDF format"""

    def __init__(self,
                 filename: str,
                 metadata,
                 verbose: Optional[bool] = False):
        """Initialize ParamDb object.

        :param filename: Path the ParamDb netcdf file
        :param verbose: Output additional debugging information
        :param verify: Verify parameters against master list
        """

        super(ParameterNetCDF, self).__init__(metadata=metadata, verbose=verbose)
        self.__filename = filename
        self.__verbose = verbose

        # Read the parameters from the parameter database
        self._read()

    def _read(self):
        """Read a parameter netCDF file.
        """

        xr_df = xr.open_dataset(self.__filename, mask_and_scale=False, decode_timedelta=False)

        # Populate the dimensions first
        self.dimensions.add(name='one', size=1)
        # self.dimensions.add(name='ndays')

        for dn, ds in dict(xr_df.sizes).items():
            self.dimensions.add(name=str(dn), size=ds)

        # Add ndepl using ndeplval
        self.dimensions.add(name='ndepl', size=int(xr_df.sizes['ndeplval'] / 11))

        # Add nobs if needed
        if not self.dimensions.exists('nobs'):
            if self.dimensions.exists('npoigages'):
                self.dimensions.add(name='nobs', size=self.dimensions.get('npoigages').size)
            else:
                self.dimensions.add(name='nobs', size=0)

        if not self.dimensions.exists('ngw'):
            self.dimensions.add(name='ngw', size=self.dimensions.get('nhru').size)

        if not self.dimensions.exists('nssr'):
            self.dimensions.add(name='nssr', size=self.dimensions.get('nhru').size)

        # Now add the parameters
        for var in xr_df.variables.keys():
            if self.__verbose:   # pragma: no cover
                print(str(var))

            cparam = xr_df[var].T

            # Add the parameter
            self.add(name=str(var))

            # Add the data
            self.get(str(var)).data = cparam.values

        self.adjust_bounded_parameters()