from __future__ import annotations

import lightningchart
from lightningchart.charts import Chart
from lightningchart import Themes
from lightningchart.series import Series2D, ComponentWithPaletteColoring
from lightningchart.utils import convert_to_dict


class PolarAreaSeries(Series2D, ComponentWithPaletteColoring):
    """Series type for visualizing polar area data."""

    def __init__(
        self,
        chart: Chart,
        theme: Themes = Themes.Light,
        name: str = None,
    ):
        Series2D.__init__(self, chart)
        self.instance.send(
            self.id,
            'addAreaSeries',
            {
                'chart': self.chart.id,
                'theme': theme.value,
                'name': name,
            },
        )

    def set_data(self, data: list[dict]):
        """Set the data for the series.

        Args:
            data (list[dict]): A list of dictionaries, each containing:
                - 'angle' (float): The angle in degrees.
                - 'amplitude' (float): The amplitude at that angle.

        Example:
            series.set_data([
                {'angle': 0, 'amplitude': 5},
                {'angle': 90, 'amplitude': 10},
                {'angle': 180, 'amplitude': 7.5},
                {'angle': 270, 'amplitude': 3},
            ])

        Returns:
            The instance of the class for fluent interface.
        """
        data = convert_to_dict(data)

        self.instance.send(self.id, 'setData', {'data': data})
        return self

    def set_color(self, color: lightningchart.Color):
        """Set a color of the series.

        Args:
            color (Color): Color of the band.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSolidFillStyle', {'color': color.get_hex()})
        return self

    def set_stroke(self, thickness: int | float, color: lightningchart.Color):
        """Set Stroke style of the series.

        Args:
            thickness (int | float): Thickness of the stroke.
            color (Color): Color of the stroke.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(
            self.id,
            'setStrokeStyle',
            {'thickness': thickness, 'color': color.get_hex()},
        )
        return self

    def set_connect_data_automatically_enabled(self, enabled: bool):
        """Set automatic connection of first and last data points enabled or not.

        Args:
            enabled: Boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(
            self.id, 'setConnectDataAutomaticallyEnabled', {'enabled': enabled}
        )
        return self
