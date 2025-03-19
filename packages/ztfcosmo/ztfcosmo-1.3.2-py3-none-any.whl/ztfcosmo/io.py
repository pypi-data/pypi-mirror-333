

import warnings
import os
import numpy as np
import pandas

SOURCE_URL = "https://ztfcosmo.in2p3.fr/download"


__all__ = ["get_data", "get_target_lightcurve", "get_target_spectra",
           "get_spec_datafile", "get_observing_logs", "is_local",
           "get_ztfcosmodir"]


def get_ztfcosmodir(directory=None, force_online=True):
    """ simple function to access the directory where the data is """
    if force_online:
        directory = SOURCE_URL
        
    elif directory is None:
        directory = os.getenv("ZTFCOSMODIR", SOURCE_URL)

    return directory

def _ztfdr2name_to_fullpath_(ztfdr2name, force_online=True, directory=None):
    """ """
    dirname = get_ztfcosmodir(directory=directory, force_online=force_online)
    if dirname == SOURCE_URL:
        ztfdr2name = ztfdr2name.replace("/", "__")

    return os.path.join(dirname, ztfdr2name)
    
def is_local():
    """ Test if you are using local files or remote data access """
    fullpath = _ztfdr2name_to_fullpath_("None")
    return not (SOURCE_URL in fullpath)

# ============= #
#   Tables      #
# ============= #
def get_data(good_coverage=None, good_lcfit=None, redshift_range=None,
             saltmodel="salt2-T21", band="gri", phase_range=[-10,40]):
    """ get snia, global and local host information.

    Parameters
    ----------
    good_coverage: bool, None
        should you limit to well sampled lightcurves (True) or badly sampled ones (False).
        None means no cut.

    good_lcfit: bool, None
        should you limit to lightcurves passing the lightcurve parameters cuts (True) 
        or these that do not (False).
        None means no cut.

    redshift_range: (float, float)
        limit data to these between given redshift range. 
        e.g. [0., 0.06] for volume limited sample.

    saltmodel: str
        which salt model to be used ("salt2-T21" is default).
        - salt2-2.4 (JLA, Betoule et al. )
        - salt2-T23 (Taylor et al. 2023)
        - salt3 (Kenworthy et al. 2021)
        
    band: str
        which band used to fit the lightcurves.
        - "gri" [default]
        - "gr" (only available for saltmodel in ['salt2-T21', 'salt3']
        
    phase_range: (int, int)
        rest-frame phase range used to fit the lightcurves.
        start: [-10, -15, -20] and for end of 40, start of [0, 5, 10]
        end: [30, 40, 45, 50]
        
    Returns
    -------
    pandas.DataFrame
    """
    sndata = get_sn_data()
    globalhost = get_globalhost_data()
    localhost = get_localhost_data()

    # merging naming convention
    param_keys = ["mass", "mass_err", "restframe_gz", "restframe_gz_err"]
    globalhost = globalhost.rename({f"{k}":f"global{k}" for k in param_keys}, axis=1)
    localhost = localhost.rename({f"{k}":f"local{k}" for k in param_keys}, axis=1)

    # out dataframe
    joined_df = sndata.join( globalhost.join(localhost) )

    #
    # some additional Selections
    # 
    if good_coverage is not None:
        if good_coverage:
            joined_df = joined_df[joined_df["lccoverage_flag"].astype(bool)]
        else:
            joined_df = joined_df[~joined_df["lccoverage_flag"].astype(bool)]


    if good_lcfit is not None:
        if good_lcfit:
            joined_df = joined_df[joined_df["fitquality_flag"].astype(bool)]
        else: # lcquality_flag
            joined_df = joined_df[~joined_df["fitquality_flag"].astype(bool)]

    if redshift_range is not None:
        joined_df = joined_df[joined_df["redshift"].between(*redshift_range)]

    return joined_df

