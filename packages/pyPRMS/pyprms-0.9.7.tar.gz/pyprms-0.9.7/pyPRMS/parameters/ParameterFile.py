
# from typing import Any,  Union, Dict, List, OrderedDict as OrderedDictType, Set
import numpy as np
from typing import List, Optional, Set

from ..Exceptions_custom import ParameterExistsError, ParameterNotValidError
from .Parameters import Parameters
from ..constants import DIMENSIONS_HDR, PARAMETERS_HDR, VAR_DELIM, PTYPE_TO_DTYPE
from ..prms_helpers import get_file_iter

from rich.console import Console
from rich import pretty

pretty.install()
con = Console()


class ParameterFile(Parameters):

    """Class to handle reading PRMS parameter file format."""

    def __init__(self, filename: str,
                 metadata,
                 verbose: Optional[bool] = False):
                 # verify: Optional[bool] = True):
        """Create the ParameterFile object.

        :param filename: name of parameter file
        :param verbose: output debugging information
        :param verify: whether to load the master parameters (default=True)
        """

        super(ParameterFile, self).__init__(metadata=metadata, verbose=verbose)

        # self.__filename = None
        # self.__header = None

        self.__isloaded = False
        self.__updated_parameters: Set[str] = set()
        self.__verbose = verbose
        self.filename = filename

    @property
    def filename(self) -> str:
        """Get parameter filename.

        :returns: name of parameter file
        """

        return self.__filename

    @filename.setter
    def filename(self, name: str):
        """Set the name of the parameter file.

        :param name: name of parameter file
        """

        self.__isloaded = False
        self.__filename = name
        self.__header: List[str] = []  # Initialize the list of file headers

        self._read()

    @property
    def headers(self) -> List[str]:
        """Get the headers from the parameter file.

        :returns: list of headers from parameter file
        """

        return self.__header

    @property
    def updated_parameters(self) -> Set[str]:
        """Get list of parameters that had more than one entry in the parameter file.

        :returns: list of parameters
        """

        return self.__updated_parameters

    def _read(self):
        """Read parameter file.
        """

        if self.__verbose:   # pragma: no cover
            con.print('INFO: Reading parameter file')

        # Read the parameter file into memory and parse it
        it = get_file_iter(self.filename)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Grab the header stuff first
        for line in it:
            if line.strip('* ') == DIMENSIONS_HDR:
                break
            self.__header.append(line)

        if self.__verbose:   # pragma: no cover
            con.print(f'HEADERS: {self.__header}')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Now process the dimensions
        for line in it:
            if line.strip('* ') == PARAMETERS_HDR:
                break
            if line == VAR_DELIM:
                continue

            # Add dimension - all dimensions are scalars
            self.dimensions.add(name=line, size=int(next(it)))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Lastly process the parameters
        for line in it:
            if line == VAR_DELIM:
                continue
            varname = line.split(' ')[0]
            # if self.__verbose:   # pragma: no cover
            #     print(f'{varname=}')

            # Add the parameter
            try:
                self.add(name=varname)
            except ParameterExistsError:
                if self.__verbose:   # pragma: no cover
                    con.print(f'[bold]{varname}[/]: updated with new values')
                self.__updated_parameters.add(varname)
            except ParameterNotValidError:
                if self.__verbose:   # pragma: no cover
                    con.print(f'[bold]{varname}[/]: [gold3]is not a valid parameter; skipping. [/]')

                # Skip to the next parameter
                try:
                    while next(it) != VAR_DELIM:
                        pass
                except StopIteration:
                    # Hit end of file
                    pass
                continue

            # Read the dimension names
            ndims = int(next(it))  # number of dimensions for this variable
            dim_names = [next(it) for _ in range(ndims)]

            # Total dimension size declared for parameter in file; it should equal the size of
            # the declared global dimensions.
            dim_size = int(next(it))

            # The datatype
            param_dtype = int(next(it))

            if self.get(varname).is_scalar:
                vals = np.array(next(it), dtype=PTYPE_TO_DTYPE[param_dtype])
            else:
                # Arrays of strings should be objects
                if param_dtype == 4:
                    vals = np.zeros(dim_size, dtype=object)
                else:
                    vals = np.zeros(dim_size, dtype=PTYPE_TO_DTYPE[param_dtype])

                for idx in range(0, dim_size):
                    # NOTE: string-float to int works but float to int does not
                    vals[idx] = next(it)

            # Make sure there are not any more values in the file
            try:
                cnt = dim_size
                while True:
                    cval = next(it)
                    if cval[0:4] == VAR_DELIM or cval.strip() == '':
                        break
                    cnt += 1

                if cnt > dim_size:
                    print(f'WARNING: Too many values specified for {varname}')
                    print(f'         {dim_size} expected, {cnt} given')
                    print('          Removing parameter')

                    self.remove(varname)
                    continue
            except StopIteration:
                # Hit the end of the file
                pass

            self.get(varname).data = vals    # type: ignore

        self.adjust_bounded_parameters()
        self.__isloaded = True
