import click
from createXML import createXML
from readInputMethylation import readMethylation
from collections import OrderedDict
from math import ceil, floor

"""
This script is intended to be used for the FlipFlop model. It can create the XML file needed to run the model in BEAST.
It only needs the beta values of the fCpGs in a data frame in comma-separated format. Rows represent each fCpG, columns
represent each sample
"""


class CustomOption(click.Option):
    def __init__(self, *args, **kwargs):
        kwargs.update({"show_default": True})
        self.help_group = kwargs.pop("help_group", None)
        super(CustomOption, self).__init__(*args, **kwargs)


class CustomCommand(click.Command):
    def format_options(self, ctx, formatter):
        """Writes all the options into the formatter if they exist."""
        opts = OrderedDict()
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None:
                if hasattr(param, "help_group") and param.help_group:
                    opts.setdefault(str(param.help_group), []).append(rv)
                else:
                    opts.setdefault("Options", []).append(rv)

        for name, opts_group in opts.items():
            with formatter.section(name):
                formatter.write_dl(opts_group)


@click.command(cls=CustomCommand)
@click.option("--input", cls=CustomOption, required=True, help="Methylation array beta values in CSV format", type=str, help_group="Inputs")
@click.option("--samplesheet", cls=CustomOption, required=True, help="Methylation array sample sheet", type=str, help_group="Inputs")
@click.option("--stemCells", "stemCells", cls=CustomOption, default=3, help="Prior for the stemCells parameter", type=int, help_group="Priors")
@click.option("--delta", cls=CustomOption, default=0.2, help="Prior for the delta parameter", type=float, help_group="Priors")
@click.option("--eta", cls=CustomOption, default=0.7, help="Prior for the eta parameter", type=float, help_group="Priors")
@click.option("--kappa", cls=CustomOption, default=50, help="Prior for the kappa parameter", type=float, help_group="Priors")
@click.option("--mu", cls=CustomOption, default=0.1, help="Prior for the mu parameter", type=float, help_group="Priors")
@click.option("--gamma", cls=CustomOption, default=0.1, help="Prior for the gamma parameter", type=float, help_group="Priors")
@click.option("--lambda", "Lambda", cls=CustomOption, default=1, help="Prior for the lambda parameter", type=float, help_group="Priors")
@click.option("--mle", cls=CustomOption, default=False, help="Whether MLE estimation is used", is_flag=True, help_group="MLE estimation module")
@click.option("--mle-steps", "mle_steps", cls=CustomOption, default=100, help="Number of power posteriors to use for MLE", type=click.INT, help_group="MLE estimation module")
@click.option(
    "--mle-iterations", "mle_iterations", cls=CustomOption, help="Number of MCMC iterations to run in each step. Defaults to MCMC --iterations / --mle-steps.", type=click.INT, help_group="MLE estimation module"
)
@click.option("--mle-sampling", "mle_sampling", cls=CustomOption, help="Sampling period for the power-posterior MCMC samplers. Defaults to --iterations / 1000", type=click.INT, help_group="MLE estimation module")
@click.option("--mle-ps", "mle_ps", cls=CustomOption, default=False, help="Activates/deactivates the analysis of the MLE samples to estimate the MLE using Path Sampling", is_flag=True, help_group="MLE estimation module")
@click.option(
    "--mle-ss", "mle_ss", cls=CustomOption, default=False, help="Activates/deactivates the analysis of the MLE samples to estimate the MLE using Stepping Stone", is_flag=True, help_group="MLE estimation module"
)
@click.option("--hme", cls=CustomOption, default=False, help="Activates/deactivates the estimation of the MLE using the Harmonic Mean Estimate", is_flag=True, help_group="MLE estimation module")
@click.option("--luca-mode", "luca_mode", cls=CustomOption, default="auto", help="Should LUCA be fixed to birth or free (recomended when no normals available)", type=click.Choice(['auto', 'free', 'fixed'], case_sensitive=False), help_group="Extra parameters")
@click.option("--age-col", "age_col", cls=CustomOption, default="Age", help="Name of the age column in the samplesheet", type=str, help_group="Extra parameters")
@click.option("--age-diagnosis-col", "age_diagnosis_col", cls=CustomOption, required=False, help="Age at diagnosis column in sample sheet", type=str, help_group="Extra parameters")
@click.option("--sample-col", "sample_col", cls=CustomOption, default="Sample", help="Name of the sample column in the samplesheet. It should contain the names in the betas file", type=str, help_group="Extra parameters")
@click.option("--sample-type-col", "sample_type_col", cls=CustomOption, default="Group", help="Name of the grouping column in the samplesheet. It should tell which samples are tumoral and which ones are normal", type=str, help_group="Extra parameters")
@click.option("--iterations", cls=CustomOption, default=750_000, help="Number of MCMC iterations (chain length)", type=int, help_group="Extra parameters")
@click.option("--precision", cls=CustomOption, default=3, help="Number of significant digits to consider when rounding the values", type=int, help_group="Extra parameters")
@click.option("--sampling", cls=CustomOption, default=75, help="Frequency of sampling in the log file", type=int, help_group="Extra parameters")
@click.option("--screenSampling", "screenSampling", cls=CustomOption, default=75, help="Frequency of sampling to print in the screen", type=int, help_group="Extra parameters")
@click.option("--stripRownames", "stripRownames", cls=CustomOption, default=False, help="Whether the input contains row names or not (they need to be removed)", is_flag=True, help_group="Extra parameters")
@click.option("--output", cls=CustomOption, default="test", help="Output prefix for the analysis files (XML, trees, logs...)", type=str, help_group="Extra parameters")
def main(
    input: str,
    samplesheet: str,
    stemCells: int,
    delta: float,
    eta: float,
    kappa: float,
    mu: float,
    gamma: float,
    Lambda: float,
    mle_iterations: int,
    mle_sampling: int,
    age_col: str,
    age_diagnosis_col: str,
    sample_col: str,
    sample_type_col: str,
    iterations: int = 20_000,
    precision: int = 3,
    sampling: int = 200,
    screenSampling: int = 200,
    output: str = "test",
    stripRownames: bool = True,
    mle: bool = False,
    mle_steps: int = 100,
    mle_ps: bool = False,
    mle_ss: bool = False,
    hme: bool = False,
    luca_mode: str = "auto",
) -> None:
    myobj = readMethylation(input, precision, stripRownames, samplesheet, age_col, age_diagnosis_col, sample_col, sample_type_col, luca_mode)
    myobj.parseSamples()

    if mle_ps or mle_ss or hme:
        mle = True

    if mle:
        mle_iterations = ceil(iterations // mle_steps) if mle_iterations is None else mle_iterations
        mle_sampling = floor(mle_iterations // 1000) if mle_sampling is None else mle_sampling

    XMLfile = createXML(stemCells=stemCells, delta=delta, eta=eta, kappa=kappa, mu=mu, gamma=gamma, Lambda=Lambda)
    XMLfile.addSamples(myobj)
    XMLfile.buildDoc(output, iterations=iterations, sampling=sampling, screenSampling=screenSampling, mle=mle, mle_ss=mle_ss, mle_ps=mle_ps, hme=hme, mle_iterations=mle_iterations, mle_sampling=mle_sampling)
    XMLfile.printDocument(output)


if __name__ == "__main__":
    main()
