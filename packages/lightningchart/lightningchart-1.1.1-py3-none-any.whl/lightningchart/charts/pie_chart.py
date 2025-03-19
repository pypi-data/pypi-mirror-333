from __future__ import annotations

import lightningchart
from lightningchart import conf, Themes
from lightningchart.charts import (
    GeneralMethods,
    TitleMethods,
    ChartWithLUT,
    ChartWithLabelStyling,
    Chart,
)
from lightningchart.instance import Instance
from lightningchart.utils import convert_to_dict


class PieChart(GeneralMethods, TitleMethods, ChartWithLUT, ChartWithLabelStyling):
    """Visualizes proportions and percentages between categories, by dividing a circle into proportional segments."""

    def __init__(
        self,
        data: list[dict[str, int | float]] = None,
        inner_radius: int | float = None,
        title: str = None,
        theme: Themes = Themes.Light,
        labels_inside_slices: bool = False,
        license: str = None,
        license_information: str = None,
    ):
        """Visualizes proportions and percentages between categories, by dividing a circle into proportional segments.

        Args:
            data (list[dict[str, int | float]]): List of {name, value} slices.
            inner_radius (int | float): Inner radius as a percentage of outer radius [0, 100].
            title (str): Title of the chart.
            theme (Themes): Theme of the chart.
            labels_inside_slices (bool): If true, the labels are inside pie slices. If false, the labels are on the
                sides of the slices.
            license (str): License key.
        """
        instance = Instance()
        Chart.__init__(self, instance)
        self.instance.send(
            self.id,
            'pieChart',
            {
                'theme': theme.value,
                'labelsInsideSlices': labels_inside_slices,
                'license': license or conf.LICENSE_KEY,
                'licenseInformation': license_information or conf.LICENSE_INFORMATION,
            },
        )
        if title:
            self.set_title(title)
        if inner_radius:
            self.set_inner_radius(inner_radius)
        if data:
            self.add_slices(data)

    def add_slice(self, name: str, value: int | float):
        """Add new Slice to the Pie Chart.

        Args:
            name (str): Initial name for Slice as string.
            value (int | float): Initial value for Slice as number.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'addSlice', {'name': name, 'value': value})
        return self

    def add_slices(self, slices: list[dict[str, int | float]]):
        """This method is used for the adding multiple slices in the funnel chart.

        Args:
            slices (list[dict[int | float, int | float]]): List of slices {name, value}.

        Returns:
            The instance of the class for fluent interface.
        """
        slices = convert_to_dict(slices)

        self.instance.send(self.id, 'addSlices', {'slices': slices})
        return self

    def set_inner_radius(self, radius: int | float):
        """Set inner radius of Pie Chart.
        This method can be used to style the Pie Chart as a "Donut Chart", with the center being hollow.

        Args:
            radius (int | float): Inner radius as a percentage of outer radius [0, 100]

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setInnerRadius', {'radius': radius})
        return self

    def set_slice_stroke(self, thickness: int | float, color: lightningchart.Color):
        """Set stroke style of Pie Slices border.

        Args:
            thickness (int | float): Thickness of the slice border.
            color (Color): Color of the slice border.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(
            self.id,
            'setSliceStrokeStyle',
            {'thickness': thickness, 'color': color.get_hex()},
        )
        return self

    def set_multiple_slice_explosion(self, enabled: bool):
        """Set if it is allowed for multiple Slices to be 'exploded' at the same time or not.
        When a Slice is exploded, it is drawn differently from non-exploded state,
        usually slightly "pushed away" from the center of Pie Chart.

        Args:
            enabled (bool): Is behavior allowed as boolean flag.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setMultipleSliceExplosion', {'enabled': enabled})
        return self

    def set_slice_explosion_offset(self, offset: int | float):
        """Set offset of exploded Slices in pixels.

        Args:
            offset (int | float): Offset of exploded Slices in pixels

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setSliceExplosionOffset', {'offset': offset})
        return self

    def set_label_connector_end_length(self, length: int | float):
        """Set horizontal length of connector line before connecting to label.

        Args:
            length (int | float): Length of the connector line before connecting to label.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLabelConnectorEndLength', {'length': length})
        return self

    def set_label_connector_gap_start(self, gap: int | float):
        """Set gap between slice and connector line start.

        Args:
            gap (int | float): Gap as pixels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLabelConnectorGapStart', {'gap': gap})
        return self

    def set_label_slice_offset(self, offset: int | float):
        """Set distance between slice and label (includes explosion offset), this points to reference position of label,
        so not necessarily the nearest corner.

        Args:
            offset (int | float): Length as pixels.

        Returns:
            The instance of the class for fluent interface.
        """
        self.instance.send(self.id, 'setLabelSliceOffset', {'offset': offset})
        return self


class PieChartDashboard(PieChart):
    def __init__(
        self,
        instance: Instance,
        dashboard_id: str,
        column: int,
        row: int,
        colspan: int,
        rowspan: int,
    ):
        Chart.__init__(self, instance)
        self.instance.send(
            self.id,
            'createPieChart',
            {
                'db': dashboard_id,
                'column': column,
                'row': row,
                'colspan': colspan,
                'rowspan': rowspan,
            },
        )
