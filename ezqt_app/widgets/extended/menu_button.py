# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    Qt,
    QSize,
    Signal,
    QPropertyAnimation,
    QEasingCurve,
)
from PySide6.QtGui import (
    QIcon,
    QPixmap,
    QPainter,
    QColor,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QToolButton,
    QSizePolicy,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////


# ///////////////////////////////////////////////////////////////
# FONCTIONS UTILITAIRES
# ///////////////////////////////////////////////////////////////


def colorize_pixmap(pixmap, color="#FFFFFF", opacity=0.5):
    """Recolore un QPixmap avec la couleur et l'opacité données."""
    result = QPixmap(pixmap.size())
    result.fill(Qt.transparent)
    painter = QPainter(result)
    painter.setOpacity(opacity)
    painter.drawPixmap(0, 0, pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(result.rect(), QColor(color))
    painter.end()
    return result


def load_icon_from_source(source) -> QIcon:
    """
    Load icon from various sources (QIcon, path, URL, etc.).

    Parameters
    ----------
    source : QIcon or str
        Icon source (QIcon, path, resource, URL, or SVG).

    Returns
    -------
    QIcon
        Loaded icon or None if failed.
    """
    # ////// HANDLE NONE
    if source is None:
        return None
    # ////// HANDLE QICON
    elif isinstance(source, QIcon):
        return source
    # ////// HANDLE STRING (PATH, URL, SVG)
    elif isinstance(source, str):

        # ////// HANDLE URL
        if source.startswith("http://") or source.startswith("https://"):
            print(f"Loading icon from URL: {source}")
            try:
                import requests

                response = requests.get(source, timeout=5)
                response.raise_for_status()
                if "image" not in response.headers.get("Content-Type", ""):
                    raise ValueError("URL does not point to an image file.")
                image_data = response.content

                # ////// HANDLE SVG FROM URL
                if source.lower().endswith(".svg"):
                    from PySide6.QtSvg import QSvgRenderer
                    from PySide6.QtCore import QByteArray

                    renderer = QSvgRenderer(QByteArray(image_data))
                    pixmap = QPixmap(QSize(16, 16))
                    pixmap.fill(Qt.transparent)
                    painter = QPainter(pixmap)
                    renderer.render(painter)
                    painter.end()
                    return QIcon(pixmap)

                # ////// HANDLE RASTER IMAGE FROM URL
                else:
                    pixmap = QPixmap()
                    if not pixmap.loadFromData(image_data):
                        raise ValueError("Failed to load image data from URL.")
                    pixmap = colorize_pixmap(pixmap, "#FFFFFF", 0.5)
                    return QIcon(pixmap)
            except Exception as e:
                print(f"Failed to load icon from URL: {e}")
                return None

        # ////// HANDLE LOCAL SVG
        elif source.lower().endswith(".svg"):
            try:
                from PySide6.QtSvg import QSvgRenderer
                from PySide6.QtCore import QFile

                file = QFile(source)
                if not file.open(QFile.ReadOnly):
                    raise ValueError(f"Cannot open SVG file: {source}")
                svg_data = file.readAll()
                file.close()
                renderer = QSvgRenderer(svg_data)
                pixmap = QPixmap(QSize(16, 16))
                pixmap.fill(Qt.transparent)
                painter = QPainter(pixmap)
                renderer.render(painter)
                painter.end()
                return QIcon(pixmap)
            except Exception as e:
                print(f"Failed to load SVG icon: {e}")
                return None

        # ////// HANDLE LOCAL/RESOURCE RASTER IMAGE
        else:
            icon = QIcon(source)
            if icon.isNull():
                print(f"Invalid icon path: {source}")
                return None
            return icon

    # ////// HANDLE INVALID TYPE
    else:
        print(f"Invalid icon source type: {type(source)}")
        return None


# ///////////////////////////////////////////////////////////////
# CLASSES PRINCIPALES
# ///////////////////////////////////////////////////////////////


class MenuButton(QToolButton):
    """
    Enhanced menu button widget with automatic shrink/extended states.

    Features:
        - Automatic shrink/extended state management
        - Icon support from various sources (QIcon, path, URL, SVG)
        - Text visibility based on state (visible in extended, hidden in shrink)
        - Customizable shrink size and icon positioning
        - Property-based access to icon and text
        - Signals for state changes and interactions
        - Hover and click effects

    Parameters
    ----------
    parent : QWidget, optional
        The parent widget (default: None).
    icon : QIcon or str, optional
        The icon to display (QIcon, path, resource, URL, or SVG).
    text : str, optional
        The button text (default: "").
    icon_size : QSize or tuple, optional
        Size of the icon (default: QSize(20, 20)).
    shrink_size : int, optional
        Width when in shrink state (default: 60).
    spacing : int, optional
        Spacing between icon and text in pixels (default: 10).
    min_height : int, optional
        Minimum height of the button (default: None, auto-calculated).
    duration : int, optional
        Animation duration in milliseconds (default: 300).
    *args, **kwargs :
        Additional arguments passed to QToolButton.

    Properties
    ----------
    icon : QIcon
        Get or set the button icon.
    text : str
        Get or set the button text.
    icon_size : QSize
        Get or set the icon size.
    shrink_size : int
        Get or set the shrink width.
    is_extended : bool
        Get the current state (True for extended, False for shrink).
    spacing : int
        Get or set spacing between icon and text.
    min_height : int
        Get or set the minimum height of the button.
    duration : int
        Get or set the animation duration in milliseconds.

    Signals
    -------
    iconChanged(QIcon)
        Emitted when the icon changes.
    textChanged(str)
        Emitted when the text changes.
    stateChanged(bool)
        Emitted when the state changes (True for extended, False for shrink).
    """

    iconChanged = Signal(QIcon)
    textChanged = Signal(str)
    stateChanged = Signal(bool)  # True for extended, False for shrink

    # INITIALIZATION
    # ///////////////////////////////////////////////////////////////

    def __init__(
        self,
        parent=None,
        icon=None,
        text="",
        icon_size=QSize(20, 20),
        shrink_size=60,  # Will be overridden by Menu class
        spacing=10,
        min_height=None,
        duration=300,  # Animation duration in milliseconds
        *args,
        **kwargs,
    ) -> None:
        super().__init__(parent, *args, **kwargs)
        self.setProperty("type", "MenuButton")

        # ////// INITIALIZE VARIABLES
        self._icon_size = (
            QSize(*icon_size)
            if isinstance(icon_size, (tuple, list))
            else QSize(icon_size)
        )
        self._shrink_size = shrink_size
        self._spacing = spacing
        self._current_icon = None
        self._min_height = min_height
        self._animation_duration = duration
        self._is_extended = False  # Start in shrink state (menu is shrinked at startup)

        # ////// CALCULATE ICON POSITION
        # Calculate the ideal icon position so it stays fixed when menu expands
        # In shrink mode: icon should be centered in shrink_size
        # In extended mode: icon should stay at the same absolute position
        self._icon_x_position = (self._shrink_size - self._icon_size.width()) // 2
        
        # ////// ANIMATION SUPPORT
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(self._animation_duration)  # Configurable duration
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)  # Smooth easing

        # ////// SETUP UI COMPONENTS
        self.icon_label = QLabel()
        self.text_label = QLabel()

        # ////// CONFIGURE ICON LABEL
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("background-color: transparent;")

        # ////// CONFIGURE TEXT LABEL
        self.text_label.setAlignment(
            Qt.AlignLeft | Qt.AlignVCenter
        )
        self.text_label.setWordWrap(True)
        self.text_label.setStyleSheet("background-color: transparent;")

        # ////// SETUP LAYOUT
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # No margins, we'll handle positioning manually
        layout.setSpacing(0)  # No spacing, we'll handle it manually
        layout.setAlignment(Qt.AlignVCenter)  # Always center vertically
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)

        # ////// CONFIGURE SIZE POLICY
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # ////// SET INITIAL VALUES
        if icon:
            self.icon = icon
        if text:
            self.text = text

        # ////// SET INITIAL STATE
        self._update_state_display(animate=False)  # No animation on initial setup

    # PROPERTY FUNCTIONS
    # ///////////////////////////////////////////////////////////////

    @property
    def icon(self):
        """Get or set the button icon."""
        return self._current_icon

    @icon.setter
    def icon(self, value):
        """Set the button icon from various sources."""
        icon = load_icon_from_source(value)
        if icon:
            self._current_icon = icon
            self.icon_label.setPixmap(icon.pixmap(self._icon_size))
            self.icon_label.setFixedSize(self._icon_size)
            self.icon_label.setStyleSheet("background-color: transparent;")
            self.iconChanged.emit(icon)

    @property
    def text(self):
        """Get or set the button text."""
        return self.text_label.text()

    @text.setter
    def text(self, value):
        """Set the button text."""
        if value != self.text_label.text():
            self.text_label.setText(str(value))
            self.textChanged.emit(str(value))

    @property
    def icon_size(self):
        """Get or set the icon size."""
        return self._icon_size

    @icon_size.setter
    def icon_size(self, value):
        """Set the icon size."""
        self._icon_size = (
            QSize(*value) if isinstance(value, (tuple, list)) else QSize(value)
        )
        if self._current_icon:
            self.icon_label.setPixmap(self._current_icon.pixmap(self._icon_size))
            self.icon_label.setFixedSize(self._icon_size)

    @property
    def shrink_size(self):
        """Get or set the shrink width."""
        return self._shrink_size

    @shrink_size.setter
    def shrink_size(self, value):
        """Set the shrink width."""
        self._shrink_size = int(value)
        # Recalculate icon position
        self._icon_x_position = (self._shrink_size - self._icon_size.width()) // 2
        self._update_state_display(animate=False)  # No animation when shrink_size changes

    @property
    def is_extended(self):
        """Get the current state (True for extended, False for shrink)."""
        return self._is_extended

    @property
    def spacing(self):
        """Get or set spacing between icon and text."""
        return self._spacing

    @spacing.setter
    def spacing(self, value):
        """Set spacing between icon and text."""
        self._spacing = int(value)
        layout = self.layout()
        if layout:
            layout.setSpacing(self._spacing)

    @property
    def min_height(self):
        """Get or set the minimum height of the button."""
        return self._min_height

    @min_height.setter
    def min_height(self, value):
        """Set the minimum height of the button."""
        self._min_height = value
        self.updateGeometry()

    @property
    def duration(self):
        """Get or set the animation duration in milliseconds."""
        return self._animation_duration

    @duration.setter
    def duration(self, value):
        """Set the animation duration in milliseconds."""
        self._animation_duration = int(value)
        if hasattr(self, '_animation'):
            self._animation.setDuration(self._animation_duration)

    # UTILITY FUNCTIONS
    # ///////////////////////////////////////////////////////////////

    def clear_icon(self):
        """Remove the current icon."""
        self._current_icon = None
        self.icon_label.clear()
        self.iconChanged.emit(QIcon())

    def clear_text(self):
        """Clear the button text."""
        self.text = ""

    def toggle_state(self):
        """Toggle between shrink and extended states with animation."""
        self._is_extended = not self._is_extended
        self._update_state_display(animate=True)
        self.stateChanged.emit(self._is_extended)

    def set_state(self, extended: bool):
        """Set the state explicitly (True for extended, False for shrink) with animation."""
        if self._is_extended != extended:
            self._is_extended = extended
            self._update_state_display(animate=True)
            self.stateChanged.emit(self._is_extended)

    def set_icon_color(self, color="#FFFFFF", opacity=0.5):
        """Apply color and opacity to the current icon."""
        if self._current_icon:
            pixmap = self._current_icon.pixmap(self._icon_size)
            colored_pixmap = colorize_pixmap(pixmap, color, opacity)
            self.icon_label.setPixmap(colored_pixmap)

    def update_theme_icon(self, theme_icon):
        """Update the icon with a new ThemeIcon (for theme changes)."""
        if theme_icon:
            self._current_icon = theme_icon
            self.icon_label.setPixmap(theme_icon.pixmap(self._icon_size))
            self.icon_label.setFixedSize(self._icon_size)
            self.iconChanged.emit(theme_icon)

    def _update_state_display(self, animate=True):
        """Update the display based on current state with optional animation."""
        layout = self.layout()

        if self._is_extended:
            # Extended state: show text, icon stays in fixed position
            self.text_label.show()
            # Remove maximum width constraint
            self.setMaximumWidth(16777215)  # Qt's maximum value
            # Set minimum width to accommodate icon + text + spacing
            min_width = self._icon_size.width() + self._spacing + 20  # margins
            if self.text:
                min_width += self.text_label.fontMetrics().horizontalAdvance(self.text)
            self.setMinimumWidth(min_width)
            # Set layout alignment to left (icon stays in position, text appears to the right)
            if layout:
                layout.setAlignment(
                    Qt.AlignLeft | Qt.AlignVCenter
                )
                # Extended mode: position icon at calculated position, text to the right
                # CORRECTION: Use exact icon position without extra padding
                left_margin = self._icon_x_position
                layout.setContentsMargins(left_margin, 2, 8, 2)
                layout.setSpacing(self._spacing)
        else:
            # Shrink state: hide text, center icon perfectly
            self.text_label.hide()
            self.setMinimumWidth(self._shrink_size)
            self.setMaximumWidth(self._shrink_size)
            # Set layout alignment to center for shrink state
            if layout:
                layout.setAlignment(
                    Qt.AlignCenter | Qt.AlignVCenter
                )
                # Perfect centering: calculate exact margins
                icon_center = self._shrink_size // 2
                icon_left = icon_center - (self._icon_size.width() // 2)
                layout.setContentsMargins(icon_left, 2, icon_left, 2)
                layout.setSpacing(0)
        
        # Apply animation if requested
        if animate:
            self._animate_state_change()

    def _animate_state_change(self):
        """Animate the state change for smooth transitions."""
        # Stop any ongoing animation
        if self._animation.state() == QPropertyAnimation.State.Running:
            self._animation.stop()
        
        # Get current and target geometries
        current_rect = self.geometry()
        
        if self._is_extended:
            # Animate to extended state
            # Calculate target width based on content
            icon_width = self._icon_size.width() if self._current_icon else 0
            text_width = 0
            if self.text:
                text_width = self.text_label.fontMetrics().horizontalAdvance(self.text)
            target_width = self._icon_x_position + icon_width + self._spacing + text_width + 8
        else:
            # Animate to shrink state
            target_width = self._shrink_size
        
        target_rect = current_rect
        target_rect.setWidth(target_width)
        
        # Start animation
        self._animation.setStartValue(current_rect)
        self._animation.setEndValue(target_rect)
        self._animation.start()

    # OVERRIDE FUNCTIONS
    # ///////////////////////////////////////////////////////////////

    def sizeHint(self) -> QSize:
        """Get the recommended size for the button."""
        return QSize(100, 40)

    def minimumSizeHint(self) -> QSize:
        """Get the minimum size hint for the button."""
        # ////// CALCULATE BASE SIZE
        base_size = super().minimumSizeHint()

        # ////// CALCULATE WIDTH BASED ON STATE
        if self._is_extended:
            # Extended state: calculate full width
            # Icon position + icon width + spacing + text width + right margin
            icon_width = self._icon_size.width() if self._current_icon else 0
            text_width = 0
            if self.text:
                text_width = self.text_label.fontMetrics().horizontalAdvance(self.text)
            total_width = (
                self._icon_x_position + icon_width + self._spacing + text_width + 8
            )  # right margin
        else:
            # Shrink state: use shrink_size
            total_width = self._shrink_size

        # ////// CALCULATE HEIGHT
        min_height = (
            self._min_height
            if self._min_height is not None
            else max(base_size.height(), self._icon_size.height() + 8)
        )

        return QSize(total_width, min_height)

    # STYLE FUNCTIONS
    # ///////////////////////////////////////////////////////////////

    def refresh_style(self) -> None:
        """Refresh the widget's style (useful after dynamic stylesheet changes)."""
        # // REFRESH STYLE
        self.style().unpolish(self)
        self.style().polish(self)
        # //////
