import numpy as np
import pandas
import warnings


from . import io


ZTFCOLOR = { # ZTF
        "ztfr":dict(marker="o", ms=7, mfc="C3"),
        "ztfg":dict(marker="o", ms=7, mfc="C2"),
        "ztfi":dict(marker="o", ms=7, mfc="C1")
}

BAD_ZTFCOLOR = { # ZTF
        "ztfr":dict(marker="o", ms=6, mfc="None", mec="C3"),
        "ztfg":dict(marker="o", ms=6, mfc="None", mec="C2"),
        "ztfi":dict(marker="o", ms=6, mfc="None", mec="C1")
}

    
def get_saltmodel(which="salt2.4", **params):
    """ """
    import sncosmo
    if which is None:
        which  ="salt2 v=T21" # default in ztfdr2

    which = which.replace("-", " v=")
    if which in ["salt2.4"]:
        which = "salt2 v=2.4"
    
    # parsing model version
    source_name, *version = which.split("v=")
    source_name = source_name.strip()
    version = None if len(version)==0 else version[0].strip()
    source = sncosmo.get_source(source_name, version=version, copy=True)
    
    dust  = sncosmo.CCM89Dust()
    model = sncosmo.Model(source, effects=[dust],
                              effect_names=['mw'],
                              effect_frames=['obs'])
    model.set(**params)
    return model

