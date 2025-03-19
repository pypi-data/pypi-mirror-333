r"""
Functions for manipulating strings and dictionaries, also a bit of IO.


.. currentmodule:: mdciao.utils.str_and_dict


Functions
=========

.. autosummary::
   :toctree: generated/

"""
from glob import glob as _glob
import numpy as _np
import mdtraj as _md
from .lists import re_warp, contiguous_ranges as _cranges
from fnmatch import fnmatch as _fnmatch
from pandas import read_excel as _read_excel
from os import path as _path, listdir as _ls
import re as _re
from collections import defaultdict as _defdict
from natsort import natsorted as _natsorted
from inspect import signature as _signature, getfullargspec as _getfullargspec

import docstring_parser as _dsp
try:
    from matplotlib import docstring as _mpldocstring
except ImportError:
    from matplotlib import _docstring as _mpldocstring
from textwrap import wrap as _twrap


tunit2tunit = {"ps":  {"ps": 1, "ns": 1e-3, "mus": 1e-6, "ms":1e-9},
                "ns":  {"ps": 1e3, "ns": 1,    "mus": 1e-3, "ms":1e-6},
                "mus": {"ps": 1e6, "ns": 1e3,  "mus": 1,    "ms":1e-3},
                "ms":  {"ps": 1e9, "ns": 1e6,  "mus": 1e3,  "ms":1},
               }

def _kwargs_docstring(obj, exclude=None) -> str:
    r""" Return the formatted docstring of a callable object's keyword arguments.

    Also returns the docstring for the `obj`'s **kwargs in case obj also has **kwargs itself.

    Parameters
    ----------
    obj : callable
        The method or class whose docstring will be extracted
    exclude : list, default is None
        A list of argument names (strings). Arguments of `obj`
        matching those in `exclude` will be excluded from
        the returned docstring.

    Returns
    -------
    docstring :  str
        A string with the docstring of obj and obj's inherited
        **kwargs. The docstring is formatted with tabs and linebreaaks
        already.
    """

    # Get the info
    sig = _signature(obj)
    fas = _getfullargspec(obj)
    ds_params = _dsp.parse(obj.__doc__).params

    if exclude is None:
        exclude=[]

    to_add_idxs = {"own":[], "**kwargs" : []}
    to_add_names = {"own" : [], "**kwargs" : []}
    #Iterate over the parameters inferred via docstring only
    for ii, par in enumerate(ds_params):
        if par.arg_name not in exclude+[fas.varkw]:

            # First case: we're adding the method's own optional parameters
            # These satisfy that 1.1) they are in the signature
            if par.arg_name in sig.parameters.keys():
                # and 1.2) they're optional
                if "=" in str(sig.parameters[par.arg_name]) or sig.parameters[par.arg_name].kind.value == 3:
                    # and 1.3) they have not been added before.
                    # This excludes inherited **kwargs that have been added to the obj's docstring and
                    # have the same name as one of the method's own kwargs. These will most likely have been exlucded
                    # via the exclude param of the decorator
                    if par.arg_name not in to_add_names["own"]:
                        to_add_idxs["own"].append(ii)
                        to_add_names["own"].append(par.arg_name)
            # Second case: we're adding the method's inherited kwargs, we check that
            # 2.1) they're NOT in the signature (hence the else)
            else:
                assert fas.varkw is not None # 2.2) we actually have **kwargs in obj
                assert all([ii>jj for jj in to_add_idxs["own"]]) # 2.3) this kwarg comes after the 'own' kwargs in the docstring
                to_add_idxs["**kwargs"].append(ii)
                to_add_names["**kwargs"].append(par.arg_name)

    picked_params =  [ds_params[ii] for ii in to_add_idxs["own"]+to_add_idxs["**kwargs"]]
    pikced_params_names = to_add_names["own"]+to_add_names["**kwargs"]

    # Check the above case-logic hasn't lead to dupes, bhould be covered by 1.3), but still
    assert len(pikced_params_names)==len(_np.unique(pikced_params_names)), (obj, sig, to_add_names, pikced_params_names)

    # Time to patch the docstring together
    params = ""
    for par in picked_params:
        line = f"{par.arg_name} : {par.type_name}\n"
        line += ''.join(['\t%s\n' % (desc) for desc in par.description.splitlines()])
        params += line.expandtabs(4)
    assert params != ''

    return params

def _kwargs_subs(funct_or_method, exclude=None):
    r"""Substitute the expression 'kwargs docstrings' in the decorated method with those of `funct_or_method`

    Will substitute the expression "%(substitute_kwargs)s" anywhere in the
    docstring of the method it decorates with the optional parameter
    docstring of funct_or_method

    Parameters
    ----------
    funct_or_method : method or function
    exclude : list, default is None
        A list of argument names (strings). Arguments of `obj`
        matching those in `exclude` will be excluded from
        the returned docstring.

    Returns
    -------
    dec : mpldocstring.Substitution object
    """

    return _mpldocstring.Substitution(
        substitute_kwargs=_kwargs_docstring(funct_or_method, exclude=exclude))

def get_trajectories_from_input(trajectories):
    r"""
    Common parser for something that can be interpreted as a trajectory

    Parameters
    ----------
    trajectories: can be one of these things:
        * pattern, e.g. "*.ext"
        * one single string containing a filename
        * one single :obj:`mdtraj.Trajectory` object
        * one list containing
         * just filenames
         * just :obj:`mdtraj.Trajectory` objects
         * a mix of filenames and :obj:`mdtraj.Trajectory` objects

    Returns
    -------
    outtrajs : list
        A list of trajectories. This list can be, depending on the input:
        * for an input pattern: sorted trajectory filenames that match that pattern
        * for filename or an :obj:`mdtraj.Trajectory`:
        one list containing that filename or :obj:`mdtraj.Trajectory` object
        * for a list, that same list (i.e. nothing happens)

    """
    if isinstance(trajectories,str):
        _trajectories = _natsorted(_glob(trajectories))
        if len(_trajectories)==0:
            nl = 'n' # https://stackoverflow.com/a/44780467
            raise FileNotFoundError(f"Couldn't find (or pattern-match) anything to '{trajectories}'.\n"
                                    f"ls $CWD[{_path.abspath(_path.curdir)}]:\n"
                                    f"{nl.join(sorted(_ls(_path.curdir)))}")
        else:
            trajectories=_trajectories

    if type(trajectories) in [_md.Trajectory, str]:
        outtrajs = [trajectories]
    else:
        assert all([type(itraj) in [_md.Trajectory, str] for itraj in trajectories])
        outtrajs = trajectories

    return outtrajs