def get_sn_data(saltmodel="salt2-T21", band="gri", phase_range=[-10,40]):
    """ grab SN Ia lightcurve data

    Parameters
    ----------
    redshift_range: (float, float)
        limit data to these between given redshift range. 
        e.g. [0., 0.06] for volume limited sample.

    saltmodel: str
        which salt model to be used ("salt2-T21" is default).
        - salt2-2.4 (JLA, Betoule et al. )
        - salt2-T23 (Taylor et al. 2023)
        - salt3 (Kenworthy et al. 2021)
        
    band: str
        which band used to fit the lightcurves.
        - "gri" [default]
        - "gr" (only available for saltmodel in ['salt2-T21', 'salt3']
        
    phase_range: (int, int)
        rest-frame phase range used to fit the lightcurves.
        start: [-10, -15, -20] and for end of 40, start of [0, 5, 10]
        end: [30, 40, 45, 50]

    Returns
    -------
    pandas.DataFrame
    """
    # default
    if saltmodel=="salt2-T21" and band=="gri" and phase_range==[-10,40]:
        ztfdr2name = os.path.join("tables", "snia_data.csv")
    else:
        phase = f"phase{phase_range[0]:d}to{phase_range[1]:d}"
        naming_convention = f"snia_data_{phase}_{band}_{saltmodel}.csv"
        ztfdr2name = os.path.join("tables", "extra", naming_convention)

    fullpath = _ztfdr2name_to_fullpath_(ztfdr2name)
    return pandas.read_csv(fullpath, index_col=0).set_index("ztfname")

def get_globalhost_data():
    """ get global host dataframe """
    ztfdr2name = os.path.join("tables", "globalhost_data.csv")
    fullpath = _ztfdr2name_to_fullpath_(ztfdr2name)
    return pandas.read_csv(fullpath, index_col=0)

def get_localhost_data():
    """ get local (2kpc) host dataframe """
    ztfdr2name = os.path.join("tables", "localhost_data.csv")
    fullpath = _ztfdr2name_to_fullpath_(ztfdr2name)
    return pandas.read_csv(fullpath, index_col=0)


# ============= #
#   Spectra     #
# ============= #
def _get_target_specfullpath_(name):
    """ """
    from . import spectrum    
    # trick of having _SPEC_DATAFILE in spectrum to open load it then.
    basenames = spectrum._SPEC_DATAFILE[spectrum._SPEC_DATAFILE["ztfname"]==name
                                      ]["basename"].values
    ztfdr2names = [os.path.join("spectra", basename) for basename in basenames]
    fullpath = [_ztfdr2name_to_fullpath_(ztfdr2name) for ztfdr2name in ztfdr2names]
    return fullpath
    
    
def get_target_spectra(name, as_data=True):
    """ get spectra (could be multiple) associated to given target

    Parameters
    ----------
    as_data: bool
        should this return the data (True) or a dedicated object (False)

    Returns
    -------
    data or object (see as_data)
    """
    from . import spectrum
    fullpath = _get_target_specfullpath_(name)
    # single spectrum case
    if len(fullpath)==1:
        file_ = fullpath[0]
        if as_data:
            return spectrum.read_spectrum(file_)
        
        return spectrum.Spectrum.from_filename(file_)
    else: # multiple spectra case
        if as_data:
            return [spectrum.read_spectrum(file_) for file_ in fullpath]
        return [spectrum.Spectrum.from_filename(file_) for file_ in fullpath]
    
def _parse_spec_filename_(filename):
    """ file or list of files.
    
    Returns
    -------
    - Serie if single file
    - DataFrame otherwise
    """
    index = ["ztfname", "date", "telescope", "version"]
    fdata = []
    for file_ in np.atleast_1d(filename):
        file_ = os.path.basename(file_).split(".ascii")[0]
        name, date, *telescope, origin = file_.split("_")    
        telescope = "_".join(telescope)
        fdata.append([name, date, telescope, origin])

    if len(fdata) == 1:
        return pandas.Series(fdata[0], index=index)
    
    return pandas.DataFrame(fdata, columns=index)

