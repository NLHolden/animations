from manim import *
import numpy as np

class SimpleGraph(Scene):
    def biased_flip(self, bias : float) -> str:
        return 'H' if np.random.random() < bias else 'T'

    def simulate_pnl(self, simulations: int, bias: float) -> tuple[list[float], list[float]]:
        player1_results = [0]
        player2_results = [0]

        for _ in range(simulations):
            result = self.biased_flip(bias)

            player1_change = 10 if result == 'H' else -10
            player2_change = -player1_change  # symmetrical

            player1_results.append(player1_results[-1] + player1_change)
            player2_results.append(player2_results[-1] + player2_change)

        return player1_results, player2_results

    def approximate_loss_probability(self, trials : int, bias : float, sims : int = 10000) -> list[int, float]:
        intermediate_results = np.array([0 for _ in range(trials + 1)])

        for _ in range(sims):
            pnl = self.simulate_pnl(trials, bias)[0]

            neg_pnl = np.array(pnl) < 0
            
            intermediate_results += neg_pnl

        return [count / sims for count in intermediate_results]

    def construct(self):
        bias = 0.51
        trials = 1000
        
        loss_prob = self.approximate_loss_probability(trials, bias)[1:]

        axes = Axes(x_range=[1, trials, 100],
                    y_range=[-0.1, 1.1, 0.1],
                    axis_config={"include_tip": False},
                    x_axis_config={"numbers_to_include": list(np.arange(0, trials+1, 100))},
                    y_axis_config={"numbers_to_include": list(np.arange(0, 1.1, 0.2))}).to_edge(DOWN)

        labels = axes.get_axis_labels(x_label=Text(r"Ρίψη"), y_label=Text(r"Πιθανότητα Κέρδους"))
        self.play(Create(axes), Write(labels))

        prob_points = [axes.c2p(x, y) for x, y in enumerate(loss_prob)]

        prob_graph = VMobject(color=BLUE)

        prob_graph.set_points_as_corners([prob_points[0]])

        self.add(prob_graph)

        for i in range(10, len(prob_points), 10):
            new_p = Line(prob_points[i - 10], prob_points[i], color=BLUE)

            self.play(Create(new_p), run_time=0.03)
            
            prob_graph.add_points_as_corners([prob_points[i]])

        self.wait() 
