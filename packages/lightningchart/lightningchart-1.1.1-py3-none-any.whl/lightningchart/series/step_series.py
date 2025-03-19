from __future__ import annotations

from lightningchart.charts import Chart
from lightningchart.ui.axis import Axis
from lightningchart.series import (
    Series2D,
    SeriesWithAddDataPoints,
    SeriesWithAddDataXY,
    SeriesWith2DLines,
    SeriesWithIndividualPoint,
    Series,
    PointLineAreaSeries,
    SeriesWith2DPoints,
)


class StepSeries(
    Series2D,
    SeriesWithAddDataPoints,
    SeriesWithAddDataXY,
    SeriesWith2DLines,
    SeriesWith2DPoints,
    SeriesWithIndividualPoint,
    PointLineAreaSeries,
):
    """Series for visualizing 2D steps."""

    def __init__(
        self,
        chart: Chart,
        step_mode: str = 'middle',
        data_pattern: str = None,
        colors: bool = False,
        lookup_values: bool = False,
        ids: bool = False,
        sizes: bool = False,
        rotations: bool = False,
        auto_sorting_enabled: bool = False,
        x_axis: Axis = None,
        y_axis: Axis = None,
    ):
        Series.__init__(self, chart)
        self.instance.send(
            self.id,
            'stepSeries',
            {
                'chart': self.chart.id,
                'stepMode': step_mode,
                'dataPattern': data_pattern,
                'colors': colors,
                'lookupValues': lookup_values,
                'ids': ids,
                'sizes': sizes,
                'rotations': rotations,
                'autoSortingEnabled': auto_sorting_enabled,
                'xAxis': x_axis,
                'yAxis': y_axis,
            },
        )
