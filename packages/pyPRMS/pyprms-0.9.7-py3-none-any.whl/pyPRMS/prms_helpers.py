from typing import Iterator, List, Optional, Set, Union

import datetime
import operator
import os
import pandas as pd   # type: ignore
import networkx as nx   # type: ignore
import numpy as np
import re
import xml.etree.ElementTree as xmlET

# from .constants import Version   # type: ignore

cond_check = {'=': operator.eq,
              '>': operator.gt,
              '<': operator.lt}


def flex_type(val: Union[str, int, float, np.float32, np.float64, np.int32, np.int64]) -> str:
    """Convert the given value to a string.

    :param val: Value to convert to a string

    :returns: String representation of the value
    """

    if isinstance(val, (np.float32, np.float64, np.int32, np.int64, np.str_)):
        val = val.item()

    if isinstance(val, str):
        return val

    if isinstance(val, int):
        return repr(val)

    if isinstance(val, float):
        if np.isinf(val):
            raise ValueError('Infinite floating point value')

        return np.format_float_positional(val, precision=20, trim='0')


def get_file_iter(filename: Union[str, os.PathLike]) -> Iterator[str]:
    """Reads a file and returns an iterator to the data

    :param filename: Name of the file to read
    :returns: Iterator to the file data
    """

    infile = open(filename, 'r')
    rawdata = infile.read().splitlines()
    infile.close()

    return iter(rawdata)


def get_streamnet_subset(dag_ds: nx.classes.digraph.DiGraph,
                         uscutoff_seg: List[int],
                         dsmost_seg: List[int]) -> nx.classes.digraph.DiGraph:
    """Extract subset of a stream network

    :param dag_ds: Directed, acyclic graph of downstream stream network
    :param uscutoff_seg: List of upstream cutoff segments
    :param dsmost_seg: List of outlet segments to start extraction from

    :returns: Stream network of extracted segments
    """
    # Create the upstream graph
    # TODO: 2021-12-01 PAN - the reverse function is pretty inefficient for multi-location
    #       jobs.
    dag_us = dag_ds.reverse()
    # logger.debug('Number of NHM upstream nodes: {}'.format(dag_us.number_of_nodes()))
    # logger.debug('Number of NHM upstream edges: {}'.format(dag_us.number_of_edges()))

    # Trim the u/s graph to remove segments above the u/s cutoff segments
    try:
        for xx in uscutoff_seg:
            try:
                dag_us.remove_nodes_from(nx.dfs_predecessors(dag_us, xx))

                # Also remove the cutoff segment itself
                dag_us.remove_node(xx)
            except KeyError:
                print(f'WARNING: nhm_segment {xx} does not exist in stream network')
    except TypeError:
        print('\nSelected cutoffs should at least be an empty list instead of NoneType.')
        # logger.error('\nSelected cutoffs should at least be an empty list instead of NoneType.')
        # exit(200)

    # logger.debug('Number of NHM upstream nodes (trimmed): {}'.format(dag_us.number_of_nodes()))
    # logger.debug('Number of NHM upstream edges (trimmed): {}'.format(dag_us.number_of_edges()))

    # =======================================
    # Given a d/s segment (dsmost_seg) create a subset of u/s segments

    # Get all unique segments u/s of the starting segment
    uniq_seg_us: Set[int] = set()
    if dsmost_seg:
        for xx in dsmost_seg:
            try:
                pred = nx.dfs_predecessors(dag_us, xx)
                uniq_seg_us = uniq_seg_us.union(set(pred.keys()).union(set(pred.values())))
            except KeyError:
                # logger.error('KeyError: Segment {} does not exist in stream network'.format(xx))
                print(f'KeyError: Segment {xx} does not exist in stream network')

        # Get a subgraph in the dag_ds graph and return the edges
        dag_ds_subset = dag_ds.subgraph(uniq_seg_us).copy()

        # 2018-02-13 PAN: It is possible to have outlets specified which are not truly
        #                 outlets in the most conservative sense (e.g. a point where
        #                 the stream network exits the study area). This occurs when
        #                 doing headwater extractions where all segments for a headwater
        #                 are specified in the configuration file. Instead of creating
        #                 output edges for all specified 'outlets' the set difference
        #                 between the specified outlets and nodes in the graph subset
        #                 which have no edges is performed first to reduce the number of
        #                 outlets to the 'true' outlets of the system.
        node_outlets = [ee[0] for ee in dag_ds_subset.edges()]
        true_outlets = set(dsmost_seg).difference(set(node_outlets))
        # logger.debug('node_outlets: {}'.format(','.join(map(str, node_outlets))))
        # logger.debug('true_outlets: {}'.format(','.join(map(str, true_outlets))))

        # Add the downstream segments that exit the subgraph
        for xx in true_outlets:
            nhm_outlet = list(dag_ds.neighbors(xx))[0]
            dag_ds_subset.add_node(nhm_outlet, style='filled', fontcolor='white', fillcolor='grey')
            dag_ds_subset.add_edge(xx, nhm_outlet)
            dag_ds_subset.nodes[xx]['style'] = 'filled'
            dag_ds_subset.nodes[xx]['fontcolor'] = 'white'
            dag_ds_subset.nodes[xx]['fillcolor'] = 'blue'
    else:
        # No outlets specified so pull the CONUS
        dag_ds_subset = dag_ds

    return dag_ds_subset


