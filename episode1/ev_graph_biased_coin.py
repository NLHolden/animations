
from manim import *
import numpy as np

class EvGraph(Scene):
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
    
    def get_mean_profit(self, trials : int, bias : float, sims : int = 1000) -> list[float]:
        intermediate_res = np.zeros(trials)

        for _ in range(sims):    
            pnls = self.simulate_pnl(trials, bias)[0][1:]

            pnls = np.array(pnls) / np.arange(1, trials + 1)

            intermediate_res += pnls
                                                
        return intermediate_res / sims

    def approximate_loss_probability(self, trials : int, bias : float, sims : int = 10000) -> list[int, float]:
        intermediate_results = np.array([0 for _ in range(trials + 1)])

        for _ in range(sims):
            pnl = self.simulate_pnl(trials, bias)[0]

            neg_pnl = np.array(pnl) < 0
            
            intermediate_results += neg_pnl

        return [count / sims for count in intermediate_results]

    def construct(self):
        bias = 0.51
        trials = 100
        
        profit_ev = self.get_mean_profit(trials, bias)

        axes = Axes(x_range=[0, trials, 10],
                    y_range=[-0.1, 1.1, 0.1],
                    axis_config={"include_tip": False},
                    x_axis_config={"numbers_to_include": list(np.arange(0, trials+1, 10))},
                    y_axis_config={"numbers_to_include": list(np.arange(0, 1.1, 0.2))}).to_edge(DOWN)

        labels = axes.get_axis_labels(x_label=Text(r"Ρίψη"), y_label=Text(r"Μέσο Κέρδος €"))
        self.play(Create(axes), Write(labels))
        
        benchmark_ev = [axes.c2p(x, 10 * (2 * bias - 1)) for x in range(0, trials + 1, 5)]
        
        legend_green = Line(ORIGIN, RIGHT * 0.5, color=GREEN)
        legend_green_label = Text("Θεωρητικό Μέσο Κέρδος ανά Ρίψη", font_size=24).next_to(legend_green, RIGHT, buff=0.2)

        legend_blue = Line(ORIGIN, RIGHT * 0.5, color=BLUE)
        legend_blue_label = Text("Μέσο Κέρδος Προσομοίωσης", font_size=24).next_to(legend_blue, RIGHT, buff=0.2)

        legend_group = VGroup(
            VGroup(legend_green, legend_green_label),
            VGroup(legend_blue, legend_blue_label)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR)

        self.play(FadeIn(legend_group))

        ev_graph = VMobject(color=GREEN)
        
        ev_graph.set_points_as_corners([benchmark_ev[0]])

        self.add(ev_graph)
        
        for i in range(1, len(benchmark_ev)):
            new_p = Line(benchmark_ev[i-1], benchmark_ev[i], color=GREEN)
            
            self.play(Create(new_p), run_time=0.03)

            ev_graph.add_points_as_corners([benchmark_ev[i]])



        ev_points = [axes.c2p(x, y) for x, y in enumerate(profit_ev)]
        
        prob_graph = VMobject(color=BLUE)

        prob_graph.set_points_as_corners([ev_points[0]])

        self.add(prob_graph)

        for i in range(1, len(ev_points)):
            new_p = Line(ev_points[i - 1], ev_points[i], color=BLUE)

            self.play(Create(new_p), run_time=0.03)
            
            prob_graph.add_points_as_corners([ev_points[i]])

        self.wait() 