def inform_about_trajectories(trajectories, only_show_first_and_last=False):
    r"""
    Return a string that informs about the trajectories

    Parameters
    ----------
    trajectories: list of strings or :obj:`mdtraj.Trajectory` objects


    Returns
    -------
    listed_str : a string with the trajectory names separated by newlines

    """
    ntraj = len(trajectories)
    assert isinstance(trajectories, list), "input has to be a list"
    if isinstance(only_show_first_and_last,int) and only_show_first_and_last*2<ntraj:
        n = only_show_first_and_last
        _trajectories =trajectories[:n]+["...[long list: omitted %u items]..."%(ntraj-2*n)]+trajectories[-n:]

    else:
        _trajectories = trajectories
    return "\n".join([str(itraj) for itraj in _trajectories])

def replace_w_dict(input_str, exp_rep_dict):
    r"""
    Sequentially perform string replacements on a string using a dictionary

    Parameters
    ----------
    input_str: str
    exp_rep_dict: dictionary
        keys are expressions that will be replaced with values, i.e.
        key = key.replace(key1, val1) for key1, val1 etc

    Returns
    -------
    key

    """
    for pat, exp in exp_rep_dict.items():
        input_str = input_str.replace(pat, exp)
    return input_str

def delete_exp_in_keys(idict, exp, sep="-"):
    r"""
    Assuming the keys in the dictionary are formed by two segments
    joined by a separator, e.g. "GLU30-ARG40", deletes the segment
    containing the input expression, :obj:`exp`

    Will fail if not all keys have the expression to be deleted

    Parameters
    ----------
    idict: dictionary
    exp: str
    sep: str, default is "-",

    Returns
    -------
    dict:
        dictionary with the same values but the keys lack the
        segment containing :obj:`exp`

    dhk : list
        List with the deleted half-keys
    """

    out_dict = {}
    deleted_half_keys=[]
    for names, val in idict.items():
        new_name, dhk = delete_pattern_in_ctc_label(exp,names,sep)
        deleted_half_keys.extend(dhk)
        out_dict[new_name]=val
    return out_dict,deleted_half_keys

def delete_pattern_in_ctc_label(pattern, label, sep):
    new_name = [name for name in splitlabel(label, sep) if pattern not in name]
    deleted_half_keys = [name for name in splitlabel(label,sep) if pattern in name]
    assert len(new_name) == 1, (new_name, pattern)
    return new_name[0], deleted_half_keys

# Order key alphabetically using the separator_key
def order_key(key, sep):
    split_key = splitlabel(key,sep)
    return sep.join([split_key[ii] for ii in _np.argsort(split_key)])

def print_wrap(text, width=100, just_return_string=False,**kwargs):
    r"""
    Print the `text` wrapping the lines to a given character `width`

    Parameters
    ----------
    text : str
        The text to wrap
    width : int, default is 100
        The maximum number of characters per line
    just_return_string : bool, default is False
        Instead of printing, just return the string
    kwargs: dict, optional
        Keyword arguments for print()

    """
    istr = "\n".join(_twrap(text, width))
    if just_return_string:
        return istr
    else:
        print(istr,**kwargs)

