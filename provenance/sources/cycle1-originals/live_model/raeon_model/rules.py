from .colors import Color

GENERATOR_COUNT_TO_MANIFOLD_COLOR = {
    3: Color.RED,
    4: Color.ORANGE,
    5: Color.YELLOW,
    6: Color.GREEN,
    7: Color.BLUE,
    8: Color.VIOLET,
}

def manifold_color_for_generator_count(count: int) -> Color:
    """Return ordinary manifold color for a legal 3..8-generator closure.

    IMPORTANT: generator count alone does NOT establish manifold legality.
    The topology/configuration solver must already have established a valid closure.
    """
    try:
        return GENERATOR_COUNT_TO_MANIFOLD_COLOR[count]
    except KeyError:
        raise ValueError("ordinary local manifolds currently require 3..8 generators")

def white_only_manifold_color(white_generator_count: int) -> Color:
    """Current rule: 3..8 White universal Generators map to Red..Violet.
    White is not produced by eight White Generators.
    """
    return manifold_color_for_generator_count(white_generator_count)
