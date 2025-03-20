from typing import List, Optional, Tuple

from matplotlib import pyplot as plt

from clscurves.plotter.plotter import MetricsPlotter
from clscurves.utils import MetricsResult


class PRGPlotter(MetricsPlotter):
    """Plot the PRG (Precision-Recall-Gain) curve.

    "Precision-Recall-Gain" plots defined
    `here <https://papers.nips.cc/paper/2015/file/33e8075e9970de0cfea955afd464\
    4bb2-Paper.pdf>`_.

    A "weighted recall" variant of Recall Gain is not discussed in the paper,
    and may not have any theoretical guarantees or reasonable interpretations.
    Because it's unclear how a positive-example weight should affect the
    quantities in a PRG plot, we do not support weighted plotting at this time.
    """

    def __init__(
        self,
        metrics: MetricsResult,
        score_is_probability: bool,
    ) -> None:
        super().__init__(metrics, score_is_probability)

    def plot_prg(
        self,
        title: str = "Precision-Recall-Gain Curve",
        cmap: str = "rainbow",
        color_by: str = "thresh",
        cbar_rng: Optional[List[float]] = None,
        cbar_label: Optional[str] = None,
        grid: bool = True,
        dpi: Optional[int] = None,
        bootstrapped: bool = False,
        bootstrap_alpha: float = 0.15,
        bootstrap_color: str = "black",
        imputed: bool = False,
        op_value: Optional[float] = None,
        return_fig: bool = False,
    ) -> Optional[Tuple[plt.Figure, plt.Axes]]:
        """Plot the PRG (Precision-Recall-Gain) curve.

        Parameters
        ----------
        title
            Title of plot.
        cmap
            Colormap string specification.
        color_by
            Name of key in metrics.curves that specifies which values to use
            when coloring points along the PRG curve; this should be either
            "frac" for fraction of cases flagged or "thresh" for score
            discrimination threshold.
        cbar_rng
            Specify a color bar range of the form [min_value, max_value] to
            override the default range.
        cbar_label
            Custom label to apply to the color bar. If None is supplied,
            the default ("Threshold Value" or "Fraction Flagged", depending on
            the ``color_by`` value) will be used.
        grid
            Whether to plot grid lines.
        dpi
            Resolution in "dots per inch" of resulting figure. If not
            specified, the Matplotlib default will be used. A good rule of
            thumb is 150 for good quality at normal screen resolutions and 300
            for high quality that maintains sharp features after zooming in.
        bootstrapped
            Specifies whether bootstrapped curves should be plotted behind the
            main colored performance scatter plot.
        bootstrap_alpha
            Opacity of bootstrap curves.
        bootstrap_color
            Color of bootstrap curves.
        imputed
            Whether to plot imputed curves.
        op_value
            Threshold value to plot a confidence ellipse for when the plot is
            bootstrapped.
        return_fig
            If set to True, will return (fig, ax) as a tuple instead of
            plotting the figure.
        """

        # Get metrics
        curves, scalars = self._get_metrics(imputed=imputed)

        # Specify which values to plot in X and Y
        x_col = "recall_gain"
        y_col = "precision_gain"

        # Make plot
        if not bootstrapped:
            fig, ax = self._make_plot(
                curves=curves,
                x_col=x_col,
                y_col=y_col,
                cmap=cmap,
                dpi=dpi,
                color_by=color_by,
                cbar_rng=cbar_rng,
                cbar_label=cbar_label,
                grid=grid,
            )
        else:
            fig, ax = self._make_bootstrap_plot(
                curves=curves,
                x_col=x_col,
                y_col=y_col,
                cmap=cmap,
                dpi=dpi,
                color_by=color_by,
                cbar_rng=cbar_rng,
                cbar_label=cbar_label,
                grid=grid,
                alpha=bootstrap_alpha,
                bootstrap_color=bootstrap_color,
            )

        # Extract PRG AUC
        scalars = scalars.loc[lambda x: x["_bootstrap_sample"].isnull()]
        auc = scalars["prg_auc"].iloc[0]

        # Extract class imbalance
        imb = scalars["imbalance"].iloc[0]

        # Compute the ratio of class sizes
        class_ratio = 1 / (imb + 1e-9) - 1

        # Plot line of randomness
        ax.plot([0, 1], [1, 0], "k-")

        # Add AUC to plot
        ax.text(
            x=0.06,
            y=0.13,
            s="%sAUPRG = %.3f" % ("Mean " if bootstrapped else "", auc),
            ha="left",
            va="center",
            bbox=dict(facecolor="gray", alpha=0.1, boxstyle="round"),
        )

        # Add class imbalance to plot
        ax.text(
            x=0.06,
            y=0.07,
            s="%sClass Imb. = %.1f : 1"
            % ("Mean " if bootstrapped else "", class_ratio),
            ha="left",
            va="center",
            bbox=dict(facecolor="gray", alpha=0.1, boxstyle="round"),
        )

        # Plot 95% confidence ellipse
        if op_value is not None:
            self._add_op_ellipse(
                curves=curves,
                op_value=op_value,
                x_col=x_col,
                y_col=y_col,
                ax=ax,
                thresh_key=color_by,
            )

        # Set labels
        ax.set_xlabel("Recall Gain = (Rec - pp)/((1 - pp) * Rec)")
        ax.set_ylabel("Precision Gain = (Prec - pp)/((1 - pp) * Prec)")
        ax.set_title(title)

        if return_fig:
            return fig, ax

        else:
            # Display and close plot
            plt.show()
            plt.close()

        return None
