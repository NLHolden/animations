from manim import *

class PnlGraphBiasedCoin(Scene):
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

    def construct(self):
        bias = 0.51
        simulations = 100
        player1_pnl, player2_pnl = self.simulate_pnl(simulations, bias)
        
        axes = Axes(
                x_range=[0, simulations, 10],
                y_range=[
                    min(min(player1_pnl), min(player2_pnl)) - 10,
                    max(max(player1_pnl), max(player2_pnl)) + 10, 20
                ],
                axis_config={"include_tip": False},
                x_axis_config={"numbers_to_include": list(range(0, simulations+1, 20))},
                y_axis_config={"numbers_to_include": list(range(int(min(player1_pnl + player2_pnl)) - 10, int(max(player1_pnl + player2_pnl)) + 20, 20))}
        ).to_edge(DOWN)

        labels = axes.get_axis_labels(x_label=Text(r"Ρίψη"), y_label=Text(r"Κέρδος"))
        self.play(Create(axes), Write(labels))

        # Dots and lines
        player1_points = [axes.c2p(x, y) for x, y in enumerate(player1_pnl)]
        player2_points = [axes.c2p(x, y) for x, y in enumerate(player2_pnl)]

        player1_graph = VMobject(color=GREEN)
        player2_graph = VMobject(color=RED)

        player1_graph.set_points_as_corners([player1_points[0]])
        player2_graph.set_points_as_corners([player2_points[0]])

        self.add(player1_graph, player2_graph)

        # Animate drawing point-by-point
        for i in range(1, len(player1_points)):
            new_p1 = Line(player1_points[i - 1], player1_points[i], color=GREEN)
            new_p2 = Line(player2_points[i - 1], player2_points[i], color=RED)

            self.play(Create(new_p1), Create(new_p2), run_time=0.07)
            player1_graph.add_points_as_corners([player1_points[i]])
            player2_graph.add_points_as_corners([player2_points[i]])

        self.wait() 