def get_spec_datafile(rebuild=False, store=False):
    """ get a dataframe summarizing spectral information data (from filenames) """
    ztfdr2name = os.path.join("tables", f"spec_dataframe.parquet")
    fullpath = _ztfdr2name_to_fullpath_(ztfdr2name)    
    if not is_local():
        if rebuild:
            warnings.warn("Cannot rebuild if not using local files.")
        
        return pandas.read_parquet(fullpath)
    
    # uses local files.
    if not os.path.isfile(fullpath):
        rebuild = True

    if not rebuild:
        return pandas.read_parquet(fullpath)
        
    # rebuild
    from glob import glob
    from astropy.time import Time
    
    ztfcosmodir = get_ztfcosmodir()
    specfiles = glob( os.path.join(ztfcosmodir, "spectra", "*.ascii"))
    datafile = pandas.DataFrame(specfiles, columns=["fullpath"])
    datafile["basename"] = datafile["fullpath"].str.split(pat="/", expand=True).iloc[:, -1]
    
    _ =  datafile.pop("fullpath") # don't store
    specfile = pandas.concat([datafile, _parse_spec_filename_(datafile["basename"])], axis=1)
    
    data = get_sn_data()
    specfile["dateiso"] = Time(np.asarray(specfile["date"].apply(lambda x: f"{x[:4]}-{x[4:6]}-{x[6:]}"), dtype=str), format="iso").mjd
    specfile = specfile.join(data[["t0", "redshift"]], on="ztfname")
    specfile["phase_obs"] = (specfile.pop("dateiso")-specfile.pop("t0"))
    specfile["phase"] = specfile["phase_obs"]/(1+specfile.pop("redshift"))

    if store:
        fullpath = _ztfdr2name_to_fullpath_(ztfdr2name)
        specfile.to_parquet(fullpath)
    
    return specfile

# ============= #
#  LightCurves  #
# ============= #
def get_target_lightcurve(name, as_data=True,
                          saltmodel="salt2-T21",
                          band="gri",
                          phase_range=[-10,40]):
    """ get the lightcurve data associated to the given target.

    Parameters
    ----------
    as_data: bool
        should this return the lightcurve as dataframe or a dedicated object.
        
    saltmodel: str
        = ignored if as_data=True = 
        which salt model to be used to model the lightcurves ("salt2-T21" is default).
        - salt2-2.4 (JLA, Betoule et al. )
        - salt2-T23 (Taylor et al. 2023)
        - salt3 (Kenworthy et al. 2021)
        
    band: str
        = ignored if as_data=True = 
        which band used to fit the lightcurves.
        - "gri" [default]
        - "gr" (only available for saltmodel in ['salt2-T21', 'salt3']
        
    phase_range: (int, int)
        = ignored if as_data=True = 
        rest-frame phase range used to fit the lightcurves.
        start: [-10, -15, -20] and for end of 40, start of [0, 5, 10]
        end: [30, 40, 45, 50]        
    
    Returns
    -------
    pandas.DataFrame or LightCurve
    """
    ztfdr2name = os.path.join("lightcurves", f"{name}_lc.csv")
    fullpath = _ztfdr2name_to_fullpath_(ztfdr2name)
    
    if as_data:
        return pandas.read_csv(fullpath,  sep='\s+', comment='#')

    from .lightcurve import LightCurve
    saltparam = get_sn_data(saltmodel=saltmodel, band=band,
                            phase_range=phase_range).loc[name]
    return LightCurve.from_name(name,
                                saltmodel=saltmodel,
                                saltparam=saltparam,
                                phase_range=phase_range)

# ================ #
#  Observing logs  #
# ================ #
def get_observing_logs():
    """ get observing logs dataframe (slow if remote access) """
    if not is_local():
        warnings.warn("you are not using local file. Loading the observing logs remotely is slow.")
        
    ztfdr2name = os.path.join("tables", "observing_logs.parquet")
    fullpath = _ztfdr2name_to_fullpath_(ztfdr2name)        
    return pandas.read_parquet(fullpath)