def read_xml(filename: str) -> xmlET.Element:
    """Returns the root of the xml tree for a given file.

    :param filename: XML filename

    :returns: Root of the xml tree
    """

    # Open and parse an xml file and return the root of the tree
    xml_tree = xmlET.parse(filename)
    return xml_tree.getroot()


def set_date(adate: Union[datetime.datetime, datetime.date, str, np.ndarray]) -> datetime.datetime:
    """Return datetime object given a datetime or string of format YYYY-MM-DD

    :param adate: Datetime object or string (YYYY-MM-DD)
    :returns: Datetime object
    """

    if isinstance(adate, datetime.datetime):
        return adate
    elif isinstance(adate, datetime.date):
        return datetime.datetime.combine(adate, datetime.time.min)
    elif isinstance(adate, np.ndarray):
        return datetime.datetime(*adate)
    else:
        return datetime.datetime(*[int(x) for x in re.split('[- :]', adate)])  # type: ignore


# def version_info(version_str: Optional[str] = None,
#                  delim: Optional[str] = '.') -> Version:
#     """Given a version string (MM.mm.rr) returns a named tuple of version values
#
#     :param version_str: Version string
#     :param delim: Delimiter for version string
#
#     :returns: Named tuple of version values
#     """
#
#     # Version = NamedTuple('Version', [('major', Union[int, None]),
#     #                                  ('minor', Union[int, None]),
#     #                                  ('revision', Union[int, None])])
#     flds: List[Union[int, None]] = [None, None, None]
#
#     # TODO: 2025-01-27 PAN - if first character == delim then raise an error
#     if version_str is not None:
#         for ii, kk in enumerate(version_str.split(delim)):
#             flds[ii] = int(kk)
#
#     return Version(flds[0], flds[1], flds[2])


# def version_info(version_str: Optional[str] = None, delim: Optional[str] = '.') -> NamedTuple:
#
#     Version = namedtuple('Version', ['major', 'minor', 'revision'])
#
#     if version_str is None:
#         return Version(0, 0, 0)
#
#     flds = [int(kk) for kk in version_str.split(delim)]
#
#     return Version(flds[0], flds[1], flds[2])

# def dparse(*dstr: Union[Sequence[str], Sequence[int]]) -> datetime:
#     """Convert date string to datetime.
#
#     This function is used by Pandas to parse dates.
#     If only a year is provided the returned datetime will be for the last day of the year (e.g. 12-31).
#     If only a year and a month is provided the returned datetime will be for the last day of the given month.
#
#     :param dstr: year, month, day; or year, month; or year
#
#     :returns: datetime object
#     """
#
#     dint: List[int] = list()
#
#     for xx in dstr:
#         if isinstance(xx, str):
#             dint.append(int(xx))
#         elif isinstance(xx, int):
#             dint.append(xx)
#         else:
#             raise TypeError('dparse entries must be either string or integer')
#     # dint = [int(x) if isinstance(x, str) else x for x in dstr]
#
#     if len(dint) == 2:
#         # For months we want the last day of each month
#         dint.append(calendar.monthrange(*dint)[1])
#     if len(dint) == 1:
#         # For annual we want the last day of the year
#         dint.append(12)
#         dint.append(calendar.monthrange(*dint)[1])
#
#     # return pd.to_datetime(dint)
#     return pd.to_datetime('-'.join([str(d) for d in dint]))
