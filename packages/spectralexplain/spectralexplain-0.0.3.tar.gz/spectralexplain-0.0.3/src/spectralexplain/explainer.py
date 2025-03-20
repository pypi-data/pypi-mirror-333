import spectralexplain as spex

class Explainer:
    def __init__(self, value_function, features, sample_budget=None, max_order=5, name=''):
        self.value_function = value_function
        self.name = name
        if type(features) == int:
            features = range(features)
        self.features = features
        self.num_features = len(self.features)
        self.max_order = max_order
        self.sample_budget = sample_budget
        self.sparsity_parameter = 8 if sample_budget is None else self.compute_sparsity_parameter()
        self.fourier_transform = self.compute_interaction_values()

    def compute_sparsity_parameter(self):
        signal, budget_thresholds = spex.sampling_strategy(lambda X: [0] * len(X), 3, 12, self.num_features,
                                                      sample_save_dir=None, t=self.max_order)
        self.budget_thresholds = budget_thresholds
        assert self.sample_budget >= budget_thresholds[3], \
            f"budget must be greater than {budget_thresholds[3]}, recommended at least {budget_thresholds[4]}"
        for key in budget_thresholds.keys():
            if self.sample_budget < budget_thresholds[key]:
                return key - 1
        else:
            return 12

    def compute_interaction_values(self):
        signal, _ = spex.sampling_strategy(self.value_function, 3, self.sparsity_parameter,
                                      self.num_features, sample_save_dir=self.name, t=self.max_order)
        return spex.support_recovery("soft", signal, self.sparsity_parameter, self.max_order)

    def interactions(self, index):
        assert index.lower() in ["fourier", "mobius", "fsii", "fbii", "stii", "sii", "bii"], \
            "index must belong to set {Fourier, Mobius, FSII, FBII, STII, SII, BII}"
        return spex.Interactions(self.fourier_transform, self.features, index, self.sample_budget)
