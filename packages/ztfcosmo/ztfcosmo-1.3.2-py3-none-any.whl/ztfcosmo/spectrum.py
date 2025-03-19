import pandas
import warnings
import numpy as np

from . import io
_SPEC_DATAFILE = io.get_spec_datafile(store=True) # store if rebuilding.

def read_spectrum(file_, sep=None):
    """ """
    if 'https://' in file_:
        from urllib import request
        data = [l.decode("utf-8").replace("\n", "") for l in request.urlopen(file_)]
    else:
        data = open(file_).read().splitlines()
        
    try:
        header = pandas.DataFrame([d.replace("#","").replace(":"," ").replace("=","").split()[:2] for d in data 
                                   if (d.startswith("#") or "=" in d or ":" in d) and len(d.split())>=2],
                              columns=["keys", "values"]).set_index("keys")["values"]
    except:
        raise IOError(f"header build Fails for {file_}")
    
    try:
        lbda, flux, *variance = np.asarray([d.split(sep) for d in data 
                                        if not (d.startswith("#") 
                                                or d.startswith("COMMENT") or d.startswith("HISTORY")
                                                or "=" in d or ":" in d) and len(d.split())>=2]).T
        data = pandas.DataFrame({"lbda":lbda, "flux":flux}, dtype="float")
    except:
        raise IOError(f"dataframe build Fails for {file_}")
    
    if len(variance)>0:
        variance_ = np.asarray(variance[0], dtype="float")
        if not np.all(variance_ == 0):
            # Test Variance or Error | unit of log closest to 0
            flag_testrange = [7000,8000]
            flag_in = data["lbda"].between(*flag_testrange)
            data_test = data[flag_in]
            flux_std = data_test["flux"].std()
            # 
            as_var = np.sqrt(variance_[flag_in].mean()) / flux_std
            as_err = variance_[flag_in].mean() / flux_std
            if np.abs(as_err-1) < np.abs(as_var-1):
                data["variance"] = variance_**2
                data["variance_orig"] = variance[0]
            else:
                data["variance"] = variance_

            if "_Keck_" in file_:
                data["variance"] /=10
                
    return header, data


