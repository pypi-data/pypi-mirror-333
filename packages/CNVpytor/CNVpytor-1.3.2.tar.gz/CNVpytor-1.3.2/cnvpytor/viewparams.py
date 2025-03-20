""" cnvpytor.viewparams

Class ViewParams: parameters and description for Viewer class
"""
from __future__ import absolute_import, print_function, division

from .genome import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import logging

_logger = logging.getLogger("cnvpytor.viewparams")


class ViewParams(object):
    default = {
        "bin_size": None,
        "panels": ["rd"],
        "rd_raw": True,
        "rd_corrected": True,
        "rd_partition": False,
        "plot_baf": True,
        "plot_maf": True,
        "plot_dbaf": True,
        "rd_call": True,
        "rd_use_mask": False,
        "rd_use_gc_corr": True,
        "callers": ["rd_mean_shift"],
        "flip_correction_caller": None,
        "Q0_range": [-1, 1],
        "pN_range": [-1, 1],
        "dG_range": [-1, np.inf],
        "size_range": [0, np.inf],
        "bins_range": [0, np.inf],
        "p_range": [0, np.inf],
        "annotate": False,
        "rd_range": [0, 6],
        "baf_range": [0, 1.0],
        "rd_manhattan_range": [0, 2],
        "rd_manhattan_log_scale": False,
        "rd_manhattan_call": False,
        "snp_use_mask": True,
        "snp_use_id": False,
        "snp_use_phase": False,
        "snp_call": True,
        "markersize": "auto",
        "font_size": "8",
        "lh_markersize": 20,
        "lh_marker": "_",
        "lh_lite":False,
        "rd_colors": ["grey", "black", "red", "green", "blue", "cyan", "brown"],
        "legend": False,
        "title": True,
        "snp_colors": ["orange", "brown", "green", "blue", "yellow", "red", "orange", "brown"],
        "snp_alpha_P": False,
        "rd_circular_colors": ["#555555", "#aaaaaa"],
        "snp_circular_colors": ["#00ff00", "#0000ff"],
        "baf_colors": ["gray", "black", "red", "green", "blue"],
        "lh_colors": ["yellow", "red"],
        "plot_files": [],
        "plot_file": 0,
        "plot": False,
        "file_titles": [],
        "chrom": [],
        "style": None,
        "grid": "auto",
        "subgrid": "vertical",
        "panel_size": [8, 6],
        "xkcd": False,
        "margins": [0.05, 0.95, 0.1, 0.98, 0.1, 0.2],
        "dpi": 200,
        "output_filename": "",
        "print_filename": "",
        "contrast": 20,
        "min_segment_size": 0,
        "matplotlib_use" : None
    }

    def __init__(self, params):
        """
        Class implements parameters and command tree used in Viewer

        Parameters
        ----------
        params : dict
            Initial parameters

        """
        for key in self.default:
            if key in params:
                setattr(self, key, params[key])
            else:
                setattr(self, key, self.default[key])
        for p in self.params:
            self.command_tree["set"][p] = None
            self.command_tree["unset"][p] = None
        for c in self.param_help:
            self.command_tree["help"][c] = None
        self.command_tree["set"]["panels"] = {}
        for panel1 in ["rd", "likelihood", "snp", "baf", "snv", "CN"]:
            self.command_tree["set"]["panels"][panel1] = self.command_tree["set"]["panels"]
        self.command_tree["set"]["callers"] = {}
        for caller in ["rd_mean_shift", "rd_mosaic", "baf_mosaic", "combined_mosaic"]:
            self.command_tree["set"]["callers"][caller] = self.command_tree["set"]["callers"]
        self.command_tree["set"]["grid"] = {"auto": None, "horizontal": None, "vertical": None}
        self.command_tree["set"]["subgrid"] = {"auto": None, "horizontal": None, "vertical": None}
        self.command_tree["set"]["flip_correction_caller"] = {"baf_mosaic": None, "combined_mosaic": None}
        self.interactive = True

    def set_param(self, param, args):
        """
        Set parameter

        Parameters
        ----------
        param: str
            Parameter name
        args: list of str
            Value/values to be casted and saved

        Returns
        -------
        None

        """
        try:
            if param in self.params and self.params[param] is False:
                self.__setattr__(param, True)
            elif param.find(".") > 0:
                sp = param.split(".")
                if len(sp) == 2 and (sp[0] in self.params) and sp[0][-7:] == "_colors" and sp[1].isdigit():
                    ix = int(sp[1])
                    self.params[sp[0]][ix] = args[0]
                if len(sp) == 2 and sp[0] == "margins" and sp[1].isdigit():
                    ix = int(sp[1])
                    self.params[sp[0]][ix] = float(args[0])
            elif param == "margins":
                if len(args) > 0:
                    self.__setattr__(param, list(map(float, args)))
            elif param == "bin_size":
                if len(args) > 0:
                    self.__setattr__(param, args[0])
            elif param == "contrast":
                if len(args) > 0:
                    self.__setattr__(param, float(args[0]))
            elif param == "markersize":
                if len(args) > 0:
                    if args[0] == "auto":
                        self.__setattr__(param, "auto")
                    else:
                        self.__setattr__(param, float(args[0]))
            elif param == "font_size":
                if len(args) > 0:
                    self.__setattr__(param, float(args[0]))
            elif param == "lh_markersize":
                if len(args) > 0:
                    self.__setattr__(param, float(args[0]))
            elif param == "lh_marker":
                if len(args) > 0:
                    self.__setattr__(param, args[0])
            elif param == "grid":
                if len(args) > 0:
                    if args[0] in ["auto", "horizontal", "vertical"]:
                        self.__setattr__(param, args[0])
                    else:
                        self.__setattr__(param, list(map(int, args[:2])))
            elif param == "subgrid":
                if len(args) > 0:
                    if args[0] in ["auto", "horizontal", "vertical"]:
                        self.__setattr__(param, args[0])
                    else:
                        self.__setattr__(param, list(map(int, args[:2])))
            elif param == "panel_size":
                if len(args) > 0:
                    self.__setattr__(param, list(map(float, args[:2])))
            elif param == "dpi":
                if len(args) > 0:
                    self.__setattr__(param, int(args[0]))
            elif param == "Q0_range":
                if len(args) > 1:
                    self.__setattr__(param, list(map(float, args[:2])))
            elif param == "pN_range":
                if len(args) > 1:
                    self.__setattr__(param, list(map(float, args[:2])))
            elif param == "size_range":
                if len(args) > 1:
                    if args[1] == "inf":
                        self.__setattr__(param, [int(args[0]), np.inf])
                    else:
                        self.__setattr__(param, list(map(int, args[:2])))
            elif param == "bins_range":
                if len(args) > 1:
                    if args[1] == "inf":
                        self.__setattr__(param, [int(args[0]), np.inf])
                    else:
                        self.__setattr__(param, list(map(int, args[:2])))
            elif param == "dG_range":
                if len(args) > 1:
                    if args[1] == "inf":
                        self.__setattr__(param, [int(args[0]), np.inf])
                    else:
                        self.__setattr__(param, list(map(int, args[:2])))
            elif param == "p_range":
                if len(args) > 1:
                    self.__setattr__(param, list(map(float, args[:2])))
            elif param == "rd_range":
                if len(args) > 1:
                    self.__setattr__(param, list(map(float, args[:2])))
            elif param == "baf_range":
                if len(args) > 1:
                    self.__setattr__(param, list(map(float, args[:2])))
            elif param == "rd_manhattan_range":
                if len(args) > 1:
                    self.__setattr__(param, list(map(float, args[:2])))
            elif param == "min_segment_size":
                if len(args) > 0:
                    self.__setattr__(param, int(args[0]))
            elif param == "output_filename":
                if len(args) > 0:
                    self.__setattr__(param, args[0])
            elif param == "print_filename":
                if len(args) > 0:
                    if args[0].split(".")[-1] in ["tsv", "vcf", "xlsx"]:
                        self.__setattr__(param, args[0])
                    else:
                        raise (ValueError)
            elif param == "plot_file":
                if len(args) > 0:
                    self.__setattr__(param, int(args[0]))
            elif param == "plot_files":
                self.__setattr__(param, list(map(int, args)))
            elif param == "style":
                if len(args) > 0:
                    self.__setattr__(param, args[0])
            elif param == "matplotlib_use":
                if len(args) > 0:
                    self.__setattr__(param, args[0])
            elif param == "flip_correction_caller":
                if len(args) > 0:
                    self.__setattr__(param, args[0])
            elif param in self.params and self.params[param] is not True:
                self.__setattr__(param, args)
            if param in self.params:
                if self.interactive:
                    print("    * %s: %s" % (param, str(self.params[param])))
            else:
                sp = param.split(".")
                if sp[0] in self.params:
                    if self.interactive:
                        print("    * %s: %s" % (sp[0], str(self.params[sp[0]])))
        except ValueError:
            _logger.warning("Value error while setting %s!" % param)

    def unset(self, param):
        """
        Set parameter to false if bool or restore default in other cases

        Parameters
        ----------
        param : str
            Parameter name

        Returns
        -------
        None

        """
        if param in self.params:
            if type(self.default[param]) == type(True):
                self.__setattr__(param, False)
            else:
                self.__setattr__(param, self.default[param])
            if self.interactive:
                print("    * %s: %s" % (param, str(self.params[param])))

    @property
    def params(self):
        dct = {}
        for key in self.default:
            dct[key] = getattr(self, key)

        return dct

    @property
    def bin_size_f(self):
        """
        Formatted bin_size (e.g. 1000 -> "1K", 10000000 -> "10M")

        Returns
        -------
        bin_size_f : str

        """
        return binsize_format(self.params["bin_size"])

    def __setattr__(self, name, value):

        if name == 'bin_size' and value is not None:
            try:
                value = binsize_type(value)
            except (ArgumentTypeError, ValueError):
                _logger.warning("bin_size should be integer divisible by 100")
        elif name == 'style':
            if value in plt.style.available:
                plt.style.use("default")
                plt.style.use(value)
        elif name == 'xkcd':
            if value:
                self.style = "classic"
                from matplotlib import patheffects
                plt.xkcd()
                plt.rcParams["path.effects"] = [patheffects.withStroke(linewidth=0.5, foreground="w")]

            elif hasattr(self, name) and self.xkcd:
                plt.rcdefaults()
                self.style = 'classic'
        elif name == 'matplotlib_use' and value is not None:
            mpl.use(value)

        super(ViewParams, self).__setattr__(name, value)