class LightCurve( object ):

    def __init__(self, data, saltparam=None, saltmodel=None, phase_range=None):
        """ likely, this is not how you should load the data. 
        See from_name() or from_filename() class methods.
        """
        self.set_data(data)
        self.set_saltparam(saltparam)
        self._saltmodel = saltmodel
        self._fitphases = phase_range
        
    @classmethod
    def from_name(cls, name, saltparam=None, saltmodel=None, phase_range=None):
        """ """
        lcdata = io.get_target_lightcurve(name, as_data=True)
        if saltparam is None:
            saltparam = io.get_data().loc[name]
            
        this = cls(data=lcdata,
                       saltparam=saltparam,
                       saltmodel=saltmodel,
                       phase_range=phase_range)
        this._name = name
        return this
    
    # ================ #
    #    Method        #
    # ================ #
    # --------- #
    #  SETTER   #
    # --------- #
    def set_data(self, data):
        """ """
        self._data = data

    def set_saltparam(self, saltparam):
        """ """
        self._saltparam = saltparam
        
    # --------- #
    #  GETTER   #
    # --------- #
    def get_obsphase(self, min_detection=5, groupby=None, **kwargs):
        """ 
        Returns
        -------
        pandas.Series 
        """
        lcdata = self.get_lcdata(min_detection=min_detection, **kwargs)
        if groupby is None:
            return lcdata["phase"]
        
        return lcdata.groupby(groupby)["phase"].apply( list )
        
    def get_saltmodel(self, which=None):
        """ """
        if which is None:
            which = self._saltmodel
            
        propmodel = self.saltparam.rename({"redshift":"z"})[["z","t0","x0","x1","c","mwebv"]
                                                           ].to_dict()
        return get_saltmodel(which=which, **propmodel)
    
    def get_lcdata(self, zp=None, in_mjdrange=None,
                       min_detection=None,
                       filters=None,
                       flagout=[1,2,4,8,16]):
        """ 
        filters: [string, None or list]
            list of filters 
            - None/'*' or 'all': no filter selection/
            - string: just this filter (e.g. 'ztfg')
            - list of string: just these filters (e.g. ['ztfg','ztfr'])

        flagout: [list of int or string]
            flag == 0 means all good, but in details:
            
            0: no warning 
            1: flux_err==0 Remove unphysical errors 
            2: chi2dof>3: Remove extreme outliers 
            4: cloudy>1: BTS cut 
            8: infobits>0: BTS cut 16: mag_lim<19.3: Cut applied in Dhawan 2021 
            32: seeing>3: Cut applied in Dhawan 2021 
            64: fieldid>879: Recommended IPAC cut 
            128: moonilf>0.5: Recommended IPAC cut 
            256: has_baseline>1: Has a valid baseline correction 
            512: airmass>2: Recommended IPAC cut 
            1024: flux/flux_err>=5: Nominal detection

        """
        from .utils import flux_to_mag

        # data should be copy()
        if flagout in ["all","any","*"]:
            data = self.data[self.data["flag"]==0].copy()
            
        elif flagout is None:
            data = self.data.copy()
        else:
            flag_ = np.all([(self.data.flag&i_==0) for i_ in np.atleast_1d(flagout)], axis=0)
            data = self.data[flag_].copy()

        # change the zeropoint
        if zp is None:
            zp = data["ZP"].values
            coef = 1. 
        else:
            coef = 10 ** (-(data["ZP"].values - zp) / 2.5)
            zp = np.ones(len(data)) * zp # broadcasting
        #
        # Data to be used
        #
        flux  = data["flux"] * coef
        error = data["flux_err"] * coef
        detection = flux/error
            
        
        lcdata = data[["mjd","mag","mag_err","filter","field_id", "flag", "rcid"]] 
        additional = pandas.DataFrame(np.asarray([zp, flux, error, detection]).T,
                                         columns=["zp", "flux", "error", "detection"],
                                         index=lcdata.index)
        
        additional["mag_lim"], _ = flux_to_mag(error*5, None, zp=zp)
        
        lcdata = pandas.merge(lcdata, additional, left_index=True, right_index=True)
        lcdata["filter"] = lcdata["filter"].replace("ztf","ztf")
        
        
        if self.saltparam is not None:
            lcdata["phase"] = lcdata["mjd"]-self.saltparam['t0']
        else:
            lcdata["phase"] = np.NaN
            
        if in_mjdrange is not None:
            lcdata = lcdata[lcdata["mjd"].between(*in_mjdrange)]

        if min_detection is not None:
            lcdata = lcdata[lcdata["detection"]>min_detection]

        if filters is not None and filters not in ["*","all"]:
            lcdata = lcdata[lcdata["filter"].isin(np.atleast_1d(filters))]
            
        return lcdata

    def get_model_residual(self, model=None, which=None,
                           intrinsic_error=None, 
                           **kwargs):
        """ get a dataframe with lightcurve data, model and residuals information.

        Parameters
        ----------
        model: [sncosmo.Model or None] -optional-
            provide the sncosmo model from which the model flux can be obtained.
            If None given [default] this method will call self.get_saltmodel().

        modelprop: [dict] -optional-
            kwarg information passed to model.set() to change the default model parameters.
            = This is only used in model=None = 
            It aims at updating model given by self.get_saltmodel()
            
        intrinsic_error: [float] -optional-
            provide an intrinsic error for the lightcurve. This will be stored as 'error_int'
            in the returned DataFrame. 
            The 'pull' will use the quadratic sum of error and error_int to be calculated.
            if None given [default] this will assume 0.

        
        **kwargs goes to get_lcdata()

        Returns
        -------
        DataFrame
        """
        basedata = self.get_lcdata(**kwargs)[["mjd","flux", "error","phase",
                                              "filter","flag", "field_id", "rcid"]
                                            ].copy()
        if model is None:
            model = self.get_saltmodel(which)

        # Model
        basedata["model"] = model.bandflux(basedata["filter"], basedata["mjd"], 
                                            zp=self.flux_zp, zpsys="ab")
        # Residual    
        basedata["residual"] = basedata["flux"] - basedata["model"]

        # Error    
        basedata["error_int"] = intrinsic_error if intrinsic_error is not None else 0
        total_error = np.sqrt(basedata["error"]**2 + basedata["error_int"]**2)
        
        # Pull    
        basedata["pull"] = basedata["residual"]/total_error

        return basedata
    
    def get_sncosmotable(self, min_detection=5,  phase_range=[-10, 40],
                             filters=["ztfr","ztfg"], **kwargs):
        """ """
        from .utils import mag_to_flux
        
        t0 = self.saltparam["t0"]
        to_fit = self.get_lcdata(min_detection=min_detection,
                                 in_mjdrange= t0 + phase_range,
                                 filters=filters, **kwargs)
        sncosmo_lc = to_fit.rename({"mjd":"time", "filter":"band"},axis=1
                                  )[["time","band","zp","mag","mag_err"]]
        sncosmo_lc["zpsys"] = "ab"
        sncosmo_lc["flux"], sncosmo_lc["flux_err"] = mag_to_flux(sncosmo_lc["mag"],
                                                                 sncosmo_lc["mag_err"],
                                                                 zp=sncosmo_lc["zp"])
        return sncosmo_lc
        
    # --------- #
    #  PLOTTER  #
    # --------- #
    def show(self, ax=None, figsize=[7,2], zp=None, bands="*",
                 formattime=True, zeroline=True,
                 incl_salt=True, which_model=None, autoscale_salt=True,
                 clear_yticks=True,
                 phase_range=[-30,100], as_phase=False, 
                 inmag=False, ulength=0.1, ualpha=0.1,
                 rm_flags=True, show_fitphase=True, **kwargs):
        """ """
        from matplotlib import dates as mdates
        from astropy.time import Time
        
        # - Axes Definition
        if ax is None:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = ax.figure
            
        # - End axes definition
        # -- 
        # - Data
        base_prop = dict(ls="None", mec="0.9", mew=0.5, ecolor="0.7", zorder=7)
        bad_prop  = dict(ls="None", mew=1, ecolor="0.7", zorder=6)        
        lineprop  = dict(color="0.7", zorder=1, lw=0.5)

        if incl_salt:
            saltmodel = self.get_saltmodel(which=which_model)
            if np.isnan(saltmodel.parameters).any():
                saltmodel = None
                autoscale_salt = False
        else:
             saltmodel = None
             autoscale_salt = False

             
        t0 = self.saltparam.t0
        if not np.isnan(t0):
            if phase_range is not None: # removes NaN
                timerange = [t0+phase_range[0], t0+phase_range[1]]
            else:
                timerange = None
                
            modeltime = t0 + np.linspace(-15,50,100)
        else:
            timerange = None
            if incl_salt:
                warnings.warn("t0 in saltparam is NaN, cannot show the model")
            if as_phase:
                warnings.warn("t0 in saltparam is NaN, as_phase not available")
                as_phase = False
                
            incl_salt = False
            saltmodel = None
            autoscale_salt = False
            
        if not rm_flags:
            prop = {"flagout": None}
        else:
            prop = {}
            
        lightcurves = self.get_lcdata(zp=zp, in_mjdrange=timerange, **prop)
        
        if bands is None or bands in ["*", "all"]:
            bands = np.unique(lightcurves["filter"])
        else:
            bands = np.atleast_1d(bands)
        

        max_saltlc = 0
        min_saltlc = 100
        # Loop over bands
        for band_ in bands:
            if band_ not in ZTFCOLOR:
                warnings.warn(f"WARNING: Unknown instrument: {band_} | magnitude not shown")
                continue

            flagband = (lightcurves["filter"]==band_)
            
            bdata = lightcurves[flagband]