def unify_freq_dicts(freqs,
                     exclude=None,
                     key_separator="-",
                     replacement_dict=None,
                     defrag=None,
                     per_residue=False,
                     is_freq=True,
                     val_missing=0,
                     verbose=True
                     ):
    r"""
    Provided with a dictionary of dictionaries, returns an equivalent,
    key-unified dictionary where all sub-dictionaries share their keys,
    putting zeroes where keys where absent originally.

    Use :obj:`key_separator` for "GLU30-LY40" == "LYS40-GLU30" to be True

    Parameters
    ----------
    freqs:  dictionary of dictionaries, e.g.:
        {A:{key1:valA1, key2:valA2, key3:valA3},
         B:{            key2:valB2, key3:valB3}}
    key_separator: str, default is "-"
        Specify how residues are separated in the contact
        label, eg. "GLU30-LYS40".
        With this knowledge, the method can split the label
        before comparison so that "GLU30-LYS40" is considered
        equal to "LYS40-GLU30". Use "", "none" or None to differentiate.
        It will also be passed to :obj:`defrag_key` in case
        :obj:`defrag` is not None.
    exclude: list, default is None
         keys containing these strings will be excluded.
         NOTE: This is not implemented yet, will raise an error
    replacement_dict: dict, default is {}
        all keys/strings will be subjected to replacements following this
        dictionary, st. "GLH30" is "GLU30" if replacement_dict is {"GLH":"GLU"}
        This way mutations and or indexing can be accounted for in different setups
    defrag : char, default is None
        If a char is given, "@", anything after that character in the labels
        will be consider fragment information and ignored. This is only recommended
        for advanced users, usually the fragment information helps keep track
        of residue names in complex topologies:
            R201@frag1 and R201@frag3 will both be "R201"
    per_residue : bool, default is False
        Aggregate interactions to their residues
    is_freq : bool, default is True
        If the dictionaries actually
        contain frequencies or not.
        If not, some checks are omitted
    val_missing : anything, default is 0
        What value to assign to the
        missing keys (TODO check the name of this in pandas)
    verbose : bool, default is True
        Be verbose


    Returns
    -------
    unified_dict: dictionary
        A dictionary  of dictionaries sharing keys:
       {A:{key1:valA1, key2:valA2, key3:valA3},
        B:{key1:0,     key2:valB2, key3:valB3}}
    """

    # Create a copy
    freqs_work = {key : {key2: val for key2, val in idict.items()} for key, idict in freqs.items()}

    # Enforce replacement dictionaries
    if replacement_dict is not None:
        freqs_work = {key: {replace_w_dict(key2, replacement_dict): val2 for key2, val2 in val.items()} for key, val in
                      freqs_work.items()}

    #Re - ordered keys if needed
    if str(key_separator).lower() != "none" and len(key_separator) > 0:
        freqs_work = {key : {order_key(key2, key_separator): val2 for key2, val2 in idict.items()} for key, idict in freqs_work.items()}

    if defrag is not None:
        freqs_work = {key:{defrag_key(key2, defrag):val2 for key2, val2 in val.items()} for key, val in freqs_work.items()}

    if per_residue:
        freqs_work = {key:sum_dict_per_residue(val, key_separator) for key, val in freqs_work.items()}

    # Perform the difference operations
    not_shared = []
    shared = []
    for idict1 in freqs_work.values():
        for idict2 in freqs_work.values():
            if not idict1 is idict2:
                not_shared += list(set(idict1.keys()).difference(idict2.keys()))
                shared += list(set(idict1.keys()).intersection(idict2.keys()))

    shared = list(_np.unique(shared))
    not_shared = list(_np.unique(not_shared))
    all_keys = shared + not_shared
    # Prune keys we're not interested in
    excluded = []
    if exclude is not None:
        raise NotImplementedError("This feature not yet implemented")
        """
        assert isinstance(exclude,list)
        print("Excluding")
        for ikey, ifreq in freqs_work.items():
            # IDK I had this condition here, i think it is more intuitive if
            # they are removed regardless if shared or not
            #for key in shared:
            for key in list(ifreq.keys()):
                for pat in exclude:
                    if pat in key:
                        ifreq.pop(key)
                        print("%s from %s" % (key, ikey))
                        print(ifreq.keys())
                        excluded.append(key)
                        #all_keys = [ak for ak in all_keys if ak != key]
        """

    # Set the non shared keys to zero
    for ikey, ifreq in freqs_work.items():
        for key in all_keys:
            if key not in ifreq.keys():
                ifreq[key] = val_missing

    if len(not_shared)>0 and is_freq and verbose:
        print("These interactions are not shared:\n%s" % (', '.join(not_shared)))
        print("Their cumulative ctc freq is %3.2f. " % _np.sum(
            [[ifreq[key] for ifreq in freqs_work.values()] for key in not_shared]))

    return freqs_work

@_kwargs_subs(unify_freq_dicts)
def average_freq_dict(freqs,
                      weights=None,
                      **unify_freq_dicts_kwargs
                     ):
    r"""
    Average frequencies (or anything) over dictionaries.

    Typically, the input :obj:`freqs` are keyed first by system,
    then by contact label, e.g. {"T300":{"GDP-R201":1.0},
                                "T320":{"GDP-R201":.25},
                                "MUT":{"GDP-L201":25}}

    The input data need not be unified, the method calls
    :obj:`unify_freq_dicts` internally. In the example above
    you have to call it with the arg replacement_dict={"L201:R201"}
    so tha it can understand that mutation when unifying


    Parameters
    ----------
    freqs : dict of dicts
        The dictionaries containing frequence dictionaries,

    weights : dict, default is None
        relative weights of each dictionary

    unify_freq_dicts_kwargs : Optional keyword args for :obj:`~mdciao.utils.str_and_dict.unify_freq_dicts`
        as listed below

    Other Parameters
    ----------------
    %(substitute_kwargs)s

    Returns
    -------
    averaged_dict : dict
        an averaged dictionary keyed only with the


    """
    freqs_work = unify_freq_dicts(freqs,**unify_freq_dicts_kwargs)

    sys_keys = list(freqs_work.keys())
    frq_keys = list(freqs_work[sys_keys[0]].keys())
    averaged_dict = {}
    if weights is None:
        weights = {key:1 for key in sys_keys}
    for fk in frq_keys:
        averaged_dict[fk] = _np.average([freqs_work[isys][fk] for isys in sys_keys],
                                        weights=[weights[isys] for isys in sys_keys])

    return averaged_dict

def sum_dict_per_residue(idict, sep):
    r"""Return a "per-residue" sum of values from a "per-residue-pair" keyed dictionary

    Note:
    There is a closely related method in :obj:`mdciao.contacts.ContactGroup`
    that allows to query the freqs from the object already aggregated
    by residue. This is for when the object is either not accessible, e.g.
    because the freqs were loaded from a file

    Parameters
    ----------
    idict : dict
        Keyed with contact labels like "res1@frag1-res2@3.50" etc
    sep : char
        Character that separates fragments in the label

    Returns
    -------
    aggr : dict
        keyed with "res1@frag1" etc

    """
    out_dict = _defdict(list)
    for key, freq in idict.items():
        key1, key2 = splitlabel(key, sep) #This will fail if sep is not in key or sep does not separate in two
        out_dict[key1].append(freq)
        out_dict[key2].append(freq)
    return {key:_np.sum(val) for key, val in out_dict.items()}

def sort_dict_by_asc_values(idict, reverse=False):
    r""" Sort a dictionary by ascending values

    Parameters
    ----------
    idict : dict
        Input dictionary
    reverse : bool, default is False
        Reverse the sorting order,
        i.e. sort by descending order
        of values

    Returns
    -------
    odict : dict
        Indict sorted with its keys
         sorted by its values
    """
    return {key: val for key, val in sorted(idict.items(), key=lambda item: item[1], reverse=reverse)}