class HelpDescription(object):
    default = ViewParams.default

    command_tree = {
        "set": {},
        "unset": {},
        "help": {},
        "save": None,
        "show": None,
        "quit": None,
        "exit": None,
        "rd": None,
        "likelihood": None,
        "baf": None,
        "snp": None,
        "info": None,
        "stat": None,
        "rdstat": None,
        "circular": None,
        "manhattan": None,
        "genotype": None,
        "calls": None,
        "print": {"calls", "merged_calls"},
        "ls": None,
        "meta": None,
        "report": None,
        "compare": None
    }

    param_help = {
        "help": help_format(
            topic="help",
            p_desc="Print help for a topic, command or parameter.",
            p_usage="help <topic>\n\nList of params: " +
                    ", ".join(default.keys()) +
                    "\n\nList of commands: " +
                    ", ".join(command_tree.keys()) +
                    "\n\nList of topics: plotting, signals",
            p_example="help bin_size\nhelp plotting"
        ),
        "plotting": help_format(
            topic="PLOTTING",
            p_desc="There are several types of plots:\n" +
                   "    * genome wide plots: rdstat, stat, rd, baf, snp, likelihood\n" +
                   "    * regions: genomic regions separated by space (new subplot) and comma (same subplot)\n" +
                   "    * manhattan: manhattan style whole genome plot\n" +
                   "    * calls: plot calls\n"
                   "    * circular: circular plots of read-depth and MAF",
            p_example="chr1:1M-20M\nchr21\nchr1:1M-20M,chr2:30M-45M chr21",
            p_see="regions, rdstat, stat, rd, baf, snp, likelihood, manhattan, calls, circular"
        ),
        "regions": help_format(
            topic="Region plot",
            p_desc="Command line is string composed of comma or space separated regions.\n" +
                   "Regions are defined by string using following format: CHR[:START-END]]\n" +
                   "If regions are separated by comma they will be ploted in the same subplot. \n" +
                   "Each region is ploted using multiple panes defined by 'panels' parameter." +
                   "Available panels are: rd, likelihood, snp, snv, snv:callset",
            p_usage="CHR[:START-END]]",
            p_example="chr1:1M-20M\nchr21\nchr1:1M-20M,chr2:30M-45M chr21",
            p_see="plotting, panels, rdstat, stat, rd, baf, snp, likelihood, manhattan, calls, circular"
        ),
        "signals": help_format(
            topic="SIGNALS",
            p_desc="...",
            p_see="plotting"
        ),
        "set": help_format(
            topic="set",
            p_desc="Set parameter value. " +
                   "Requires argument or list of arguments except in the case when parameter type is bool.",
            p_usage="set param [value]",
            p_example="set bin_size 100000\nset rd_call_mosaic\nset panels rd likelihood",
            p_see="unset"
        ),
        "unset": help_format(
            topic="unset",
            p_desc="Set bool parameter to False.",
            p_usage="unset param",
            p_example="unset rd_call_mosaic",
            p_see="unset"
        ),
        "save": help_format(
            topic="save",
            p_desc="Save current figure to file. There is a shortcut (see examples): " +
                   "redirection '>' after plotting command.\n" +
                   "Available formats:\n" +
                   "    * pgf - PGF code for LaTeX\n" +
                   "    * svgz - Scalable Vector Graphics\n" +
                   "    * tiff - Tagged Image File Format\n" +
                   "    * jpg - Joint Photographic Experts Group\n" +
                   "    * raw - Raw RGBA bitmap\n" +
                   "    * jpeg - Joint Photographic Experts Group\n" +
                   "    * png - Portable Network Graphics\n" +
                   "    * ps - Postscript\n" +
                   "    * svg - Scalable Vector Graphics\n" +
                   "    * eps - Encapsulated Postscript\n" +
                   "    * rgba - Raw RGBA bitmap\n" +
                   "    * pdf - Portable Document Format\n" +
                   "    * tif - Tagged Image File Format",
            p_usage="save filename",
            p_example="save image.png\n manhattan > image.png\n chr1:20M-50M > image.png",
            p_see="output_filename"
        ),
        "show": help_format(
            topic="show",
            p_desc="Lists all parameters with values",
            p_usage="show",
            p_see="set, unset"
        ),
        "quit": help_format(
            topic="quit",
            p_desc="Exists interactive mode.",
            p_usage="quit",
            p_see="help, exit"
        ),
        "exit": help_format(
            topic="quit",
            p_desc="Exists interactive mode.",
            p_usage="quit",
            p_see="help, quit"
        ),
        "rd": help_format(
            topic="rd",
            p_desc="Genome wide plot. Plots rd signal from a single cnvpytor file defined by 'plot_file' parameter.",
            p_usage="rd",
            p_example="rd",
            p_see="plotting, regions, panels, rdstat, stat, baf, snp, likelihood, manhattan, calls, circular"
        ),
        "likelihood": help_format(
            topic="likelihood",
            p_desc="Genome wide plot. Plots likelihood from a single cnvpytor file defined by 'plot_file' parameter.",
            p_usage="likelihood",
            p_example="likelihood",
            p_see="plotting, regions, panels, rd, rdstat, stat, baf, snp, manhattan, calls, circular"
        ),
        "snp": help_format(
            topic="snp",
            p_desc="Genome wide plot. Plots SNPs from a single cnvpytor file defined by 'plot_file' parameter.",
            p_usage="snp",
            p_example="snp",
            p_see="plotting, regions, panels, rdstat, stat, baf, rd, likelihood, manhattan, calls, circular"
        ),
        "baf": help_format(
            topic="baf",
            p_desc="Genome wide plot. Plots baf signals from a single cnvpytor file defined by 'plot_file' parameter.",
            p_usage="baf",
            p_example="baf",
            p_see="plotting, regions, panels, rdstat, stat, rd, snp, likelihood, manhattan, calls, circular"
        ),
        "stat": help_format(
            topic="stat",
            p_desc="Plot RD distribution and GC correction curve for bin size given by parameter 'bin_size'.",
            p_usage="stat",
            p_example="stat",
            p_see="rdstat, plotting, bin_size"
        ),
        "rdstat": help_format(
            topic="rdstat",
            p_desc="Plot RD distribution and GC correction curve for 100 bp bin size.",
            p_usage="rdstat",
            p_example="rdstat",
            p_see="stat, plotting"
        ),
        "circular": help_format(
            topic="circular",
            p_desc="Plots RD and MAF signal in circular plot for all chromosomes defined by 'chrom' parameter.",
            p_usage="circular",
            p_example="circular",
            p_see="plotting, manhattan, chrom, bin_size"
        ),
        "manhattan": help_format(
            topic="manhattan",
            p_desc="Scatter plot of RD signal for all chromosomes defined by 'chrom' parameter.",
            p_usage="manhattan",
            p_example="manhattan",
            p_see="plotting, circular, chrom, bin_size"
        ),
        "calls": help_format(
            topic="calls",
            p_desc="Line plot of SNP calls for all chromosomes defined by 'chrom' parameter.",
            p_usage="calls",
            p_example="calls",
            p_see="plotting, manhattan, chrom, bin_size"
        ),
        "compare": help_format(
            topic="compare",
            p_desc="Compare RD in two genomic regions. Plot and print statistics to stdout for each file\n" +
                   "defined by 'plot_files' parameter. Printed columns are:\n" +
                   "filename, REGION1, REGION2, mean rd in REGION1, stdev in REGION1\n" +
                   "mean rd in REGION2, stdev in REGION2, t-test P value, RD ratio, RD ratio error.",
            p_usage="compare REGION1 REGION2",
            p_example="compare 1:10M-20M 2:25M-45M\ncompare 1 X",
            p_see="rdstat, stat"
        ),
        "ls": help_format(
            topic="ls",
            p_desc="Print content of pytor files",
            p_usage="ls",
            p_see="show"
        ),
        "meta": help_format(
            topic="ls",
            p_desc="Print meta information",
            p_usage="ls",
            p_see="show"
        ),
        "report": help_format(
            topic="report",
            p_desc="create a single pytor file report (specified by plot_file) as pdf",
            p_usage="report filename.pdf",
            p_see="ls, info"
        ),
        "bin_size": help_format(
            topic="bin_size",
            p_desc="Size of bins used for plotting",
            p_type="binsize_type (int divisible by 100)",
            p_default=str(default["bin_size"]),
            p_affects="all",
            p_example="set bin_size 100000",
            p_see="output_filename, xkcd"
        ),
        "panels": help_format(
            topic="panels",
            p_desc="List of panels to plot. Possible options are:\n" +
                   "    rd         - read depth plot,\n" +
                   "    likelihood - baf likelihood 2D plot,\n" +
                   "    baf        - binned baf, maf and likelihood peak position,\n" +
                   "    snp        - plot baf for each particular SNP",
            p_type="list of strings",
            p_default=str(default["panels"]),
            p_affects="region plot, manhattan",
            p_example="set panels rd likelihood",
            p_see="grid"
        ),
        "rd_partition": help_format(
            topic="rd_partition",
            p_desc="Enables plotting partition signal in rd plots",
            p_type="bool",
            p_default=str(default["rd_partition"]),
            p_affects="region plot, rd",
            p_example="set rd_partition\nunset rd_partition",
            p_see="rd_call"
        ),
        "rd_call": help_format(
            topic="rd_call",
            p_desc="Enables plotting call signal in rd plots",
            p_type="bool",
            p_default=str(default["rd_call"]),
            p_affects="region plot, rd",
            p_example="set rd_call\nunset rd_call",
            p_see="rd_partition"
        ),
        "rd_manhattan_log_scale": help_format(
            topic="rd_manhattan_log_scale",
            p_desc="Enables log scale in manhattan RD plot",
            p_type="bool",
            p_default=str(default["rd_manhattan_log_scale"]),
            p_affects="manhattan plot",
            p_example="set rd_manhattan_log_scale\nunset rd_manhattan_log_scale",
            p_see="rd_manhattan_range"
        ),
        "plot_baf": help_format(
            topic="plot_baf",
            p_desc="Enables plotting baf signal in baf plots",
            p_type="bool",
            p_default=str(default["plot_baf"]),
            p_affects="region plot, baf",
            p_example="set plot_baf\nunset plot_baf",
            p_see="plot_maf, plot_dbaf, rd_call, rd_call_mosaic"
        ),
        "plot_maf": help_format(
            topic="plot_maf",
            p_desc="Enables plotting maf signal in baf plots",
            p_type="bool",
            p_default=str(default["plot_maf"]),
            p_affects="region plot, baf",
            p_example="set plot_maf\nunset plot_maf",
            p_see="plot_baf, plot_dbaf, rd_call, rd_call_mosaic"
        ),
        "plot_dbaf": help_format(
            topic="plot_dbaf",
            p_desc="Enables plotting dbaf signal in baf plots",
            p_type="bool",
            p_default=str(default["plot_dbaf"]),
            p_affects="region plot, baf",
            p_example="set plot_dbaf\nunset plot_dbaf",
            p_see="plot_maf, plot_baf, rd_partition, rd_call, rd_call_mosaic"
        ),
        "rd_raw": help_format(
            topic="rd_raw",
            p_desc="Enables plotting raw signal in rd plots",
            p_type="bool",
            p_default=str(default["rd_raw"]),
            p_affects="region plot, rd",
            p_example="set rd_raw\nunset rd_raw",
            p_see="rd_corrected, rd_partition, rd_call, rd_call_mosaic"
        ),
        "rd_corrected": help_format(
            topic="rd_corrected",
            p_desc="Enables plotting raw signal in rd plots",
            p_type="bool",
            p_default=str(default["rd_corrected"]),
            p_affects="region plot, rd",
            p_example="set rd_corrected\nunset rd_corrected",
            p_see="rd_raw, rd_partition, rd_call, rd_call_mosaic"
        ),
        "rd_use_mask": help_format(
            topic="rd_use_mask",
            p_desc="If set for all plots rd signal with P mask will be used.",
            p_type="bool",
            p_default=str(default["rd_use_mask"]),
            p_affects="region plot, rd",
            p_example="set rd_use_mask\nunset rd_use_mask",
            p_see="rd_use_gc_corr, snp_use_mask, snp_use_id, snp_use_phase"
        ),
        "rd_use_gc_corr": help_format(
            topic="rd_use_gc_corr",
            p_desc="If set for all plots rd signal with gc correction will be used.",
            p_type="bool",
            p_default=str(default["rd_use_gc_corr"]),
            p_affects="region plot, rd",
            p_example="set rd_use_gc_corr\nunset rd_use_gc_corr",
            p_see="rd_use_mask, snp_use_mask, snp_use_id, snp_use_phase"
        ),
        "rd_range": help_format(
            topic="rd_range",
            p_desc="Range used for y-axis in rd plots defined in mean rd.",
            p_type="two floats",
            p_default=str(default["rd_range"]),
            p_affects="region plot, rd",
            p_example="set rd_range 0 2\nunset rd_range",
            p_see="rd_manhattan_range, rd_colors"
        ),
        "rd_manhattan_range": help_format(
            topic="rd_manhattan_range",
            p_desc="Range used for y-axis in manhattan rd plot defined in copy numbers",
            p_type="two floats",
            p_default=str(default["rd_range"]),
            p_affects="manhattan",
            p_example="set rd_manhattan_range 0 2\nunset rd_manhattan_range",
            p_see="rd_range, rd_colors"
        ),
        "rd_manhattan_call": help_format(
            topic="rd_manhattan_call",
            p_desc="Enables plotting call signal (defined by parameters rd_call and rd_call_mosaic) in manhattan plots",
            p_type="bool",
            p_default=str(default["rd_manhattan_call"]),
            p_affects="manhattan",
            p_example="set rd_manhattan_call\nunset rd_manhattan_call",
            p_see="rd_partition, rd_call, rd_call_mosaic"
        ),
        "snp_use_mask": help_format(
            topic="snp_use_mask",
            p_desc="If set for all plots snp signal with P mask will be used.",
            p_type="bool",
            p_default=str(default["snp_use_mask"]),
            p_affects="region plot, likelihood, baf, snp",
            p_example="set snp_use_mask\nunset snp_use_mask",
            p_see="rd_use_gc_corr, rd_use_mask, snp_use_id, snp_use_phase"
        ),
        "snp_use_id": help_format(
            topic="snp_use_mask",
            p_desc="If set for all plots snp signal with ID filter will be used.",
            p_type="bool",
            p_default=str(default["snp_use_id"]),
            p_affects="region plot, likelihood, baf, snp",
            p_example="set snp_use_id\nunset snp_use_id",
            p_see="rd_use_gc_corr, rd_use_mask, snp_use_mask, snp_use_phase"
        ),
        "snp_use_phase": help_format(
            topic="snp_use_mask",
            p_desc="If set for all plots phased snp signal will be used.",
            p_type="bool",
            p_default=str(default["snp_use_phase"]),
            p_affects="region plot, likelihood, baf, snp",
            p_example="set snp_use_phase\nunset snp_use_phase",
            p_see="rd_use_gc_corr, rd_use_mask, snp_use_mask, snp_use_id"
        ),
        "snp_call": help_format(
            topic="snp_call",
            p_desc="Enables plotting call signal in likelihood/baf plots",
            p_type="bool",
            p_default=str(default["snp_call"]),
            p_affects="region plot, rd",
            p_example="set snp_call\nunset snp_call",
            p_see="rd_call, rd_call_mosaic"
        ),
        "lh_lite": help_format(
            topic="lh_lite",
            p_desc="Enables plotting lite likelihood. Should be used when -baf step is performed with -nolh option",
            p_type="bool",
            p_default=str(default["lh_lite"]),
            p_affects="region plot, rd",
            p_example="set lh_lite\nunset lh_lite",
            p_see="snp_call, rd_call_mosaic"
        ),
        "markersize": help_format(
            topic="markersize",
            p_desc="Size of markers used in scatter like plots (e.g. manhattan, snp).",
            p_type="float or str",
            p_default=str(default["markersize"]),
            p_affects="manhattan, snp, region plot with snp panel",
            p_example="set markersize 10\nset markersize auto",
            p_see="rd_colors, snp_colors, baf_colors, lh_colors, font_size"
        ),
        "font_size": help_format(
            topic="font_size",
            p_desc="Size of font used in all plots (e.g. manhattan, snp).",
            p_type="float or str",
            p_default=str(default["font_size"]),
            p_affects="manhattan, snp, region plot with snp panel",
            p_example="set font_size 10\nset font_size 8",
            p_see="rd_colors, snp_colors, baf_colors, lh_colors, markersize"
        ),
        "rd_colors": help_format(
            topic="rd_colors",
            p_desc="Colors used in rd plot.\n" +
                   "Colors correspond to following signals: raw, gc corrected, partition, call, mosaic 2d call, mosaic baf call",
            p_type="list of strings",
            p_default=str(default["rd_colors"]),
            p_affects="rd, region plot with rd panel",
            p_example="set rd_colors red grey green black blue cyan orange\nunset rd_colors\nset rd_colors.1 red",
            p_see="markersize, snp_colors, baf_colors, lh_colors"
        ),
        "legend": help_format(
            topic="legend",
            p_desc="Enables legend in region plots",
            p_type="bool",
            p_default=str(default["legend"]),
            p_affects="region plot, rd, baf",
            p_example="set legend\nunset legend",
            p_see="rd_range, rd_call"
        ),
        "title": help_format(
            topic="title",
            p_desc="Enables title in region plots",
            p_type="bool",
            p_default=str(default["title"]),
            p_affects="region plot, rd, baf",
            p_example="set title\nunset title",
            p_see="legend"
        ),
        "snp_colors": help_format(
            topic="snp_colors",
            p_desc="Colors used in snp plot.\n" +
                   "Eight colors correspond to following SNPs:\n" +
                   "    " + TerminalColor.YELLOW + "0|0 out of P region, " + TerminalColor.YELLOW2 + "0|0 inside P region,\n" +
                   "    " + TerminalColor.CYAN + "0|1 out of P region, " + TerminalColor.BLUE + "0|1 inside P region,\n" +
                   "    " + TerminalColor.GREEN2 + "1|0 out of P region, " + TerminalColor.GREEN + "1|0 inside P region,\n" +
                   "    " + TerminalColor.YELLOW + "1|1 out of P region, " + TerminalColor.YELLOW2 + "1|1 inside P region.\n" +
                   TerminalColor.DARKCYAN + "P region refers to 1kG project strict mask.\n" +
                   "If snp_alpha_P is set, transparency will be used instead colors for out of P region SNPs.\n",
            p_type="list of strings",
            p_default=str(default["snp_colors"]),
            p_affects="snp, region plot with snp panel",
            p_example="set snp_colors red grey green black blue yellow orange cyan\nunset snp_colors\nset snp_colors.7 red",
            p_see="markersize, rd_colors, baf_colors, lh_colors"
        ),
        "snp_alpha_P": help_format(
            topic="snp_alpha_P",
            p_desc="If set, alpha color value will be used for non-P region SNPs.",
            p_type="bool",
            p_default=str(default["snp_alpha_P"]),
            p_affects="region plot, snp",
            p_example="set snp_alpha_P\nunset snp_alpha_P",
            p_see="snp_colors, snp_use_mask, snp_use_id"
        ),
        "baf_colors": help_format(
            topic="baf_colors",
            p_desc="Colors used in baf plot.\n" +
                   "Colors correspond to following signals: baf, maf, i1 (p2p distance in likelihood function)",
            p_type="list of strings",
            p_default=str(default["baf_colors"]),
            p_affects="baf, region plot with baf panel",
            p_example="set baf_colors red grey green\nunset baf_colors\nset baf_colors.1 red",
            p_see="markersize, snp_colors, rd_colors, lh_colors"
        ),
        "lh_colors": help_format(
            topic="lh_colors",
            p_desc="Colors used in likelihood plot.\n" +
                   "Colors correspond to following signals: likelihood call (snp_call parameter)",
            p_type="list of strings",
            p_default=str(default["lh_colors"]),
            p_affects="likelihood, region plot with likelihood panel",
            p_example="set baf_colors green\nunset baf_colors\nset baf_colors.0 red",
            p_see="markersize, baf_colors, rd_colors, lh_colors, snp_call"
        ),
        "plot_files": help_format(
            topic="plot_files",
            p_desc="Indices of files to be plot. Only for plots that support multi file plotting.\n" +
                   "One file can be ploted multiple times. Use 'show' to view list of files.",
            p_type="list of integers",
            p_default=str(default["plot_files"]),
            p_affects="region plot, manhattan, circular, compare",
            p_example="set plot_files 0 1 2\nunset plot_files",
            p_see="plot_file, panels"
        ),
        "plot_file": help_format(
            topic="plot_file",
            p_desc="Index of a file to be plot. Only for single file plots.\n" +
                   "Use 'show' to view list of files.",
            p_type="integer",
            p_default=str(default["plot_file"]),
            p_affects="rd, likelihood, baf, snp, snv",
            p_example="set plot_files 0 1 2\nunset plot_files",
            p_see="plot_file, panels"
        ),
        "file_titles": help_format(
            topic="file_titles",
            p_desc="List of titles used with multiple file plots. If empty filename will be used instead.",
            p_type="list of str",
            p_default=str(default["file_titles"]),
            p_affects="manhattan, circular",
            p_example="set file_titles Title1 Title2\nunset file_titles",
            p_see="plot_files, grid"
        ),
        "chrom": help_format(
            topic="chrom",
            p_desc="List of chromosomes to be plotted. All available will be plotted if empty.",
            p_type="list of str",
            p_default=str(default["chrom"]),
            p_affects="manhattan, rd, likelihood, baf, snp. snv, circular",
            p_example="set chrom 1 2 3 MT\nset chrom chr1 chr15 chrX \nunset chrom",
            p_see="plot_files, plot_file"
        ),
        "style": help_format(
            topic="style",
            p_desc="Matplotlib style to be used.\n" +
                   "Use double <tab> after 'set style' to get list of all available styles.",
            p_type="str",
            p_default=str(default["style"]),
            p_affects="all plots",
            p_example="set style seaborn\nunset style",
            p_see="xkcd, chrom, output_filename"
        ),
        "matplotlib_use": help_format(
            topic="matplotlib_use",
            p_desc="Change matplotlib backend.",
            p_type="str",
            p_default=str(default["matplotlib_use"]),
            p_affects="all plots",
            p_example="set matplotlib_use agg",
            p_see="style, xkcd, chrom, output_filename"
        ),
        "grid": help_format(
            topic="grid",
            p_desc="Set plot layout grid. Automatic if 'auto'.",
            p_type="two integers, 'auto', 'vertical' or 'horizontal'",
            p_default=str(default["grid"]),
            p_affects="all plots",
            p_example="set grid 5 4\nset grid horizontal\nunset grid",
            p_see="subgrid, xkcd, chrom, output_filename"
        ),
        "subgrid": help_format(
            topic="subgrid",
            p_desc="Set plot layout subgrid. Automatic if 'auto'.",
            p_type="two integers, 'auto', 'vertical' or 'horizontal'",
            p_default=str(default["subgrid"]),
            p_affects="plots with multiple panels",
            p_example="set subgrid 5 4\nset subgrid horizontal\nunset subgrid",
            p_see="grid, xkcd, chrom, output_filename"
        ),
        "panel_size": help_format(
            topic="panel_size",
            p_desc="Set plot panel size.",
            p_type="two floats",
            p_default=str(default["panel_size"]),
            p_affects="plots with multiple panels",
            p_example="set panel_size 8 1\nunset panel_size",
            p_see="grid, subgrid, output_filename"
        ),
        "xkcd": help_format(
            topic="xkcd",
            p_desc="Use xkcd comic plot style (see http://xkcd.com).",
            p_type="bool",
            p_default=str(default["xkcd"]),
            p_affects="all plots",
            p_example="set xkcd\nunset xkcd",
            p_see="style, chrom, output_filename"
        ),
        "plot": help_format(
            topic="plot",
            p_desc="Plots when true (works with compare and print).",
            p_type="bool",
            p_default=str(default["plot"]),
            p_affects="compare, print",
            p_example="set plot\nunset plot",
            p_see="compare, print calls, print join_calls"
        ),
        "output_filename": help_format(
            topic="output_filename",
            p_desc="If not empty plots will be store into file without plotting on the screen." +
                   "Use one of following extensions:\n" +
                   "    * pgf - PGF code for LaTeX\n" +
                   "    * svgz - Scalable Vector Graphics\n" +
                   "    * tiff - Tagged Image File Format\n" +
                   "    * jpg - Joint Photographic Experts Group\n" +
                   "    * raw - Raw RGBA bitmap\n" +
                   "    * jpeg - Joint Photographic Experts Group\n" +
                   "    * png - Portable Network Graphics\n" +
                   "    * ps - Postscript\n" +
                   "    * svg - Scalable Vector Graphics\n" +
                   "    * eps - Encapsulated Postscript\n" +
                   "    * rgba - Raw RGBA bitmap\n" +
                   "    * pdf - Portable Document Format\n" +
                   "    * tif - Tagged Image File Format",
            p_type="str",
            p_default=str(default["output_filename"]),
            p_affects="all plots",
            p_example="set output_filename filename.png\nunset output_filename",
            p_see="save, dpi, style, xkcd"
        ),
        "print_filename": help_format(
            topic="output_filename",
            p_desc="If not empty calls will be printed into specified file." +
                   "Use one of following extensions:\n" +
                   "    * tsv - tab separated\n" +
                   "    * xlsx - Excel format\n" +
                   "    * vcf - VCF file format (not working for merged calls)",
            p_type="str",
            p_default=str(default["output_filename"]),
            p_affects="print",
            p_example="set print_filename filename.tsv\nunset print_filename",
            p_see="print, callers"
        ),
        "flip_correction_caller": help_format(
            topic="flip_correction_caller",
            p_desc="Use haplotype switch correction for phased SNP plots." +
                   "Takes one of following values (caller name):\n" +
                   "    * baf_mosaic\n" +
                   "    * combined_mosaic\n" +
                   "    * None (default)",
            p_type="str",
            p_default=str(default["flip_correction_caller"]),
            p_affects="region plot",
            p_example="set flip_correction_caller baf_mosaic\nunset flip_correction_caller",
            p_see="snp_use_phase, callers"
        ),
        "callers": help_format(
            topic="callers",
            p_desc="List of callers to use for plotting and printing. Possible options are:\n" +
                   "    rd_mean_shift    - read depth mean shift caller,\n" +
                   "    rd_mosaic    - read depth mosaic caller (under development),\n" +
                   "    baf_mosaic    - baf mosaic caller (under development),\n" +
                   "    combined_mosaic  - read depth and baf mosaic caller (under development).",
            p_type="list of strings",
            p_default=str(default["callers"]),
            p_affects="region plot, manhattan",
            p_example="set callers rd_mean_shift\nunset callers",
            p_see="plotting, print"
        ),
        "print": help_format(
            topic="print",
            p_desc="Print filtered calls.",
            p_usage="print [calls, merged_calls]",
            p_example="print calls\nprint merged_calls",
            p_see="Q0_range, p_range, pN_range, size_range, dG_range, callers"
        ),
        "rd_circular_colors": help_format(
            topic="rd_circular_colors",
            p_desc="Colors used in circular plot for filling chromosomes in rd signal.",
            p_type="list of strings",
            p_default=str(default["rd_circular_colors"]),
            p_affects="circular",
            p_example="set rd_circular_colors red grey green black blue\nunset rd_circular_colors\nset rd_circular_colors.1 red",
            p_see="snp_circular_colors, circular, rd_colors, snp_colors, baf_colors, lh_colors"
        ),
        "snp_circular_colors": help_format(
            topic="snp_circular_colors",
            p_desc="Colors used in circular plot for filling chromosomes in snp signal.",
            p_type="list of strings",
            p_default=str(default["snp_circular_colors"]),
            p_affects="circular",
            p_example="set snp_circular_colors red grey green black blue\nunset snp_circular_colors\nset snp_circular_colors.1 red",
            p_see="rd_circular_colors, circular, rd_colors, snp_colors, baf_colors, lh_colors"
        ),
        "contrast": help_format(
            topic="contrast",
            p_desc="Contrast used for transparency in snp call plots.",
            p_type="float",
            p_default=str(default["contrast"]),
            p_affects="calls, likelihood, region plot",
            p_example="set contrast 100\nunset contrast",
            p_see="min_segment_size"
        ),
        "min_segment_size": help_format(
            topic="min_segment_size",
            p_desc="Threshold for call size used in snp call plots.",
            p_type="float",
            p_default=str(default["min_segment_size"]),
            p_affects="calls, likelihood, region plot",
            p_example="set min_segment_size 10\nunset min_segment_size",
            p_see="contrast"
        ),
        "Q0_range": help_format(
            topic="Q0_range",
            p_desc="Range used to filter Q0 for calls",
            p_type="two floats",
            p_default=str(default["Q0_range"]),
            p_affects="calls plot",
            p_example="set Q0_range 0 0.5\nunset Q0_range",
            p_see="pN_range, size_range, dG_range, p_range, baf_range, bins_range"
        ),
        "pN_range": help_format(
            topic="pN_range",
            p_desc="Range used to filter percentage of reference genome gaps for calls",
            p_type="two floats",
            p_default=str(default["pN_range"]),
            p_affects="calls plot",
            p_example="set pN_range 0 0.5\nunset pN_range",
            p_see="Q0_range, size_range, dG_range, p_range, baf_range, bins_range"
        ),
        "size_range": help_format(
            topic="size_range",
            p_desc="Range used to filter size of calls",
            p_type="two integers or integer and 'inf' (for unlimited upper bound)",
            p_default=str(default["size_range"]),
            p_affects="calls plot",
            p_example="set size_range 100000 10000000\nset size_range 100000 inf\nunset size_range",
            p_see="Q0_range, pN_range, p_range, dG_range, baf_range, bins_range"
        ),
        "bins_range": help_format(
            topic="bins_range",
            p_desc="Range used to filter calls based on number of call bins with signal",
            p_type="two integers or integer and 'inf' (for unlimited upper bound)",
            p_default=str(default["bins_range"]),
            p_affects="calls plot",
            p_example="set size_range 2 100\nset bins_range 5 inf\nunset bins_range",
            p_see="Q0_range, pN_range, p_range, dG_range, baf_range, size_range"
        ),
        "dG_range": help_format(
            topic="size_range",
            p_desc="Range used to filter calls on distance from closest large (>100bp) gap in reference genome",
            p_type="two integers or integer and 'inf' (for unlimited upper bound)",
            p_default=str(default["dG_range"]),
            p_affects="calls plot",
            p_example="set dG_range 100000 10000000\nset dG_range 100000 inf\nunset dG_range",
            p_see="Q0_range, pN_range, size_range, p_range, baf_range, bins_range"
        ),
        "p_range": help_format(
            topic="p_range",
            p_desc="Range used to filter calls based on e-value (e-val1)",
            p_type="two floats",
            p_default=str(default["p_range"]),
            p_affects="calls plot",
            p_example="set p_range 0 0.000001\nunset p_range",
            p_see="Q0_range, pN_range, size_range, dG_range, baf_range, bins_range"
        ),
        "baf_range": help_format(
            topic="baf_range",
            p_desc="Range used to filter baf for calls",
            p_type="two floats",
            p_default=str(default["baf_range"]),
            p_affects="calls plot",
            p_example="set baf_range 0.4 0.5\nunset baf_range",
            p_see="pN_range, size_range, dG_range, p_range, Q0_range, bins_range"
        ),
        "dpi": help_format(
            topic="dpi",
            p_desc="Resolution (dots per inch) used for plotting.",
            p_type="int",
            p_default=str(default["dpi"]),
            p_affects="calls, likelihood, region plot",
            p_example="set dpi 300\nunset dpi",
            p_see="margins, style, output_filename, xkcd"
        ),
        "margins": help_format(
            topic="margins",
            p_desc="Margins used for matplotlib figure:\n" +
                   "[bottom, top, left, right, wspace, hspace]",
            p_type="list of floats",
            p_default=str(default["margins"]),
            p_affects="all plots",
            p_example="set margins 0 0 0 0 0 0\nunset margins\nset margins.3 0.2",
            p_see="style, output_filename, dpi"
        ),
    }