#            flag_good_ = flag_good[flagband]
            
            # IN FLUX
            if not inmag:
                # - Data
                if as_phase:
                    datatime = bdata["mjd"].astype("float") - t0
                else:
                    datatime = Time(bdata["mjd"].astype("float"), format="mjd").datetime
                    
                y, dy = bdata["flux"], bdata["error"]
                # - Salt
                if saltmodel is not None:
                    saltdata = saltmodel.bandflux(band_, modeltime, zp=self.flux_zp, zpsys="ab") \
                      if saltmodel is not None else None
                else:
                    saltdata = None
                    
            # IN MAG                                
            else:
                # - Data
                bdata = bdata[ (bdata["mag"]<99) ]
                if as_phase:
                    datatime = bdata["mjd"].astype("float") - t0
                else:
                    datatime = Time(bdata["mjd"], format="mjd").datetime
                    
                y, dy = bdata["mag"], bdata["mag_err"]
                # - Salt
                if saltmodel is not None:
                    saltdata = saltmodel.bandmag(band_, "ab", modeltime)
                else:
                    saltdata = None
            
            # -> good
            ax.errorbar(datatime,#[flag_good_],
                            y,#[flag_good_],
                            yerr=dy,#[flag_good_], 
                            label=band_, 
                            **{**base_prop, **ZTFCOLOR[band_],**kwargs}
                            )
            # -> bad
            ax.errorbar(datatime,#[~flag_good_],
                            y,#[~flag_good_],
                            yerr=dy,#[~flag_good_], 
                            label=band_, 
                            **{**bad_prop, **BAD_ZTFCOLOR[band_],**kwargs}
                            )
        
            if saltdata is not None:
                if as_phase:
                    time_shown = modeltime - t0
                else:
                    time_shown = Time(modeltime, format="mjd").datetime
                    
                ax.plot(time_shown,
                        saltdata,
                        color=ZTFCOLOR[band_]["mfc"], zorder=5)

                max_saltlc = np.nanmax([max_saltlc, np.max(saltdata)])
                min_saltlc = np.nanmin([min_saltlc, np.min(saltdata)])
            
        if inmag:
            ax.invert_yaxis()
            for band_ in bands:
                bdata = lightcurves[(lightcurves["filter"]==band_) & (lightcurves["mag"]>=99)]
                if as_phase:
                    datatime = Time(bdata["mjd"], format="mjd").datetime
                else:
                    datatime = bdata["mjd"].astype("float") - t0
                    
                y = bdata["mag_lim"]
                ax.errorbar(datatime, y,
                                 yerr=ulength, lolims=True, alpha=ualpha,
                                 color=ZTFCOLOR[band_]["mfc"], 
                                 ls="None",  label="_no_legend_")
                                 
        if formattime and not as_phase:
            locator = mdates.AutoDateLocator()
            formatter = mdates.ConciseDateFormatter(locator)
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)

        if inmag:
            ax.set_ylabel(f"mag")
        else:
            zp = self.flux_zp if zp is None else zp # default ZP
            ax.set_ylabel(f"flux [zp={zp}]")
        if zeroline:
            ax.axhline(0 if not inmag else 22, color="0.7",ls="--",lw=1, zorder=1)

        if not inmag:
            max_data = np.percentile(lightcurves["flux"], 99.)
            mean_error = np.nanmean(lightcurves["error"])
            ax.set_ylim(-2*mean_error, max_data*1.15)
            if clear_yticks:
                ax.axes.yaxis.set_ticklabels([])
            
        if autoscale_salt:
            if timerange is not None:
                if as_phase:
                    ax.set_xlim(*(np.asarray(timerange)-t0))
                else:
                    ax.set_xlim(*Time(timerange,format="mjd").datetime)
                    
            if not inmag:
                ax.set_ylim(bottom=-max_saltlc*0.25,
                            top=max_saltlc*1.25)
            else:
                if np.isinf(min_saltlc) or np.isnan(min_saltlc):
                    ax.set_ylim(23, 14)
                else:
                    ax.set_ylim(bottom=23, top=min_saltlc*0.95)


        if show_fitphase:
            upper_ref = 0 if not inmag else 22
            lower = ax.get_ylim()[0]
            fluxes = [upper_ref, lower]
            t0color = "0.5"
            if not as_phase:
                t0 = self.saltparam["t0"]
                time_ = Time(t0, format="mjd").datetime
            else:
                t0 = 0
                time_ = 0

            ax.plot([time_, time_], fluxes, color=t0color, lw=0.5, zorder=9)

            # phase [-10, +40]
            ## accept both coventions
            redshift = self.saltparam.get("redshift", self.saltparam.get("z"))
            phase_range = self.fit_phaserange
            if phase_range is None:
                phase_range = [-10, +40]
                
            start, stop = phase_range
            time_range = [t0+start/(1.+redshift), t0+stop/(1.+redshift)]
            if not as_phase:
                time_range = Time(np.asarray(time_range), format="mjd").datetime

            ax.fill_between(time_range,
                                y2=upper_ref,
                                y1=[lower,lower], facecolor=t0color,
                            alpha=0.1, edgecolor="None")
                    
        return fig

    
    # ================ #
    #   Properties     #
    # ================ #        
    @property
    def data(self):
        """ """
        return self._data
    
    @property
    def name(self):
        """ """
        if not hasattr(self,"_name"):
            self._name = "unknown_name"
            
        return self._name
    
    @property
    def saltparam(self):
        """ """
        if not hasattr(self,"_saltparam"):
            return None
        
        return self._saltparam

    @property
    def fit_phaserange(self):
        """ """
        if not hasattr(self, "_fitphases"):
            return None
        
        return self._fitphases
        

    @property
    def flux_zp(self):
        """ """
        zp = self.data["ZP"]
        if len(np.unique(zp)) == 1:
            return float(zp[0])
        
        return zp

    
    