def lexsort_ctc_labels(ctc_labels, reverse=False, columns=[0,1], sep="-") -> tuple:
    r"""
    Sort contact-labels in ascending order of resSeq using both columns

    Wraps around :obj:`numpy.lexsort` with some string handling.

    It will also work with contact-labels consisting of only one residue,
    e.g. in the cases where the "anchor" has been deleted or the frequencies
    have been aggregated to per-residue frequencies

    >>> labels = ["ALA30@3.50-GLU50",
    >>>           "HIS28-GLU50",
    >>>           "ALA30-GLU20"]
    >>> sorted_labels, order = mdciao.utils.str_and_dict.lexsort_ctc_labels(labels)
    >>> sorted_ctc_labels
    >>> ['HIS28-GLU50',
    >>>  'ALA30-GLU20',
    >>>  'ALA30@3.50-GLU50']

    Parameters
    ----------
    ctc_labels : list or np.ndarray
        Strings describing the contact
        residues. It can contain also
        fragment information, which
        will be ignored when sorting
        but returned in :obj:`sorted_ctc_labels`
    reverse : bool, default is False
        If True, sort in descending
        order, instead of ascending
    columns : list
        The order of the columns,
        e.g. [0,1] means sort first
        by first column (idx 0),
        then by second column (idx 1).
    sep : char, default is "-"
        The character to use
        when separating the
        contact label into both residues

    Returns
    -------
    sorted_ctc_labels : list
        The sorted contact labels
    order : 1D np.ndarray
        The indices of :obj:`ctc_labels` that
        sort it into :obj:`sorted_ctc_labels`
    """
    resSeqs = _np.vstack(
        [[intblocks_in_str(pp)[0] for pp in splitlabel(lab,sep)] for lab in ctc_labels])

    if resSeqs.shape[1]==1:
        order = _np.argsort(resSeqs.squeeze())
    else:
        order = _np.lexsort([resSeqs[:, columns[1]], resSeqs[:, columns[0]]])
    if reverse:
        order=order[::-1]
    sorted_ctc_labels = [ctc_labels[ii] for ii in order]
    return sorted_ctc_labels, order

def freq_file2dict(ifile, defrag=None):
    r"""
    Read a file containing the frequencies ("freq") and labels ("label")
    of pre-computed contacts

    Parameters
    ----------
    ifile : str
        Path to file, can be a .xlsx, .dat, .txt

    defrag : str, default is None
        If passed a string, e.g "@", the fragment information
        of the contact label will be deleted upon reading,
        so that R131@frag1 becomes R131. This is done
        by calling :obj:`defrag_key` internally

    Returns
    -------
    dict : keyed by labels and valued with frequencies, e.g .{"0-1":.3, "0-2":.1}

    """
    ext = _path.splitext(ifile)[-1]
    if ext.lower() == ".xlsx":
        df = _read_excel(ifile, engine="openpyxl")
        if "freq" in df.keys() and "label" in df.keys():
            res = {key: val for key, val in zip(df["label"].values, df["freq"].values)}
        else:
            row_lab, col_lab = _np.argwhere(df.values == "label").squeeze()
            row_freq, col_freq = _np.argwhere(df.values == "freq").squeeze()
            assert row_lab == row_freq,"File %s yields a weird dataframe on read \n%s"%(ifile,df)
            res = {key: val for key, val in zip(df.values[row_freq + 1:, col_lab].tolist(),
                                                 df.values[row_freq + 1:, col_freq].tolist())}
    else:
        res = freq_ascii2dict(ifile)
    if defrag is not None:
        res = {defrag_key(key, defrag=defrag):val for key, val in res.items()}

    return res

def freq_ascii2dict(ifile, comment="#"):
    r"""
    Reads an ASCII file that contains contact frequencies
    (1st column) and contact labels (2nd and/or 3rd column).
    Columns are separated by tabs or spaces.

    Contact labels have to come after the frequency in the
    form of "res1 res2, "res1-res2" or "res1 - res2",

    Columns other than the frequencies and the residue labels are ignored.

    Examples
    --------
    File produced by mdciao:

    >>> #freq              label              residue idxs  sum
    >>> 0.59 R389@G.H5.21    - L394@G.H5.26    348 353    0.59
    >>> 0.46 L394@G.H5.26    - K270@6.32x32    353 972    1.05
    >>> 0.34 L388@G.H5.20    - L394@G.H5.26    347 353    1.39
    >>> 0.32 L394@G.H5.26    - L230@5.69x69    353 957    1.71
    >>> 0.04 R385@G.H5.17    - L394@G.H5.26    344 353    1.75

    Minimal file with mixed labeling

    >>> 1 ALA30-GLU50
    >>> .5 ASP31 - GLU51
    >>> .1 ASP31 GLU50


    TODO use pandas to allow more flex, not needed for the moment

    Parameters
    ----------
    ifile : str
        The filename to be read
    comment : str, default is '#'
        Any line starting with any of these
        characters will be ignored
    Returns
    -------
    freqdict : dictionary
        Keys are "res1-res2" (regardless of input)
        and values are freqs

    """
    #TODO consider using pandas
    outdict = {}
    with open(ifile) as f:
        for iline in f.read().splitlines():
            if iline.strip()[0] not in comment and len(iline)>0:
                try:
                    iline = iline.replace("-"," ").split()
                    freq, names = float(iline[0]),"%s-%s"%(iline[1],iline[2])
                    outdict[names]=float(freq)
                except ValueError:
                    print(iline)
                    raise
    return outdict

_symbols =  ['alpha','beta','gamma', 'mu', "Sigma"]+["AA"]
_scripts =  ["^","_"]


