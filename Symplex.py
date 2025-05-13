from manim import *


#####################################
#    @author: Cavallero Lorenzo     #
#####################################


config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30

class Simplex(Scene):
    def construct(self):
        equations = [
            "x_1  & \;-\;    2x_2 &\; \ge \; & 3",
            "2x_1 &\;+\;     3x_2 &\; \le \; & 8",
            "&\;\;\;\;\;\;\;  x_2 &\; \le \; & 2",
            "&\;\;\;\;   x_1, x_2 &\; \ge \; & 0"
        ]
        title    = Tex(r"Risoluzione di programmi lineari")
        subtitle = Tex(r"Metodo grafico").next_to(title, DOWN)

        plane = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            background_line_style={"stroke_color": "#888888", "stroke_width": 1}
        ).to_edge(RIGHT)
        plane.add_coordinates()

        # Non conosco bene latex quindi potrebbe essere un obrobrio
        problem_label = Tex(fr"""\[
            \small
            \begin{{alignedat}}{3}
            \max\; z &&\;\;=\;   2x_1 &\;+\;\;\;      x_2 \\[6pt]
            \text{{soggetto a}}\quad
             & & {equations[0]} \\[6pt]
             & & {equations[1]} \\[6pt]
             & & {equations[2]} \\[6pt]
             & & {equations[3]} \\[6pt]
            \end{{alignedat}}
            \]""", font_size=40) \
            .to_edge(LEFT)

        # Vertici della zona ammissibile
        pts = [(0, 2), (1, 2), (4, 0),(3, 0), (0, 1.5)]

        # Rettangoli che racchiudono l'equazionoe della retta che sta venendo disegnata
        highlight_rects = [
            Rectangle(
                width  = 3,
                height = 0.6,
                color  = BLUE
            ).shift(problem_label.get_center() + 0.85 * UP   + 1.4 * RIGHT),
            Rectangle(
                width  = 3,
                height = 0.6,
                color  = GREEN
            ).shift(problem_label.get_center() + 0.05 * UP   + 1.4 * RIGHT),
            Rectangle(
                width  = 1.5,
                height = 0.6,
                color  = RED
            ).shift(problem_label.get_center() + 0.80 * DOWN + 2.1 * RIGHT),

            Rectangle(
                width  = 2.2,
                height = 0.6,
                color  = ORANGE
            ).shift(problem_label.get_center() + 1.70 * UP   + 1.1 * RIGHT)
        ]

        lines = [
            plane.plot(
                lambda x: (3 - x) / 2,
                x_range=[-1, 6],
                color=BLUE, stroke_width=2
            ),
            plane.plot(
                lambda x: (8 - 2 * x) / 3,
                x_range=[-1, 6],
                color=GREEN, stroke_width=2
            ),
            plane.plot(
                lambda x: 2,
                x_range=[-1, 6],
                color=RED, stroke_width=2
            )
        ]

        # zone ammissibili
        zones_pts = [
            [(5, 0), (3, 0), (0, 1.5), (0, 5), (5, 5)],
            [(4, 0), (3, 0), (0, 1.5), (0, 2.6666666)],
            [(4, 0), (3, 0), (0, 1.5), (0, 2), (1, 2)]
        ]
        zones = [
            Polygon(
                *[plane.c2p(x, y) for x, y in zones_pts[0]],
                color=BLUE,
                fill_opacity=0.5
            ),
            Polygon(
                *[plane.c2p(x, y) for x, y in zones_pts[1]],
                color=BLUE,
                fill_opacity=0.5
            ),
            Polygon(
                *[plane.c2p(x, y) for x, y in zones_pts[2]],
                color=BLUE,
                fill_opacity=0.5
            )
        ]

        zone_labels = [
            Tex(fr"""\[ 
                \begin{{alignedat}}{3}
                    {equations[0]}
                \end{{alignedat}} 
            \]""").move_to(zones[0].get_center()),

            Tex(fr"""\[ 
                \begin{{alignedat}}{3}
                    {equations[1]}
                \end{{alignedat}} 
            \]""").move_to(zones[1].get_center()),

            Tex(fr"""\[ 
                \begin{{alignedat}}{3}
                    {equations[2]}
                \end{{alignedat}} 
            \]""").move_to(zones[2].get_center())
        ]


        # Vettore di crescita
        c_vec  = np.array([1, 0.5])
        c_unit = c_vec / np.linalg.norm(c_vec)
        arr = Arrow(
            plane.c2p(0, 0),
            plane.c2p(2, 1),
            color=ORANGE, buff=0, stroke_width=2, tip_length=0.2
        )
        c_label = Tex(r"c").next_to(arr, UP)

        # Retta perpendicolare al vettore c
        perp_line = plane.plot(
            lambda x: -2 * x,
            x_range=[-1, 6], color=PURPLE, stroke_width=2
        )

        # Cerchio dell'ottimo
        last_point = plane.c2p(4, 0)
        solution_circle = Circle(
            radius=0.2,
            color=YELLOW,
            fill_opacity=0.5
        ).move_to(last_point)

        ########################
        # Animation Start      #
        ########################


        # Genera titolo e sottotitolo e dopo un secondo li toglie
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(1)
        self.play(Unwrite(title), Unwrite(subtitle))
        self.wait(0.2)

        # Genera Piano e Problema
        self.play(Create(plane))
        self.wait(0.5)
        self.play(Write(problem_label))


        # ogni iterazione disegna la retta descritta dall'equazione associata (che racchiude nel rettangolo corrispondente)
        # per poi modificare la zona ammissibile.
        prev_zone = None
        for idx, (line, rect, zone, zone_label) in enumerate(zip(lines, highlight_rects, zones, zone_labels)):
            self.wait(1)
            self.play(
                Create(line),
                Create(rect)
            )
            self.wait(0.3)

            if idx == 0:
                self.play(
                    Create(zone),
                    run_time=1
                )
            else:
                self.play(
                    ReplacementTransform(prev_zone, zone),
                    run_time=1
                )

            self.play(
                Write(zone_label),
                run_time=1
            )
            self.wait(1)

            self.play(
                Uncreate(rect),
                Unwrite(zone_label)
            )
            prev_zone = zone


        # Genera il vettore di crescita e gli elementi associati
        self.play(
            GrowArrow(arr),
            Write(c_label),
            Create(highlight_rects[3])
        )
        self.wait(1)
        self.play(Uncreate(highlight_rects[3]))
        self.wait(0.5)

        # Genera la retta perpendicolare al vettore di crescita
        self.play(Create(perp_line))

        # Disegna i vertici della zona ammissibile
        dots = VGroup(*[
            Dot(
                plane.c2p(x, y),
                color=YELLOW,
                radius=0.05
            )
            for x, y in pts
        ])

        self.add(dots)

        self.wait(0.5)


        # Muove la perpenicolare nella direzione del vettore c e la ferma ogni vertice.
        projections = [np.dot(np.array(p), c_unit) for p in pts]
        sorted_proj = sorted(projections)
        current_shift = np.array([0.0, 0.0, 0.0])
        for t in sorted_proj:
            shift = np.append(c_unit * t, 0) - current_shift
            self.play(perp_line.animate.shift(plane.c2p(*shift[:2]) - plane.c2p(0, 0)), run_time=1.5)
            current_shift += shift
            self.wait(0.2)

        self.wait(1)

        # Cerchia il vertice ottimo
        self.play(Create(solution_circle))
        self.wait(2)
