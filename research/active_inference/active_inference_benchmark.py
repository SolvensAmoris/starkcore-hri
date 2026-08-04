import numpy as np
from itertools import product


class ActiveInferenceAgent:
    def __init__(self, H=3):

        self.H = H

        # Modelo del agente
        self.A = np.array([
            [0.8, 0.2],
            [0.2, 0.8]
        ])

        self.B = np.zeros((2,2,2))

        self.B[:,:,0] = np.array([
            [0.7,0.0],
            [0.3,1.0]
        ])

        self.B[:,:,1] = np.array([
            [0.9,0.8],
            [0.1,0.2]
        ])

        self.C = np.array([
            0.95,
            0.05
        ])

        self.belief = np.array([
            0.5,
            0.5
        ])


    def reset(self):
        self.belief = np.array([0.5,0.5])


    def perceive(self, obs):

        likelihood = self.A[obs,:]

        posterior = likelihood * self.belief

        norm = posterior.sum()

        if norm > 0:
            self.belief = posterior / norm


        # evitar certeza absoluta artificial
        eps = 1e-6

        self.belief = np.clip(
            self.belief,
            eps,
            1-eps
        )

        self.belief /= self.belief.sum()

        return self.belief



    def step_G(self, belief, action):

        next_belief = (
            self.B[:,:,action]
            @ belief
        )

        obs = self.A @ next_belief


        risk = np.sum(
            obs *
            (
                np.log(obs + 1e-12)
                -
                np.log(self.C + 1e-12)
            )
        )


        entropy = -np.sum(
            self.A *
            np.log(self.A + 1e-12),
            axis=0
        )


        ambiguity = np.sum(
            next_belief * entropy
        )


        return next_belief, risk + ambiguity



    def evaluate_policy(self, policy):

        belief = self.belief.copy()

        G = 0

        for action in policy:

            belief, step = self.step_G(
                belief,
                action
            )

            G += step

        return G



    def act(self):

        best_G = np.inf
        best_policy = None


        for policy in product(
            [0,1],
            repeat=self.H
        ):

            G = self.evaluate_policy(
                policy
            )

            if G < best_G:

                best_G = G
                best_policy = policy


        return best_policy[0], best_G



class Environment:

    def __init__(self):

        # Mundo ligeramente diferente al modelo
        self.A = np.array([
            [0.75,0.25],
            [0.25,0.75]
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



    def reset(self):

        self.state = 1



    def step(self,action):

        probs = self.B[:,self.state,action]


        self.state = np.random.choice(
            2,
            p=probs
        )


        obs = np.random.choice(
            2,
            p=self.A[:,self.state]
        )


        return obs,self.state




def run_agent(mode,episodes=1000):

    env = Environment()

    active = ActiveInferenceAgent()

    score = []

    for _ in range(episodes):

        env.reset()
        active.reset()

        preferred = 0


        for t in range(100):

            if mode=="active":

                action,_ = active.act()

            elif mode=="random":

                action=np.random.choice([0,1])

            elif mode=="fixed0":

                action=0


            obs,state = env.step(action)


            if mode=="active":
                active.perceive(obs)


            if state==0:
                preferred += 1


        score.append(
            preferred/100
        )


    return np.mean(score), np.std(score)



if __name__=="__main__":

    np.random.seed(42)


    print("=== BENCHMARK 1000 EPISODIOS ===")


    for mode in [
        "active",
        "random",
        "fixed0"
    ]:

        mean,std = run_agent(mode)

        print(
            f"{mode:8s} "
            f"media={mean:.4f} "
            f"std={std:.4f}"
        )