def replace4latex(istr,
                  sindex=["_", "^"],
                  symbols=["alpha", "beta", "gamma", "sigma", "mu", "aa"],
                  enclose_pure_text=False
                  ):
    r"""
    Return a string where symbols and super/sub-indices have been prepared for LaTeX

    One quirk: when sub- or superindexing, the following
    types get protected in curly brackets to
    avoid only sub/super indexing the first character:

     * fully numeric: C_{300}
     * fully alphabetical: GLY_{ACE}
     * containing dots: L394^{G.H.26}

    BUT mixed \beta_2AR are left unprotected:

    >>> replace4latex("mdciao can alpha Sigma_2 beta2AR ACE_GLY GLU30^3.50 no [frag1-WT] problem!")
    'mdciao can $\\alpha$ $\\Sigma\\mathrm{_{2}}$ $\\beta\\mathrm{_2AR}$ $\\mathrm{{ACE}_{GLY}}$ $\\mathrm{GLU30^{3.50}}$ no [frag1-WT] problem!'


    Parameters
    ----------
    istr : str
        The string to be prepare for LaTeX mathmode
        If a $ sign is already in :obj:`istr`,
        nothing will happen
        If a word in :obj:`istr` contains
        the same :obj:`sindex` character more than
        once, it'll be skipped (ask [Knut](https://tex.stackexchange.com/questions/253080/why-am-i-getting-a-double-subscript-error))
    sindex : list
        The characters that indicate super- and sub-indices
    symbols : list
        The words that should be considered LaTeX symbols

    Returns
    -------
    lstr : str
        The string with LaTex-mathmode insertions
    """
    if "$" in istr:
        return istr
    pattern = " |" + "|".join(symbols)
    bits = [bit for bit in _re.split("(?i)(%s)" % pattern, istr.replace("\n", " ? ")) if len(bit) > 0]
    for ii in range(len(bits)):
        if bits[ii].lower() in symbols:
            bits[ii] = "$\%s$" % bits[ii]
        elif any([ss == bits[ii] for ss in sindex]):
            bits[ii] = "$%s$" % bits[ii]
        elif any([ss in bits[ii] for ss in sindex]):
            ibit = bits[ii]
            if any([ibit.count(ss)>1 for ss in sindex]):
                continue
            words = [word for word in _re.split("(%s)" % "|".join(["\%s" % ss for ss in sindex]), ibit)
                     if len(word) > 0]
            for ww in range(len(words)):
                word = words[ww]
                if word.isnumeric() or word.isalpha() or "." in word and word not in sindex: #Also gets 3.50
                    words[ww] = "{%s}" % word
            ibit = "".join(words)
            bits[ii] = "$\mathrm{%s}$" % ibit
        else:
            if enclose_pure_text and any([c.isalpha()  for c in bits[ii]]):
                bits[ii] = "$\mathrm{%s}$" % bits[ii]

    return "".join(bits).replace("$$", "").replace(" ? ","\n")

def _replace_regex_special_chars(word,
                                 repl_char="!",
                                 special_chars=["^", "[", "]", "(", ")"]):
    r"""
    Ad-hoc method to replace special regexp-chars with something else before
    computing char positions using regexp.finditer

    Note:
    this method only makes sense because downstream from here, finditer is used
    to search a substring in a string and special chars break that search.

    Note:
    somewhere, a dev that knows how to use regex is crying

    Parameters
    ----------
    word : str
    repl_char : char, default is '!'
        The replacement character
    special_chars : list
        The characters that trigger replacement

    Returns
    -------
    word : str
        A string with all special characters repaced with :obj:`repl_char`

    """
    for sp in special_chars:
        word = word.replace(sp, repl_char)
    return word

def latex_mathmode(istr, enclose=True):
    r"""
    Prepend *symbol* words with "\\ " and protect *non-symbol* words with '\\mathrm{}'

    * *symbol* words are things that can
      be interpreted by LaTeX in math mode, e.g.
      '\\alpha' or '\\AA'
    * *non-symbol* words are everything else

    Works "opposite" to :obj:`replace4latex` and for the moment
    it's my (very bad) solution for latexifying contact-labels' fragments
    as super indices where the fragments themselves contain
    sub-indices (GLU30^$\beta_2AR}


    >>> replace4latex("There's an alpha and a beta here, also C_200")
    "There's an $\alpha$ and a $\beta$ here, also $C_{200}$"

    >>> latex_mathmode("There's an alpha and a beta here, also C_200")
    "$\\mathrm{There's an }\\alpha\\mathrm{ and a }\\beta\\mathrm{ here, also C_200}$"

    Parameters
    ----------
    istr : string
    enclose : bool, default is True
        Return string enclosed in
        dollar-signs: '$string$'
        Use False for cases where
        the LaTeX math-mode is already
        active

    Returns
    -------
    istr : string
    """
    output = []
    exp = "(%s)" % "|".join(["\%s" % ss if ss == "^" else "%s" % ss for ss in _symbols])
    for word in _re.split(exp, istr):
        if len(word) > 0:
            if word in _symbols:
                word = "\\%s" % word
            else:
                word = "\\mathrm{%s}" % word
            output.append(word)
    output = "".join(output)
    if enclose:
        output= "$%s$"%output
    return output

def latex_superscript_fragments(contact_label, defrag="@"):
    r"""
    Format fragment descriptors as Latex math-mode superscripts

    Thinly wrap around :obj:`_latex_superscript_one_fragment` with :obj:`splitlabel`

    Parameters
    ----------
    contact_label : str
        contact label of any form,
        as long as to AAs are joined
        with '-' character
    defrag : char, default is '@'
        The character to divide
        residue and fragment label
    Returns
    -------
    contact_label : str

    """
    return '-'.join(_latex_superscript_one_fragment(w, defrag=defrag) for w in splitlabel(contact_label, "-"))