class Spectrum( object ):
    """ """
    def __init__(self, data, header=None, meta=None, 
                     snidresult=None):
        """ """
        self._data = data
        self._header = header
        self._meta = meta
        self.set_snidresult(snidresult)
        
    @classmethod
    def from_filename(cls, filename, snidresult=None):
        """ 
        load_snidres: fetch for snidresults and loads it if it exists.
        """
        from .io import _parse_spec_filename_
        header, data = read_spectrum(filename)    
        meta = _parse_spec_filename_(filename)
        
        this = cls(data, header=header, meta=meta,
                   snidresult=snidresult)
        
        this._filename = filename
        return this
    
    @classmethod
    def from_name(cls, name, **kwargs):
        """ """
        from .io import _get_target_specfullpath_
        fullpath = _get_target_specfullpath_(name)
        
        if len(fullpath)==0:
            warnings.warn(f"No spectra target for {name}")
            return None
        
        if len(fullpath) == 1:
            return cls.from_filename(fullpath[0], **kwargs)
        else:
            return [cls.from_filename(file_, **kwargs) for file_ in fullpath]
                    
    # ================ #
    #    Method        #
    # ================ #
    def fetch_snidresult(self, warn_if_notexist=True):
        """ """
        import os
        
        if self.filename is None:
            raise AttributeError("Unknown filename: cannot fetch the corresponding snidresult")

        snidresult_file = self.filename.replace(".ascii","_snid.h5")
        if not os.path.isfile(snidresult_file):
            if warn_if_notexist:
                warnings.warn(f"snidres file does not exists {snidresult_file}")
            return None
        
        from pysnid.snid import SNIDReader
        return SNIDReader.from_filename(snidresult_file)
    
    def load_snidresult(self, phase=None, redshift=None,
                            force_fit=False, allow_fit=True, **kwargs):
        """ get and set """
        snidresult = self.fetch_snidresult()
        self.set_snidresult( snidresult )
        
    def set_snidresult(self, snidresult):
        """ """
        self._snidresult = snidresult
        
        
    # --------- #
    #  GETTER   #
    # --------- #
    def get_obsdate(self):
        """ calls self.obsdate """
        return self.obsdate
    
    # --------- #
    # PLOTTER   #
    # --------- #        
    def show(self, ax=None, savefile=None, figsize=[7,3],
                 color=None, ecolor=None, ealpha=0.2, 
             show_error=True, zeroline=True, zcolor="0.7", zls="--", 
             zprop={}, fillprop={}, normed=False, offset=None,
             label=None, legend=None, **kwargs):
        """ 
        label: [string or None]
            label for the spectra. 
            use: label='_meta_' to see meta content.
            
        """

        if ax is None:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = ax.figure
        
        prop = dict(zorder=3)
        coef = 1 if not normed else self.flux.mean()
        if offset is None:
            offset = 0

        if label == "_meta_":
            label = f"{self.meta['name']} | by {self.meta.instrument} on {self.meta.date.split('T')[0]}"
        elif label == "_meta_noname_":
            label = f"{self.meta.instrument} on {self.meta.date.split('T')[0]}"
            
        if label is not None and legend is None:
            legend=True
            
        _ = ax.plot(self.lbda, self.flux/coef + offset, label=label, color=color, **{**prop, **kwargs})
        if self.has_error() and show_error:
            if ecolor is None:
                ecolor = color
            ax.fill_between(self.lbda, (self.flux-self.error)/coef+ offset, (self.flux+self.error)/coef+ offset, 
                           facecolor=ecolor, alpha=ealpha, **{**prop,**fillprop})
            
        if zeroline:
            ax.axhline(0, color=zcolor,ls=zls, **{**dict(lw=1, zorder=1),**zprop} )
            
        ax.set_ylabel("flux []"+ (" -normed-" if normed else ""))
        ax.set_xlabel(r"Wavelength [$\AA$]")
        if legend:
            ax.legend(loc="best", frameon=False, fontsize="small")

        if savefile:
            fig.savefig(savefile, dpi=150)
            
        return fig

    def show_snidresult(self, axes=None, savefile=None, label=None, **kwargs):
        """ shortcut to self.snidresult.show() """
        if self.snidresult is None:
            warnings.warn("snidres is not defined (None)")
            return self.show(ax=axes[0] if axes is not None else None)
        
        return self.snidresult.show(axes=axes, savefile=savefile, label=label, **kwargs)
    
    # ------------ #
    #   Internal   #
    # ------------ #
    # ================ #
    #   Properties     #
    # ================ #
    # Baseline    
    @property
    def data(self):
        """ """
        return self._data
    
    @property
    def header(self):
        """ """
        return self._header
    
    @property
    def meta(self):
        """ """
        return self._meta

    @property
    def name(self):
        """ name of the target (from self.meta). 
        None if no meta or name not in meta"""
        if self.meta is None:
            return None
        
        return self.meta.get("ztfname")

    @property
    def obsdate(self):
        """ """
        if self.meta is None:
            return None
        
        if "date" not in self.meta.index or self.meta["date"] is None:
            warnings.warn("Unknown date for the given spectrum")
            return None

        from astropy.time import Time
        from datetime import datetime
        return Time(datetime.strptime(self.meta["date"], '%Y%m%d'))


    @property
    def snidresult(self):
        """ """
        return self._snidresult
    
    # Derived
    @property
    def lbda(self):
        """ """
        return np.asarray(self.data["lbda"].values, dtype="float")

    @property
    def average_lstep(self):
        """ """
        return np.mean( np.unique(np.round( np.diff(self.lbda), 2) ) )
    
    @property
    def flux(self):
        """ """
        return np.asarray(self.data["flux"].values, dtype="float")
    
    def has_error(self):
        """ """
        return self.has_variance()
    
    def has_variance(self):
        """ """
        return "variance" in self.data
    
    @property
    def variance(self):
        """ """
        if not self.has_error():
            return None
        
        return np.asarray(self.data["variance"].values, dtype="float")
        
    @property
    def error(self):
        """ """
        if not self.has_error():
            return None
        
        return np.sqrt(self.variance)

    @property
    def filename(self):
        """ """
        if not hasattr(self,"_filename"):
            return None
        return self._filename
