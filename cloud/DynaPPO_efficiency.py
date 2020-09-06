import os
import sys

sys.path.append("../")
import RNA
from evaluators.Evaluator import Evaluator
from explorers.DynaPPO_explorer import DynaPPO_explorer
from models.Ground_truth_oracles.RNA_landscape_models import RNA_landscape_constructor
from models.Ground_truth_oracles.TF_binding_landscape_models import *
from models.Noisy_models.Ensemble import Ensemble_models
from models.Noisy_models.Neural_network_models import NN_model
from utils.model_architectures import NLNN, CNNa, Linear
from utils.sequence_utils import generate_random_mutant

LANDSCAPE_TYPES_RNA = {"RNA": [0], "TF": []}

dynappo_explorer = DynaPPO_explorer(batch_size=100, virtual_screen=20)
dynappo_explorer.debug = False

os.makedirs("../simulations/eval/RNA/DynaPPO/", exist_ok=True)
evaluator_dynappo = Evaluator(
    dynappo_explorer,
    landscape_types=LANDSCAPE_TYPES_RNA,
    path="../simulations/eval/RNA/DynaPPO/",
    adaptive_ensemble=False,
)
evaluator_dynappo.evaluate_for_landscapes(evaluator_dynappo.efficiency, num_starts=3)
