
from manim import *

class ExpectedValueBiasedCoin(Scene):
    def construct(self):
        title = Text("Αναμενόμενο Κέρδος Νομίσματος - 100 Επαναλήψεις")
        title.scale_to_fit_width(config.frame_width * 0.9) 
        title.to_edge(UP)
        self.play(Write(title))

        # Coin probabilities
        prob_heads = Text("51 στις 100 έρχεται κορώνα", font_size=25)
        prob_tails = Text("49 στις 100 έρχεται γράμματα", font_size=25)

        probs = VGroup(prob_heads, prob_tails).arrange(DOWN, aligned_edge=LEFT)
        probs.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(prob_heads, shift=LEFT), FadeIn(prob_tails, shift=RIGHT))

    # Payoffs
        payoff_heads = Text("Αν έρθει Κορώνα +10$", font_size=25)
        payoff_tails = Text("Αν έρθει Γράμματα -10$", font_size=25)

        payoffs = VGroup(payoff_heads, payoff_tails).arrange(DOWN)
        payoffs.next_to(probs, DOWN, buff=0.7)
        self.play(Write(payoff_heads), Write(payoff_tails))
        
    # Expected value formula
        ev_formula = MathTex("\\text{MK} = 51 * (+10) + 49 * (-10)")
        ev_formula_result = MathTex("\\text{MK} = 510 - 490 = 20")

        ev_group = VGroup(ev_formula, ev_formula_result).arrange(DOWN)
        ev_group.next_to(payoffs, DOWN, buff=0.8)

        self.play(Write(ev_formula))
        self.wait(1)
        self.play(TransformMatchingTex(ev_formula.copy(), ev_formula_result))
        self.wait(1)
        
        conclusion = Text("Μέσο Κέρδος ανά Ρίψη = 0.2$", color=GREEN)
        conclusion.next_to(ev_group, DOWN, buff=1)
        self.play(Write(conclusion))
        self.wait(2)
