import numpy as np
import pandas as pd
from anaerodig.convert.feed_convert import FeedConverter
from anaerodig.pyadm1.basic_classes.feed import ADM1Feed
from anaerodig.pyam2.basic_classes.feed import AM2Feed


class ADM1ToAM2FeedConverter(FeedConverter):
    """Feed conversion between ADM1 to AM2.

    Requires (beyond ADM1Feed):
        pH_feed: Measure of pH of entering feed, either a time series of same length as feed,
            or a float
        V_liq: Volume of liquid phase in the digester
        pH: Measure of the pH in the digester, either a time series of same length as feed, or a
            float
    """

    def __init__(self, pH_feed, V_liq, pH):
        self.pH_feed = pH_feed
        self.V_liq = V_liq
        self.pH = pH

    def convert(self, feed: ADM1Feed) -> AM2Feed:
        """
        Convert feed information designed for ADM1 to feed information for AM2

        Input feed should be a dataframe containing the following columns (with units)
            "time": # Day
            "S_su"  # kgCOD M-3
            "S_aa"  # kgCOD M-3
            "S_fa"  # kgCOD M-3
            "S_va" # kgCOD M-3
            "S_bu" # kgCOD M-3
            "S_pro"  # kgCOD M-3
            "S_ac"  # kgCOD M-3
            "S_h2" # kgCOD M-3
            "S_ch4" # kgCOD M-3
            "S_IC" # kgCOD M-3
            "S_IN" # kmole N M-3
            "S_I" # kmole C M-3
            "X_c" # kgCOD m-3
            "X_ch" # kgCOD m-3
            "X_pr" # kgCOD M-3
            "X_li" # kgCOD M-3
            "X_su" # kgCOD M-3
            "X_aa" # kgCOD M-3
            "X_fa" # kgCOD M-3
            "X_c4"  # kgCOD M-3
            "X_pro" # kgCOD M-3
            "X_ac" # kgCOD M-3
            "X_h2" # kgCOD M-3
            "X_I"  # kgCOD M-3
            "S_cation"  # kmole M-3
            "S_anion"  # kmole M-3
            "Q"  # M3 Day-1

        Note:
        Columns "S_h2", "S_ch4", "S_IN", "S_I", "X_I", "S_cation", "S_anion", "Q" are not used and as
            such not necessary. Mentionned for coherence with ADM1 standards

        Output:
            A numpy.ndarray which can be used as DigesterFeed for AM2
        """
        # Prepare ShCO3
        ShCO3 = np.exp(-np.log(10.0) * (14 - self.pH_feed))

        # Compute AM2 feed columns

        X1_in = (feed.df["X_su"] + feed.df["X_aa"] + feed.df["X_fa"]) / 1.55
        X2_in = (
            feed.df["X_ac"] + feed.df["X_h2"] + feed.df["X_c4"] + feed.df["X_pro"]
        ) / 1.55

        S1_in = (
            feed.df["S_su"]
            + feed.df["S_aa"]
            + feed.df["S_fa"]
            + feed.df["X_c"]
            + feed.df["X_ch"]
            + feed.df["X_pr"]
            + feed.df["X_li"]
        )
        S2_in = (
            (feed.df["S_va"] / 208)
            + (feed.df["S_bu"] / 160)
            + (feed.df["S_pro"] / 112)
            + (feed.df["S_ac"] / 64)
        ) * 1000

        Z_in = (
            (feed.df["S_va"] / 208)
            + (feed.df["S_bu"] / 160)
            + (feed.df["S_pro"] / 112)
            + (feed.df["S_ac"] / 64)
            + ShCO3
        ) * 1000
        C_in = feed.df["S_IC"].to_numpy() * 1000

        D = feed.df["Q"] / self.V_liq

        # Prepare dataFrame
        Data = np.array(
            [feed.df["time"].to_numpy(), D, X1_in, X2_in, S1_in, S2_in, Z_in, C_in]
        ).T
        n_feed = pd.DataFrame(
            Data, columns=["time", "D", "X1", "X2", "S1", "S2", "Z", "C"]
        )
        n_feed["pH"] = self.pH

        return AM2Feed(n_feed)
