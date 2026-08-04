import numpy as np
from itertools import product


class ActiveInferenceAgentDeep:
    def __init__(self, H=3):
        self.H = H

        # Modelo generativo del agente
        # A[o,s] = P(o|s)
        self.A = np.array([
            [0.8, 0.2],
            [0.2, 0.8]
        ])

        # B[s_futuro,s_pasado,accion]
        self.B = np.zeros((2, 2, 2))

        self.B[:, :, 0] = np.array([
            [0.7, 0.0],
            [0.3, 1.0]
        ])

        self.B[:, :, 1] = np.array([
            [0.9, 0.8],
            [0.1, 0.2]
        ])

        # Preferencia sobre observaciones
        self.C = np.array([0.95, 0.05])

        self.belief = np.array([0.5, 0.5])

        self._validate_matrices()


    def _validate_matrices(self):
        assert np.all(self.A >= 0)
        assert np.all(self.B >= 0)
        assert np.all(self.C >= 0)

        assert np.allclose(self.A.sum(axis=0), 1.0)

        for a in range(self.B.shape[2]):
            assert np.allclose(
                self.B[:, :, a].sum(axis=0),
                1.0
            )

        assert np.isclose(self.C.sum(), 1.0)


    def perceive(self, obs_idx):
        likelihood = self.A[obs_idx, :]

        posterior = likelihood * self.belief

        norm = posterior.sum()

        if norm > 0:
            self.belief = posterior / norm

        return self.belief


    def _step_G(self, belief, action):

        next_belief = self.B[:, :, action] @ belief

        expected_obs = self.A @ next_belief

        risk = np.sum(
            expected_obs *
            (
                np.log(expected_obs + 1e-12)
                -
                np.log(self.C + 1e-12)
            )
        )

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
            raise RuntimeError("No policy found")


        return best_policy[0], best_G, best_policy



class MinimalEnv:

    def __init__(self, init_state=1):

        # Física real ligeramente distinta
        self.A = np.array([
            [0.75, 0.25],
            [0.25, 0.75]
        ])

        self.B = np.zeros((2,2,2))

        self.B[:,:,0] = np.array([
            [0.65,0.05],
            [0.35,0.95]
        ])

        self.B[:,:,1] = np.array([
            [0.85,0.75],
            [0.15,0.25]
        ])

        self.state = init_state


    def step(self, action):

        probs = self.B[:, self.state, action]

        self.state = np.random.choice(
            2,
            p=probs
        )

        obs_probs = self.A[:, self.state]

        obs = np.random.choice(
            2,
            p=obs_probs
        )

        return obs, self.state



if __name__ == "__main__":

    np.random.seed(42)

    agent = ActiveInferenceAgentDeep(H=3)

    env = MinimalEnv(
        init_state=1
    )

    STEPS = 100

    preferred = 0
    actions = []
    G_history = []

    print("=== ACTIVE INFERENCE CLOSED LOOP ===")
    print(" t | a | obs | state | belief")

    for t in range(STEPS):

        action, G, policy = agent.act()

        G_history.append(G)

        obs, state = env.step(action)

        agent.perceive(obs)

        actions.append(action)

        if state == 0:
            preferred += 1


        if t < 15 or t % 20 == 0:
            print(
                f"{t:2d} | "
                f"{action} | "
                f"{obs} | "
                f"{state} | "
                f"{agent.belief.round(3)}"
            )


    print("\n=== METRICAS ===")
    print(
        "Tiempo en estado preferido:",
        round(preferred/STEPS,3)
    )

    print(
        "Acciones 1:",
        actions.count(1),
        "/",
        STEPS
    )

    print(
        "G inicial:",
        round(G_history[0],4)
    )

    print(
        "G final:",
        round(G_history[-1],4)
    )

    print(
        "G promedio:",
        round(np.mean(G_history),4)
    )

    print(
        "Belief final:",
        agent.belief.round(4)
    )