def _latex_superscript_one_fragment(label, defrag="@"):
    r"""
    Format s.t. the fragment descriptor appears as superindex in LaTeX math-mode

    Parameters
    ----------
    label : str
        Contact label, "GLU30" and
        optionally "GLU30@beta_2AR"
    defrag : char, default is '@'
        The character to divide
        residue and fragment label

    Returns
    -------
    label : str
    """
    words = label.split(defrag,maxsplit=1)
    if len(words)==1:
        return label
    elif len(words)==2:
        return words[0]+"$^{%s}$" %replace4latex(words[1], enclose_pure_text=True).replace("$","")

def _label2componentsdict(istr,sep="-",defrag="@",
                          dont_split=None,
                          assume_ctc_label=True):
    r"""
    Identify the components of label like 'residue1@frag1-residue2@frag2' and return them as dictionary

    Parameters
    ----------
    istr : str
        Can be of any of these forms:
        * res1
        * res1@frag1
        * res1@frag1-res2
        * res1@frag1-res2@frag2
        * res1-res2@frag2
        * res1-res2

        The fragment names can contain the separator, e.g.
        'res1@B2AR-CT-res2@Gprot' is possible, but residue
        names cannot.

        The special case 'res1@frag1-r2' is handled with
        the parameter :obj:`assume_ctc_label` (see below)

        Labels have to start with a residue.
    sep : char, default is "-"
        The character that separates pairs of labels
    defrag : char, default is "@"
        The character that separates residues form their host fragment
    dont_split : list, default is None
        The strings in this list won't be separated
        even if they contain the separator. If the user
        knows that residue names like the ion "Cl-" or the
        ligand "DRG-1" might come up, they can "protect" them
        from splitting via this list.
    assume_ctc_label : bool, default is True
        In special cases of the form 'res1@frag1-r2', assume
        this is a contact label, i.e. 'r2' does not
        belong to the name of the fragment of res1, but is
        the second residue.

    Returns
    -------
    label : dict
        A dictionary tuple with the components present in :obj:`istr`.
        Keys can be 'res1','frag1','res2','frag2'
    """
    assert len(sep)==len(defrag)==1, "The 'sep' and 'defrag' arguments have to have both len 1, have " \
                                     "instead %s (%u) %s (%u)"%(sep,len(sep),defrag,len(defrag))

    bits = {}
    if dont_split is not None:
        rep_dict = {val : val.replace(sep,"{}") for val in dont_split} # alt use a random string
        istr = replace_w_dict(istr,rep_dict)
    if defrag not in istr:
        for ii, ires in enumerate(istr.split(sep),start=1):
            bits["res%u"%ii]=ires
    else:
        spans = [0] + _np.hstack([m.span() for m in _re.finditer(defrag, istr)]).tolist() + [len(istr)]

        # Counters
        r, f = 1, 1
        for ii, jj in _np.reshape(spans, (-1, 2)):
            iw = istr[ii:jj + 1]
            #print(iw, ii, jj)

            if sep in iw and ii == 0:
                ires, jres = iw.replace(defrag,"").split(sep)
                bits["res%u"%r]=ires
                r+=1
                bits["res%u"%r]=jres
                r+=1
                f+=1 # because we've already established res1 hasn't any fragment
            else:
                if defrag not in iw:
                    if sep not in iw or not assume_ctc_label:
                        bits["frag%u"%f]=iw
                        f+=1
                    elif sep in iw and assume_ctc_label:
                        ires, ifrag = [jw[::-1] for jw in iw[::-1].split(sep, 1)]
                        if "res1" in bits.keys():
                            if "frag1" in bits.keys():
                                bits["frag%u"%f]=iw
                                f+=1
                            else:
                                if "res2" in bits.keys():
                                    bits["frag%u" % f] = iw
                                else:
                                    bits["frag%u"%f]=ifrag
                                    f+=1
                                    bits["res%u"%r]=ires
                                    r+=1

                else:
                    assert iw.endswith(defrag)
                    if sep not in iw:
                        bits["res%u"%r]=iw.split(defrag)[0]
                        r+=1
                    else:
                        ires, ifrag = [jw[::-1] for jw in iw[::-1][1:].split(sep, 1)]
                        bits["frag%u"%f]=ifrag
                        bits["res%u"%r]=ires
                        f+=1
                        r+=1
    for key in bits.keys():
        bits[key] = bits[key].replace("{}",sep) #no need for full replacement dictonary

    return bits

def splitlabel(label, sep="-", defrag="@", dont_split=None):
    r"""
    Split a contact label. Analogous to label.split(sep) but more robust
    because fragment names can contain the separator character.

    Parameters
    ----------
    label : str
        Can be any of these forms:
         * res1
         * res1@frag1
         * res1@frag1-res2
         * res1@frag1-res2@frag2
         * res1-res2@frag2
         * res1-res2

        The fragment names can contain the separator, e.g.
        'res1@B2AR-CT-res2@Gprot' is possible. Residue
        names cannot contain the separator.

        The method assumes that labels start with a residue,
        (see above), else you'll get weird behaviour.
    sep : char, default is "-"
        The character that separates pairs of labels
    defrag : char, default is "@"
        The character that separates residues form their host fragment
    dont_split : list, default is None
        The strings in this list won't be separated
        even if they contain the separator. If the user
        knows that residue names like the ion "Cl-" or the
        ligand "DRG-1" might come up, they can "protect" them
        from splitting via this list.
    Returns
    -------
    split : list
        A list equivalent to having used label.split(sep)
        but the separator is ignored in the fragment labels.
    """

    bits = _label2componentsdict(label,sep=sep,defrag=defrag, dont_split=dont_split)

    split = [bits["res1"]]
    if "frag1" in bits.keys():
        split[0] += "%s%s" % (defrag,bits["frag1"])
    if "res2" in bits.keys():
        split.append(bits["res2"])
        if "frag2" in bits.keys():
            split[1] += "%s%s" % (defrag,bits["frag2"])
    return split

