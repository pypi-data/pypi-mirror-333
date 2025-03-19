# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from torchrl.modules.tensordict_module.common import DistributionalDQNnet

from .distributions import (
    Delta,
    distributions_maps,
    IndependentNormal,
    MaskedCategorical,
    MaskedOneHotCategorical,
    NormalParamExtractor,
    NormalParamWrapper,
    OneHotCategorical,
    OneHotOrdinal,
    Ordinal,
    ReparamGradientStrategy,
    TanhDelta,
    TanhNormal,
    TruncatedNormal,
)
from .models import (
    BatchRenorm1d,
    ConsistentDropout,
    ConsistentDropoutModule,
    Conv3dNet,
    ConvNet,
    DdpgCnnActor,
    DdpgCnnQNet,
    DdpgMlpActor,
    DdpgMlpQNet,
    DecisionTransformer,
    DreamerActor,
    DTActor,
    DuelingCnnDQNet,
    MLP,
    MultiAgentConvNet,
    MultiAgentMLP,
    MultiAgentNetBase,
    NoisyLazyLinear,
    NoisyLinear,
    ObsDecoder,
    ObsEncoder,
    OnlineDTActor,
    QMixer,
    reset_noise,
    RSSMPosterior,
    RSSMPrior,
    RSSMRollout,
    Squeeze2dLayer,
    SqueezeLayer,
    VDNMixer,
)
from .tensordict_module import (
    Actor,
    ActorCriticOperator,
    ActorCriticWrapper,
    ActorValueOperator,
    AdditiveGaussianModule,
    AdditiveGaussianWrapper,
    DecisionTransformerInferenceWrapper,
    DistributionalQValueActor,
    DistributionalQValueHook,
    DistributionalQValueModule,
    EGreedyModule,
    EGreedyWrapper,
    GRU,
    GRUCell,
    GRUModule,
    LMHeadActorValueOperator,
    LSTM,
    LSTMCell,
    LSTMModule,
    MultiStepActorWrapper,
    OrnsteinUhlenbeckProcessModule,
    OrnsteinUhlenbeckProcessWrapper,
    ProbabilisticActor,
    QValueActor,
    QValueHook,
    QValueModule,
    recurrent_mode,
    SafeModule,
    SafeProbabilisticModule,
    SafeProbabilisticTensorDictSequential,
    SafeSequential,
    set_recurrent_mode,
    TanhModule,
    ValueOperator,
    VmapModule,
    WorldModelWrapper,
)
from .utils import get_primers_from_module
from .planners import CEMPlanner, MPCPlannerBase, MPPIPlanner  # usort:skip

__all__ = [
    "DistributionalDQNnet",
    "Delta",
    "distributions_maps",
    "IndependentNormal",
    "MaskedCategorical",
    "MaskedOneHotCategorical",
    "NormalParamExtractor",
    "NormalParamWrapper",
    "OneHotCategorical",
    "OneHotOrdinal",
    "Ordinal",
    "ReparamGradientStrategy",
    "TanhDelta",
    "TanhNormal",
    "TruncatedNormal",
    "BatchRenorm1d",
    "ConsistentDropout",
    "ConsistentDropoutModule",
    "Conv3dNet",
    "ConvNet",
    "DdpgCnnActor",
    "DdpgCnnQNet",
    "DdpgMlpActor",
    "DdpgMlpQNet",
    "DecisionTransformer",
    "DreamerActor",
    "DTActor",
    "DuelingCnnDQNet",
    "MLP",
    "MultiAgentConvNet",
    "MultiAgentMLP",
    "MultiAgentNetBase",
    "NoisyLazyLinear",
    "NoisyLinear",
    "ObsDecoder",
    "ObsEncoder",
    "OnlineDTActor",
    "QMixer",
    "reset_noise",
    "RSSMPosterior",
    "RSSMPrior",
    "RSSMRollout",
    "Squeeze2dLayer",
    "SqueezeLayer",
    "VDNMixer",
    "Actor",
    "ActorCriticOperator",
    "ActorCriticWrapper",
    "ActorValueOperator",
    "AdditiveGaussianModule",
    "AdditiveGaussianWrapper",
    "DecisionTransformerInferenceWrapper",
    "DistributionalQValueActor",
    "DistributionalQValueHook",
    "DistributionalQValueModule",
    "EGreedyModule",
    "EGreedyWrapper",
    "GRU",
    "GRUCell",
    "GRUModule",
    "LMHeadActorValueOperator",
    "LSTM",
    "LSTMCell",
    "LSTMModule",
    "MultiStepActorWrapper",
    "OrnsteinUhlenbeckProcessModule",
    "OrnsteinUhlenbeckProcessWrapper",
    "ProbabilisticActor",
    "QValueActor",
    "QValueHook",
    "QValueModule",
    "recurrent_mode",
    "SafeModule",
    "SafeProbabilisticModule",
    "SafeProbabilisticTensorDictSequential",
    "SafeSequential",
    "set_recurrent_mode",
    "TanhModule",
    "ValueOperator",
    "VmapModule",
    "WorldModelWrapper",
    "get_primers_from_module",
    "CEMPlanner",
    "MPCPlannerBase",
    "MPPIPlanner",
]
