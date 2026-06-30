from algorithms.uninformed.bfs import bfs1, bfs2
from algorithms.uninformed.dfs import dfs1, dfs2
from algorithms.uninformed.ucs import ucs_standard
from algorithms.uninformed.iddfs import iddfs

from algorithms.informed.gbfs import gbfs
from algorithms.informed.a_star import a_star
from algorithms.informed.ida_star import ida_star

from algorithms.complex_env.belief_dfs import belief_dfs, sensorless_belief_dfs
from algorithms.complex_env.partially_observable_dfs import partially_observable_belief_dfs
from algorithms.complex_env.and_or_search import and_or_graph_search

from algorithms.local_search.hill_climbing import (
    simple_hill_climbing,
    steepest_ascent_hill_climbing,
    stochastic_hill_climbing,
    random_restart_hill_climbing,
    local_beam_search
)
from algorithms.local_search.simulated_annealing import simulated_annealing

from algorithms.csp.backtracking import (
    backtracking_search,
    HCMC_DISTRICTS,
    HCMC_NEIGHBORS,
    DISTRICT_POSITIONS,
    COLOR_HEX
)
from algorithms.csp.ac3 import mac_search
from algorithms.csp.min_conflicts import min_conflicts_search
from algorithms.csp.map_data import DISTRICT_POLYGONS

from algorithms.adversarial_search.minimax import minimax_generator, play_tictactoe_ai_vs_ai