def intblocks_in_str(istr):
    r"""
    Return the integers that appear as contiguous blocks in strings.

    E.g.  "GLU30@3.50-GDP396@frag1" returns [30,3,50,396,1]

    Will raise a ValueError if `istr` doesn't contain any integers

    Related, but not the same as :obj:`~mdciao.utils.residue_and_atom.int_from_AA_code`


    Parameters
    ----------
    istr : string

    Returns
    -------
    ints : list or ValueError if `istr` doesn't have any integers in it

    """
    try:
        intblocks = _cranges([char.isdigit() for char in istr])[True]
        return [int("".join([istr[idx] for idx in block])) for block in intblocks]
    except KeyError as e:
        raise ValueError(f"'{istr}' doesn't contain any integers!")

def iterate_and_inform_lambdas(ixtc,chunksize, stride=1, top=None, nchars_fname=None):
    r"""
    Given a trajectory (as object or file), returns
    a strided, chunked iterator and function for progress report

    Parameters
    ----------
    ixtc: str (filename) or :obj:`mdtraj.Trajectory` object
    chunksize: int
        The trajectory will be iterated over in chunks of this many frames
    stride: int, default is 1
        The stride with which to iterate over the trajectory
    top:  str (filename) or :obj:`mdtraj.Topology`
        If :obj:`ixtc` is a filename, the topology needed to read it
    nchars_fname : int, default is None
        The number of characters for the filename field. By default
        it adjusts automatically, but it can be fixed here in case
        you want to use the same field width for many files.

    Returns
    -------

    iterate, inform

    iterate: lambda(ixtc)
        strided, chunked iterator over :obj:`ixtc`

    inform: lambda(ixtc, traj_idx, chunk_idx, running_f)
        iterator that returns a string informing on streaming progress for every iteration

    Note
    ----

    The lambdas returned differ depending on the type of input, but signature
    is the same, s.t. the user does not have to care in posterior use

    """
    if isinstance(ixtc, _md.Trajectory):
        iterate = lambda ixtc: (ixtc[idxs] for idxs in re_warp(_np.arange(ixtc.n_frames)[::stride], chunksize))
        inform = lambda ixtc, traj_idx, chunk_idx, running_f: \
            f"Streaming over trajectory object nr. {traj_idx :4} ({ixtc.n_frames :6} frames, {_np.ceil(ixtc.n_frames/stride) : 6} with stride {stride :2}) in chunks of {chunksize :6} frames. Now at chunk nr {chunk_idx :4}, frames so far {running_f :6}"
    elif ixtc.endswith(".pdb") or ixtc.endswith(".pdb.gz") or ixtc.endswith(".gro"):
        if nchars_fname is None:
            nchars_fname = len(ixtc)
        iterate =  lambda ixtc: [_md.load(ixtc)[::stride]]
        inform  =  lambda ixtc, traj_idx, chunk_idx, running_f: \
            f"Loaded {ixtc :{nchars_fname}} (nr. {traj_idx :4}) in full, using stride {stride :2} but ignoring chunksize of {chunksize :6} frames. Total frames loaded {running_f :6}."
    else:
        if nchars_fname is None:
            nchars_fname = len(ixtc)
        iterate = lambda ixtc: _md.iterload(ixtc, top=top, stride=stride, chunk=int(_np.round(chunksize / stride)))
        inform = lambda ixtc, traj_idx, chunk_idx, running_f: \
            f"Streaming {ixtc :{nchars_fname}} (nr. {traj_idx :4}) with stride {stride :2} in chunks of {chunksize :6} frames. Now at chunk nr {chunk_idx :4}, frames so far {running_f :6}."
    return iterate, inform

def choose_options_descencing(options,
                              fmt="%s",
                              dont_accept=["none", "na"]):
    r"""
    Return the first entry that's acceptable according to some rule

    If no is found, "" is returned
    Parameters
    ----------
    options : list
    fmt : str, default is "%s"
        You can specify a different
        format here. Will only
        apply in case something
        is returned
    dont_accept : list
        Move down the list if
        current item is one
        of these

    Returns
    -------
    best : str
        Either the best entry in :obj:`options`
        or "" if no option was found
    """
    for option in options:
        if str(option).lower() not in dont_accept:
            return fmt%str(option)
    return ""


def fnmatch_ex(patterns_as_csv, list_of_keys):
    r"""
    Match the keys in :obj:`list_of_keys` against some naming patterns
    using Unix filename pattern matching
    TODO include link:  https://docs.python.org/3/library/fnmatch.html

    This method also allows for exclusions (grep -e)

    TODO: find out if regular expression re.findall() is better

    Uses fnmatch under the hood

    Parameters
    ----------
    patterns_as_csv : str
        Patterns to include or exclude, separated by commas, e.g.
        * "H*,-H8" will include all TMs but not H8
        * "G.S*" will include all beta-sheets
    list_of_keys : list
        Keys against which to match the patterns, e.g.
        * ["H1","ICL1", "H2"..."ICL3","H6", "H7", "H8"]

    Returns
    -------
    matching_keys : list

    """
    include_patterns = [pattern for pattern in patterns_as_csv.split(",") if not pattern.startswith("-")]
    exclude_patterns = [pattern[1:] for pattern in patterns_as_csv.split(",") if pattern.startswith("-")]
    #print(include_patterns)
    #print(exclude_patterns)
    # Define the match using a lambda
    matches_include = lambda key : any([_fnmatch(str(key), patt) for patt in include_patterns])
    matches_exclude = lambda key : any([_fnmatch(str(key), patt) for patt in exclude_patterns])
    passes_filter = lambda key : matches_include(key) and not matches_exclude(key)
    outgroup = []
    for key in list_of_keys:
        #print(key, matches_include(key),matches_exclude(key),include_patterns, exclude_patterns)
        if passes_filter(key):
            outgroup.append(key)
    return outgroup

