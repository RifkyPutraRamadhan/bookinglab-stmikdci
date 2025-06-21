from .fifo import fifo_scheduling
from .sjf import sjf_scheduling
from .rr import round_robin_scheduling

__all__ = ['fifo_scheduling', 'sjf_scheduling', 'round_robin_scheduling']