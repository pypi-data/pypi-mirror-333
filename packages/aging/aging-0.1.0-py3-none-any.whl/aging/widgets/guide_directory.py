"""Provides the guide directory widget."""

##############################################################################
# NGDB imports.
from ngdb import NortonGuide

##############################################################################
# Textual imports.
from textual import on
from textual.reactive import var
from textual.widgets.option_list import Option, OptionDoesNotExist

##############################################################################
# Textual enhanced imports.
from textual_enhanced.widgets import EnhancedOptionList

##############################################################################
# Local imports.
from ..data import Guide, Guides
from ..messages import OpenGuide


##############################################################################
class GuideView(Option):
    """A view of an option in the guide directory widget."""

    def __init__(self, guide: Guide) -> None:
        """Initialise the guide option."""
        self._guide = guide
        """The guide being handled by this option."""
        super().__init__(guide.title, id=str(guide.location))

    @property
    def guide(self) -> Guide:
        """The guide being handled by this option."""
        return self._guide


##############################################################################
class GuideDirectory(EnhancedOptionList):
    """A widget that holds and manages the Norton Guide directory."""

    DEFAULT_CSS = """
    GuideDirectory {
        width: auto;
        dock: left;
        background: transparent;
        height: 1fr;
        border: none;

        &:focus {
            border: none;
        }

        &.--dock-right {
            dock: right;
        }
    }
    """

    HELP = """
    ## Guide directory

    This is the directory of all the Norton Guide files that have been added
    to the application.
    """

    dock_right: var[bool] = var(False)
    """Should the directory dock to the right?"""

    guides: var[Guides] = var(Guides)
    """The guides in the directory."""

    guide: var[NortonGuide | None] = var(None)
    """The currently-selected guide.

    Note:
        This isn't the currently-highlighted guide, this is the guide that
        has been selected for display. Setting this will move the highlight
        in the widget to the correct position.
    """

    def _watch_guides(self) -> None:
        """React to the guides being changed."""
        with self.preserved_highlight:
            self.clear_options().add_options(GuideView(guide) for guide in self.guides)

    def _watch_dock_right(self) -> None:
        """React to the dock toggle being changed."""
        self.set_class(self.dock_right, "--dock-right")

    def _watch_guide(self) -> None:
        """React to the current guide being set."""
        try:
            self.highlighted = (
                self.get_option_index(str(self.guide))
                if self.guide is not None
                else None
            )
        except OptionDoesNotExist:
            pass

    @on(EnhancedOptionList.OptionSelected)
    def _open_guide(self, message: EnhancedOptionList.OptionSelected) -> None:
        """React to a user's request to open a guide.

        Args:
            message: The message with the details of the request.
        """
        message.stop()
        assert isinstance(message.option, GuideView)
        self.post_message(OpenGuide(message.option.guide.location))


### guide_directory.py ends here