def match_dict_by_patterns(patterns_as_csv, index_dict, verbose=False):
    r"""
    Joins all the values in an input dictionary if their key matches
    some patterns. This method also allows for exclusions (grep -e)

    TODO: find out if regular expression re.findall() is better

    Parameters
    ----------
    patterns_as_csv : str
        Comma-separated patterns to include or exclude, separated by commas, e.g.
        * "H*,-H8" will include all TMs but not H8
        * "G.S*" will include all beta-sheets
    index_dict : dictionary
        It is expected to contain iterable of ints or floats or anything that
        is "joinable" via np.hstack. Typically, something like:
        * {"H1":[0,1,...30], "ICL1":[31,32,...40],...}

    Returns
    -------
    matching_keys, matching_values : list, array of joined values

    """
    matching_keys =   fnmatch_ex(patterns_as_csv, index_dict.keys())
    if verbose:
        print(', '.join(matching_keys))

    if len(matching_keys)==0:
        matching_values = []
    else:
        matching_values = _np.hstack([index_dict[key] for key in matching_keys])

    return matching_keys, matching_values

def defrag_key(key, defrag="@", sep="-"):
    r"""Remove fragment information from a contact label

    Parameters
    ----------
    key : str
        Contact label with some sort of pair information
        e.g. e.g. R1@frag1-E2@frag2->R1-E2
    defrag: char, default is "@"
        Character that indicates the beginning of the
        fragment
    sep : char, default is "-"
        Character that indicates the separation
        between first and second residue of the pair

    Returns
    -------

    """
    return sep.join([kk.split(defrag,1)[0].strip(" ") for kk in splitlabel(key,sep)])

def df_str_formatters(df):
    r"""
    Return formatters for :obj:`~pandas.DataFrame.to_string'

    In principle, this should be solved by
    https://github.com/pandas-dev/pandas/issues/13032,
    but I cannot get it to work

    Parameters
    ----------
    df : :obj:`~pandas.DataFrame`

    Returns
    -------
    formatters : dict
        Keyed with :obj:`df`-keys
        and valued with lambdas
        s.t. formatters[key][istr]=formatted_istr

    """
    formatters = {}
    for key in df.keys():
        fmt = "%%-%us"%max([len(ii)+1 for ii in df[key]])
        formatters[key]=lambda istr : fmt%istr
    return formatters

class FilenameGenerator(object):
    r"""
    Generate per project filenames when you need them

    This is a WIP to consolidate all filenaming in one place,
    s.t. all sanitizing and project-specific naming operations happen
    here and not in the cli methods

    A named tuple would've been enough, but we need some
     methods for dynamic naming (e.g. per-residue or per-traj)

    """

    def __init__(self, output_desc, ctc_cutoff_Ang, output_dir, graphic_ext, table_ext, graphic_dpi, t_unit):

        self._graphic_ext = graphic_ext.strip(".")
        self._output_desc = output_desc.strip(".")
        self._ctc_cutoff_Ang = ctc_cutoff_Ang
        self._output_dir = output_dir
        self._graphic_dpi = graphic_dpi
        self._t_unit = t_unit
        self._allowed_table_exts = ["dat", "txt", "xlsx", "ods"] #TODO what about npy?
        assert str(table_ext).lower != "none"
        self._table_ext = str(table_ext).lower().strip(".")
        if self._table_ext not in self._allowed_table_exts:
            raise ValueError("The table extension, cant be '%s', "
                             "has be one of %s"%(table_ext,self._allowed_table_exts))


    @property
    def output_dir(self):
        return self._output_dir
    @property
    def basename_wo_ext(self):
        return "%s.overall@%2.1f_Ang" % (self.output_desc,
                                         self.ctc_cutoff_Ang)
    @property
    def ctc_cutoff_Ang(self):
        return self._ctc_cutoff_Ang

    @property
    def output_desc(self):
        return self._output_desc.replace(" ","_")

    @property
    def fullpath_overall_no_ext(self):
        return _path.join(self.output_dir, self.basename_wo_ext)

    @property
    def graphic_ext(self):
        return self._graphic_ext

    @property
    def graphic_dpi(self):
        return self._graphic_dpi
    @property
    def table_ext(self):
        return self._table_ext

    @property
    def t_unit(self):
        return self._t_unit
    @property
    def fullpath_overall_fig(self):
        return ".".join([self.fullpath_overall_no_ext, self.graphic_ext])

    def fname_per_residue_table(self,istr):
        assert self.table_ext is not None
        fname = '%s.%s@%2.1f_Ang.%s' % (self.output_desc,
                                        istr.replace('*', "").replace(" ","_"),
                                        self.ctc_cutoff_Ang,
                                        self.table_ext)
        return _path.join(self.output_dir, fname)

    def fname_per_site_table(self, istr):
        return self.fname_per_residue_table(istr)


    def fname_timetrace_fig(self, surname):
        return '%s.%s.time_trace@%2.1f_Ang.%s' % (self.output_desc,
                                                  surname.replace(" ", "_"),
                                                  self.ctc_cutoff_Ang,
                                                  self.graphic_ext)
    @property
    def fullpath_overall_excel(self):
        return ".".join([self.fullpath_overall_no_ext, "xlsx"])

    @property
    def fullpath_overall_dat(self):
        return ".".join([self.fullpath_overall_no_ext, "dat"])

    @property
    def fullpath_pdb(self):
        return ".".join([self.fullpath_overall_no_ext, "as_bfactors.pdb"])

    @property
    def fullpath_matrix(self):
        return self.fullpath_overall_fig.replace("overall@", "matrix@")

    @property
    def fullpath_flare_vec(self):
        if self.graphic_ext == "svg":
            gx = self.graphic_ext
        else:
            gx = "pdf"
        return '.'.join([self.fullpath_overall_no_ext.replace("overall@", "flare@"),gx])