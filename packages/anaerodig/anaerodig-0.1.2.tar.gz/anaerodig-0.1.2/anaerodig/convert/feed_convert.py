from abc import ABC, abstractmethod

from anaerodig.pyad.feed import DigesterFeed


class FeedConverter(ABC):
    """Store implementation of Feed conversion from model to another

    Note: __init__ should be used to store all the variables beyond the
    feed which are required for the conversion.

    Use of this class:
    >> feed_model_2 = FeedConverter(extra_param_1, extra_param_2).convert(feed_model_1)
    """

    @abstractmethod
    def convert(self, feed: DigesterFeed) -> DigesterFeed:
        """Convert Feed information from one format to another"""
