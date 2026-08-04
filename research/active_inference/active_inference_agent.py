import numpy as np
from itertools import product


class ActiveInferenceAgentDeep:
    def __init__(self, H=4):
        self.H = H

        # A[o,s] = P(o|s)
        self.A = np.array([
            [0.8, 0.2],
            [0.2, 0.8]
        ])

        # B[s_futuro,s_pasado,accion]
        self.B = np.zeros((2, 2, 2))

        # Acción 0
        self.B[:, :, 0] = np.array([
            [0.7, 0.0],
            [0.3, 1.0]
        ])

        # Acción 1
        self.B[:, :, 1] = np.array([
            [0.9, 0.8],
            [0.1, 0.2]
        ])

        # Preferencias C[o]
        self.C = np.array([0.95, 0.05])

        # q(s)
        self.belief = np.array([0.5, 0.5])

        self._validate_matrices()


    def _validate_matrices(self):
        assert np.all(self.A >= 0)
        assert np.all(self.B >= 0)
        assert np.all(self.C >= 0)

        assert np.allclose(
            self.A.sum(axis=0),
            1.0
        ), "A no es columna-estocástica"

        for a in range(self.B.shape[2]):
            assert np.allclose(
                self.B[:, :, a].sum(axis=0),
                1.0
            ), f"B[{a}] no es columna-estocástica"

        assert np.isclose(
            self.C.sum(),
            1.0
        ), "C inválida"


    def perceive(self, obs_idx):
        likelihood = self.A[obs_idx, :]

        posterior = likelihood * self.belief

        norm = posterior.sum()

        if norm > 0:
            self.belief = posterior / norm

        return self.belief


    def _step_G(self, belief, action):

        # Predicción estado futuro
        next_belief = self.B[:, :, action] @ belief

        # Predicción observación
        expected_obs = self.A @ next_belief


        # Riesgo KL(expected_obs || C)
        risk = np.sum(
            expected_obs *
            (
                np.log(expected_obs + 1e-12)
                -
                np.log(self.C + 1e-12)
            )
        )


        # Ambigüedad
        entropy_state = -np.sum(
            self.A *
            np.log(self.A + 1e-12),
            axis=0
        )

        ambiguity = np.sum(
            next_belief * entropy_state
        )


        return next_belief, risk + ambiguity



    def evaluate_policy(self, policy, best_G):

        belief = self.belief.copy()

        total_G = 0.0

        for action in policy:

            belief, step_G = self._step_G(
                belief,
                action
            )

            total_G += step_G


            # Branch and Bound
            if total_G >= best_G:
                return np.inf


        return total_G



    def act(self):

        best_policy = None
        best_G = np.inf


        for policy in product(
            range(self.B.shape[2]),
            repeat=self.H
        ):

            G = self.evaluate_policy(
                policy,
                best_G
            )

            if G < best_G:
                best_G = G
                best_policy = policy


        if best_policy is None:
            raise RuntimeError(
                "No existe política válida"
            )


        return (
            best_policy[0],
            best_G,
            best_policy
        )



if __name__ == "__main__":

    agent = ActiveInferenceAgentDeep(H=4)

    action, G, policy = agent.act()

    print("\n=== ACTIVE INFERENCE TEST ===")
    print("Belief inicial:", agent.belief)
    print("Política óptima:", policy)
    print("G mínimo:", round(G,6))
    print("Acción ejecutada:", action)
