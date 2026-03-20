import tkinter as tk


class BalanceChart(tk.Canvas):
    """Smooth line chart showing account balance over time.

    - Y-axis: amount scale on the left (€), 4 evenly spaced gridlines
    - X-axis: date labels (DD/MM) at the bottom, thinned automatically
    - Curve: single thin line, no filled area underneath
    - A dot marks the last (most recent) balance point
    """

    LINE_COLOR  = "#7c3aed"   # curve and dot colour
    GRID_COLOR  = "#2a2a3e"   # faint horizontal gridlines
    LABEL_COLOR = "#6b7280"   # muted labels

    def __init__(self, master, months: list, values: list, **kwargs):
        """Create the chart canvas.

        Args:
            master: Parent tkinter widget.
            months: Date label strings for the x-axis (e.g. '15/03').
                    Must have the same length as values.
            values: Cumulative balance floats, one per label.
                    Requires at least 2 points to render.
        """
        self.months = months
        self.values = values
        super().__init__(master, bg="#1e1e2e", highlightthickness=0, **kwargs)
        self.bind("<Configure>", lambda e: self._draw())

    # ── Drawing ───────────────────────────────────────────────────────────── #

    def _draw(self):
        """Redraw the entire chart from scratch."""
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()

        if w < 10 or h < 10:
            return
        if len(self.values) < 2:
            return

        # Margins: left is wider to fit the € scale labels
        pad_left = 64
        pad_right = 20
        pad_top   = 16
        pad_bot   = 36

        n    = len(self.values)
        vmin = min(self.values)
        vmax = max(self.values)

        # Expand range slightly so curve never touches top/bottom edges
        span = vmax - vmin if vmax != vmin else 1
        vmin -= span * 0.08
        vmax += span * 0.08

        def to_x(i):
            """Map point index → horizontal pixel."""
            return pad_left + i * (w - pad_left - pad_right) / (n - 1)

        def to_y(v):
            """Map balance value → vertical pixel (top = high value)."""
            return pad_top + (1 - (v - vmin) / (vmax - vmin)) * (h - pad_top - pad_bot)

        # ── Horizontal gridlines + Y-axis labels ──────────────────────────── #

        n_grid = 4   # number of horizontal gridlines (including top and bottom)
        for i in range(n_grid + 1):
            ratio = i / n_grid
            grid_v = vmax - ratio * (vmax - vmin)
            grid_y = to_y(grid_v)

            # Faint gridline across the chart area
            self.create_line(pad_left, grid_y, w - pad_right, grid_y,
                             fill=self.GRID_COLOR, width=1)

            # € amount label on the left
            label = self._format_amount(grid_v)
            self.create_text(pad_left - 6, grid_y,
                             text=label, anchor="e",
                             fill=self.LABEL_COLOR,
                             font=("Helvetica", 9))

        # ── Curve ─────────────────────────────────────────────────────────── #

        pts = [(to_x(i), to_y(v)) for i, v in enumerate(self.values)]

        flat = []
        for x, y in pts:
            flat.extend([x, y])

        self.create_line(flat, fill=self.LINE_COLOR, width=1,
                         smooth=True, splinesteps=64)

        # Dot on the last point
        lx, ly = pts[-1]
        r = 4
        self.create_oval(lx - r, ly - r, lx + r, ly + r,
                         fill=self.LINE_COLOR, outline="white", width=1)

        # ── X-axis date labels ─────────────────────────────────────────────── #

        visible = self._pick_labels(n)
        for i, (label, (x, _)) in enumerate(zip(self.months, pts)):
            # Skip the last point — it is always today, adding no useful context
            if i == n - 1:
                continue
            if i not in visible:
                continue
            self.create_text(x, h - pad_bot + 14,
                             text=label, anchor="center",
                             fill=self.LABEL_COLOR, font=("Helvetica", 9))

    # ── Helpers ───────────────────────────────────────────────────────────── #

    @staticmethod
    def _format_amount(value: float) -> str:
        """Format a euro amount compactly for the Y-axis scale.

        Examples:
            1325.0   → '1 325 €'
            -50.0    → '-50 €'
            12500.0  → '12 500 €'
        """
        # Use space as thousands separator for readability
        return f"{value:,.0f} €".replace(",", " ")

    @staticmethod
    def _pick_labels(n: int) -> set:
        """Return the indices that should show an x-axis label.

        Always includes the first and last point. Thins the middle
        labels so they don't overlap when there are many data points.

        Args:
            n: Total number of data points.
        """
        if n <= 6:
            return set(range(n))

        # ~4 evenly spaced labels plus the last one
        step   = max(1, (n - 1) // 4)
        result = set(range(0, n, step))
        result.add(n - 1)
        return result