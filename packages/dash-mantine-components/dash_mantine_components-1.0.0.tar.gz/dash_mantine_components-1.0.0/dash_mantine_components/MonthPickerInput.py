# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class MonthPickerInput(Component):
    """A MonthPickerInput component.
MonthPickerInput

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- allowDeselect (boolean; optional):
    Determines whether user can deselect the date by clicking on
    selected item, applicable only when type=\"default\".

- allowSingleDateInRange (boolean; optional):
    Determines whether single year can be selected as range,
    applicable only when type=\"range\".

- aria-* (string; optional):
    Wild card aria attributes.

- ariaLabels (dict; optional):
    aria-label attributes for controls on different levels.

    `ariaLabels` is a dict with keys:

    - monthLevelControl (string; optional)

    - yearLevelControl (string; optional)

    - nextMonth (string; optional)

    - previousMonth (string; optional)

    - nextYear (string; optional)

    - previousYear (string; optional)

    - nextDecade (string; optional)

    - previousDecade (string; optional)

- bd (string | number; optional):
    Border.

- bg (boolean | number | string | dict | list; optional):
    Background, theme key: theme.colors.

- bga (boolean | number | string | dict | list; optional):
    BackgroundAttachment.

- bgp (string | number; optional):
    BackgroundPosition.

- bgr (boolean | number | string | dict | list; optional):
    BackgroundRepeat.

- bgsz (string | number; optional):
    BackgroundSize.

- bottom (string | number; optional)

- c (boolean | number | string | dict | list; optional):
    Color.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds class names to Mantine components.

- clearButtonProps (dict; optional):
    Props passed down to clear button.

    `clearButtonProps` is a dict with keys:

    - size (boolean | number | string | dict | list; optional):
        Size of the button, by default value is based on input
        context.

    - radius (number; optional):
        Key of `theme.radius` or any valid CSS value to set
        border-radius. Numbers are converted to rem.
        `theme.defaultRadius` by default.

    - disabled (boolean; optional):
        Sets `disabled` and `data-disabled` attributes on the button
        element.

    - iconSize (string | number; optional):
        `X` icon `width` and `height`, `80%` by default.

    - children (a list of or a singular dash component, string or number; optional):
        Content rendered inside the button, for example
        `VisuallyHidden` with label for screen readers.

    - icon (a list of or a singular dash component, string or number; optional):
        Replaces default close icon. If set, `iconSize` prop is
        ignored.

- clearable (boolean; optional):
    Determines whether input value can be cleared, adds clear button
    to right section, False by default.

- closeOnChange (boolean; optional):
    Determines whether dropdown should be closed when date is
    selected, not applicable when type=\"multiple\", True by default.

- columnsToScroll (number; optional):
    Number of columns to scroll when user clicks next/prev buttons,
    defaults to numberOfColumns.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

- debounce (number; default False):
    Debounce time in ms.

- decadeLabelFormat (string; optional):
    dayjs label format to display decade label or a function that
    returns decade label based on date value, defaults to \"YYYY\".

- description (a list of or a singular dash component, string or number; optional):
    Contents of `Input.Description` component. If not set, description
    is not rendered.

- descriptionProps (dict with strings as keys and values of type boolean | number | string | dict | list; optional):
    Props passed down to the `Input.Description` component.

- disabled (boolean; optional):
    Sets `disabled` attribute on the `input` element.

- disabledDates (list of strings; optional):
    Specifies days that should be disabled.

- display (boolean | number | string | dict | list; optional)

- dropdownType (a value equal to: 'popover', 'modal'; optional):
    Type of dropdown, defaults to popover.

- error (a list of or a singular dash component, string or number; optional):
    Contents of `Input.Error` component. If not set, error is not
    rendered.

- errorProps (dict with strings as keys and values of type boolean | number | string | dict | list; optional):
    Props passed down to the `Input.Error` component.

- ff (boolean | number | string | dict | list; optional):
    FontFamily.

- firstDayOfWeek (a value equal to: 0, 1, 2, 3, 4, 5, 6; optional):
    number 0-6, 0 – Sunday, 6 – Saturday, defaults to 1 – Monday.

- flex (string | number; optional)

- fs (boolean | number | string | dict | list; optional):
    FontStyle.

- fw (boolean | number | string | dict | list; optional):
    FontWeight.

- fz (number; optional):
    FontSize, theme key: theme.fontSizes.

- h (string | number; optional):
    Height, theme key: theme.spacing.

- hasNextLevel (boolean; optional):
    Determines whether next level button should be enabled, defaults
    to True.

- hiddenFrom (boolean | number | string | dict | list; optional):
    Breakpoint above which the component is hidden with `display:
    none`.

- hideOutsideDates (boolean; optional):
    Determines whether outside dates should be hidden, defaults to
    False.

- hideWeekdays (boolean; optional):
    Determines whether weekdays row should be hidden, defaults to
    False.

- inputWrapperOrder (list of a value equal to: 'label', 'description', 'error', 'input's; optional):
    Controls order of the elements, `['label', 'description', 'input',
    'error']` by default.

- inset (string | number; optional)

- label (a list of or a singular dash component, string or number; optional):
    Contents of `Input.Label` component. If not set, label is not
    rendered.

- labelProps (dict with strings as keys and values of type boolean | number | string | dict | list; optional):
    Props passed down to the `Input.Label` component.

- labelSeparator (string; optional):
    Separator between range value.

- left (string | number; optional)

- leftSection (a list of or a singular dash component, string or number; optional):
    Content section rendered on the left side of the input.

- leftSectionPointerEvents (a value equal to: '-moz-initial', 'inherit', 'initial', 'revert', 'revert-layer', 'unset', 'auto', 'none', 'all', 'fill', 'painted', 'stroke', 'visible', 'visibleFill', 'visiblePainted', 'visibleStroke'; optional):
    Sets `pointer-events` styles on the `leftSection` element,
    `'none'` by default.

- leftSectionProps (dict; optional):
    Props passed down to the `leftSection` element.

- leftSectionWidth (string | number; optional):
    Left section width, used to set `width` of the section and input
    `padding-left`, by default equals to the input height.

- level (a value equal to: 'year', 'decade'; optional):
    Current level displayed to the user (decade, year), used for
    controlled component.

- lh (number; optional):
    LineHeight, theme key: lineHeights.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer. For use with dash<3.

    `loading_state` is a dict with keys:

    - is_loading (boolean; required):
        Determines if the component is loading or not.

    - prop_name (string; required):
        Holds which property is loading.

    - component_name (string; required):
        Holds the name of the component that is loading.

- lts (string | number; optional):
    LetterSpacing.

- m (number; optional):
    Margin, theme key: theme.spacing.

- mah (string | number; optional):
    MaxHeight, theme key: theme.spacing.

- maw (string | number; optional):
    MaxWidth, theme key: theme.spacing.

- maxDate (string; optional):
    Maximum possible date.

- maxLevel (a value equal to: 'year', 'decade'; optional):
    Max level that user can go up to (decade, year), defaults to
    decade.

- mb (number; optional):
    MarginBottom, theme key: theme.spacing.

- me (number; optional):
    MarginInlineEnd, theme key: theme.spacing.

- mih (string | number; optional):
    MinHeight, theme key: theme.spacing.

- minDate (string; optional):
    Minimum possible date.

- miw (string | number; optional):
    MinWidth, theme key: theme.spacing.

- ml (number; optional):
    MarginLeft, theme key: theme.spacing.

- mod (string | dict with strings as keys and values of type boolean | number | string | dict | list; optional):
    Element modifiers transformed into `data-` attributes, for
    example, `{ 'data-size': 'xl' }`, falsy values are removed.

- modalProps (dict; optional):
    Props passed down to Modal component.

    `modalProps` is a dict with keys:

    - className (string; optional):
        Class added to the root element, if applicable.

    - style (optional):
        Inline style added to root component element, can subscribe to
        theme defined on MantineProvider.

    - hiddenFrom (boolean | number | string | dict | list; optional):
        Breakpoint above which the component is hidden with `display:
        none`.

    - visibleFrom (boolean | number | string | dict | list; optional):
        Breakpoint below which the component is hidden with `display:
        none`.

    - lightHidden (boolean; optional):
        Determines whether component should be hidden in light color
        scheme with `display: none`.

    - darkHidden (boolean; optional):
        Determines whether component should be hidden in dark color
        scheme with `display: none`.

    - mod (string | dict with strings as keys and values of type boolean | number | string | dict | list; optional):
        Element modifiers transformed into `data-` attributes, for
        example, `{ 'data-size': 'xl' }`, falsy values are removed.

    - m (number; optional):
        Margin, theme key: theme.spacing.

    - my (number; optional):
        MarginBlock, theme key: theme.spacing.

    - mx (number; optional):
        MarginInline, theme key: theme.spacing.

    - mt (number; optional):
        MarginTop, theme key: theme.spacing.

    - mb (number; optional):
        MarginBottom, theme key: theme.spacing.

    - ms (number; optional):
        MarginInlineStart, theme key: theme.spacing.

    - me (number; optional):
        MarginInlineEnd, theme key: theme.spacing.

    - ml (number; optional):
        MarginLeft, theme key: theme.spacing.

    - mr (number; optional):
        MarginRight, theme key: theme.spacing.

    - p (number; optional):
        Padding, theme key: theme.spacing.

    - py (number; optional):
        PaddingBlock, theme key: theme.spacing.

    - px (number; optional):
        PaddingInline, theme key: theme.spacing.

    - pt (number; optional):
        PaddingTop, theme key: theme.spacing.

    - pb (number; optional):
        PaddingBottom, theme key: theme.spacing.

    - ps (number; optional):
        PaddingInlineStart, theme key: theme.spacing.

    - pe (number; optional):
        PaddingInlineEnd, theme key: theme.spacing.

    - pl (number; optional):
        PaddingLeft, theme key: theme.spacing.

    - pr (number; optional):
        PaddingRight, theme key: theme.spacing.

    - bd (string | number; optional):
        Border.

    - bg (boolean | number | string | dict | list; optional):
        Background, theme key: theme.colors.

    - c (boolean | number | string | dict | list; optional):
        Color.

    - opacity (boolean | number | string | dict | list; optional)

    - ff (boolean | number | string | dict | list; optional):
        FontFamily.

    - fz (number; optional):
        FontSize, theme key: theme.fontSizes.

    - fw (boolean | number | string | dict | list; optional):
        FontWeight.

    - lts (string | number; optional):
        LetterSpacing.

    - ta (boolean | number | string | dict | list; optional):
        TextAlign.

    - lh (number; optional):
        LineHeight, theme key: lineHeights.

    - fs (boolean | number | string | dict | list; optional):
        FontStyle.

    - tt (boolean | number | string | dict | list; optional):
        TextTransform.

    - td (string | number; optional):
        TextDecoration.

    - w (string | number; optional):
        Width, theme key: theme.spacing.

    - miw (string | number; optional):
        MinWidth, theme key: theme.spacing.

    - maw (string | number; optional):
        MaxWidth, theme key: theme.spacing.

    - h (string | number; optional):
        Height, theme key: theme.spacing.

    - mih (string | number; optional):
        MinHeight, theme key: theme.spacing.

    - mah (string | number; optional):
        MaxHeight, theme key: theme.spacing.

    - bgsz (string | number; optional):
        BackgroundSize.

    - bgp (string | number; optional):
        BackgroundPosition.

    - bgr (boolean | number | string | dict | list; optional):
        BackgroundRepeat.

    - bga (boolean | number | string | dict | list; optional):
        BackgroundAttachment.

    - pos (boolean | number | string | dict | list; optional):
        Position.

    - top (string | number; optional)

    - left (string | number; optional)

    - bottom (string | number; optional)

    - right (string | number; optional)

    - inset (string | number; optional)

    - display (boolean | number | string | dict | list; optional)

    - flex (string | number; optional)

    - size (number; optional):
        Controls width of the content area, `'md'` by default.

    - radius (number; optional):
        Key of `theme.radius` or any valid CSS value to set
        `border-radius`, `theme.defaultRadius` by default.

    - opened (boolean; optional):
        Determines whether modal/drawer is opened.

    - closeOnClickOutside (boolean; optional):
        Determines whether the modal/drawer should be closed when user
        clicks on the overlay, `True` by default.

    - trapFocus (boolean; optional):
        Determines whether focus should be trapped, `True` by default.

    - closeOnEscape (boolean; optional):
        Determines whether `onClose` should be called when user
        presses the escape key, `True` by default.

    - keepMounted (boolean; optional):
        If set modal/drawer will not be unmounted from the DOM when it
        is hidden, `display: none` styles will be added instead,
        `False` by default.

    - transitionProps (dict; optional):
        Props added to the `Transition` component that used to animate
        overlay and body, use to configure duration and animation
        type, `{ duration: 200, transition: 'pop' }` by default.

        `transitionProps` is a dict with keys:

        - keepMounted (boolean; optional):
            If set element will not be unmounted from the DOM when it
            is hidden, `display: none` styles will be applied instead.

        - transition (boolean | number | string | dict | list; optional):
            Transition name or object.

        - duration (number; optional):
            Transition duration in ms, `250` by default.

        - exitDuration (number; optional):
            Exit transition duration in ms, `250` by default.

        - timingFunction (string; optional):
            Transition timing function,
            `theme.transitionTimingFunction` by default.

        - mounted (boolean; required):
            Determines whether component should be mounted to the DOM.

    - withinPortal (boolean; optional):
        Determines whether the component should be rendered inside
        `Portal`, `True` by default.

    - portalProps (dict; optional):
        Props passed down to the Portal component when `withinPortal`
        is set.

    - zIndex (string | number; optional):
        `z-index` CSS property of the root element, `200` by default.

    - shadow (boolean | number | string | dict | list; optional):
        Key of `theme.shadows` or any valid CSS box-shadow value, 'xl'
        by default.

    - returnFocus (boolean; optional):
        Determines whether focus should be returned to the last active
        element when `onClose` is called, `True` by default.

    - overlayProps (dict; optional):
        Props passed down to the `Overlay` component, use to configure
        opacity, `background-color`, styles and other properties.

        `overlayProps` is a dict with keys:

        - transitionProps (dict; optional):
            Props passed down to the `Transition` component.

            `transitionProps` is a dict with keys:

            - keepMounted (boolean; optional):
                If set element will not be unmounted from the DOM when
                it is hidden, `display: none` styles will be applied
                instead.

            - transition (boolean | number | string | dict | list; optional):
                Transition name or object.

            - duration (number; optional):
                Transition duration in ms, `250` by default.

            - exitDuration (number; optional):
                Exit transition duration in ms, `250` by default.

            - timingFunction (string; optional):
                Transition timing function,
                `theme.transitionTimingFunction` by default.

            - mounted (boolean; required):
                Determines whether component should be mounted to the
                DOM.

        - className (string; optional):
            Class added to the root element, if applicable.

        - style (optional):
            Inline style added to root component element, can
            subscribe to theme defined on MantineProvider.

        - hiddenFrom (boolean | number | string | dict | list; optional):
            Breakpoint above which the component is hidden with
            `display: none`.

        - visibleFrom (boolean | number | string | dict | list; optional):
            Breakpoint below which the component is hidden with
            `display: none`.

        - lightHidden (boolean; optional):
            Determines whether component should be hidden in light
            color scheme with `display: none`.

        - darkHidden (boolean; optional):
            Determines whether component should be hidden in dark
            color scheme with `display: none`.

        - mod (string | dict with strings as keys and values of type boolean | number | string | dict | list; optional):
            Element modifiers transformed into `data-` attributes, for
            example, `{ 'data-size': 'xl' }`, falsy values are
            removed.

        - m (number; optional):
            Margin, theme key: theme.spacing.

        - my (number; optional):
            MarginBlock, theme key: theme.spacing.

        - mx (number; optional):
            MarginInline, theme key: theme.spacing.

        - mt (number; optional):
            MarginTop, theme key: theme.spacing.

        - mb (number; optional):
            MarginBottom, theme key: theme.spacing.

        - ms (number; optional):
            MarginInlineStart, theme key: theme.spacing.

        - me (number; optional):
            MarginInlineEnd, theme key: theme.spacing.

        - ml (number; optional):
            MarginLeft, theme key: theme.spacing.

        - mr (number; optional):
            MarginRight, theme key: theme.spacing.

        - p (number; optional):
            Padding, theme key: theme.spacing.

        - py (number; optional):
            PaddingBlock, theme key: theme.spacing.

        - px (number; optional):
            PaddingInline, theme key: theme.spacing.

        - pt (number; optional):
            PaddingTop, theme key: theme.spacing.

        - pb (number; optional):
            PaddingBottom, theme key: theme.spacing.

        - ps (number; optional):
            PaddingInlineStart, theme key: theme.spacing.

        - pe (number; optional):
            PaddingInlineEnd, theme key: theme.spacing.

        - pl (number; optional):
            PaddingLeft, theme key: theme.spacing.

        - pr (number; optional):
            PaddingRight, theme key: theme.spacing.

        - bd (string | number; optional):
            Border.

        - bg (boolean | number | string | dict | list; optional):
            Background, theme key: theme.colors.

        - c (boolean | number | string | dict | list; optional):
            Color.

        - opacity (boolean | number | string | dict | list; optional)

        - ff (boolean | number | string | dict | list; optional):
            FontFamily.

        - fz (number; optional):
            FontSize, theme key: theme.fontSizes.

        - fw (boolean | number | string | dict | list; optional):
            FontWeight.

        - lts (string | number; optional):
            LetterSpacing.

        - ta (boolean | number | string | dict | list; optional):
            TextAlign.

        - lh (number; optional):
            LineHeight, theme key: lineHeights.

        - fs (boolean | number | string | dict | list; optional):
            FontStyle.

        - tt (boolean | number | string | dict | list; optional):
            TextTransform.

        - td (string | number; optional):
            TextDecoration.

        - w (string | number; optional):
            Width, theme key: theme.spacing.

        - miw (string | number; optional):
            MinWidth, theme key: theme.spacing.

        - maw (string | number; optional):
            MaxWidth, theme key: theme.spacing.

        - h (string | number; optional):
            Height, theme key: theme.spacing.

        - mih (string | number; optional):
            MinHeight, theme key: theme.spacing.

        - mah (string | number; optional):
            MaxHeight, theme key: theme.spacing.

        - bgsz (string | number; optional):
            BackgroundSize.

        - bgp (string | number; optional):
            BackgroundPosition.

        - bgr (boolean | number | string | dict | list; optional):
            BackgroundRepeat.

        - bga (boolean | number | string | dict | list; optional):
            BackgroundAttachment.

        - pos (boolean | number | string | dict | list; optional):
            Position.

        - top (string | number; optional)

        - left (string | number; optional)

        - bottom (string | number; optional)

        - right (string | number; optional)

        - inset (string | number; optional)

        - display (boolean | number | string | dict | list; optional)

        - flex (string | number; optional)

        - radius (number; optional):
            Key of `theme.radius` or any valid CSS value to set
            border-radius, `0` by default.

        - unstyled (boolean; optional):
            Remove all Mantine styling from the component.

        - children (a list of or a singular dash component, string or number; optional):
            Content inside overlay.

        - zIndex (string | number; optional):
            Overlay z-index, `200` by default.

        - center (boolean; optional):
            Determines whether content inside overlay should be
            vertically and horizontally centered, `False` by default.

        - fixed (boolean; optional):
            Determines whether overlay should have fixed position
            instead of absolute, `False` by default.

        - backgroundOpacity (number; optional):
            Controls overlay `background-color` opacity 0–1,
            disregarded when `gradient` prop is set, `0.6` by default.

        - color (boolean | number | string | dict | list; optional):
            Overlay `background-color`, `#000` by default.

        - blur (string | number; optional):
            Overlay background blur, `0` by default.

        - gradient (string; optional):
            Changes overlay to gradient. If set, `color` prop is
            ignored.

    - withOverlay (boolean; optional):
        Determines whether the overlay should be rendered, `True` by
        default.

    - padding (number; optional):
        Key of `theme.spacing` or any valid CSS value to set content,
        header and footer padding, `'md'` by default.

    - title (a list of or a singular dash component, string or number; optional):
        Modal title.

    - withCloseButton (boolean; optional):
        Determines whether the close button should be rendered, `True`
        by default.

    - closeButtonProps (dict; optional):
        Props passed down to the close button.

        `closeButtonProps` is a dict with keys:

        - size (number; optional):
            Controls width and height of the button. Numbers are
            converted to rem. `'md'` by default.

        - radius (number; optional):
            Key of `theme.radius` or any valid CSS value to set
            border-radius. Numbers are converted to rem.
            `theme.defaultRadius` by default.

        - disabled (boolean; optional):
            Sets `disabled` and `data-disabled` attributes on the
            button element.

        - iconSize (string | number; optional):
            `X` icon `width` and `height`, `80%` by default.

        - children (a list of or a singular dash component, string or number; optional):
            Content rendered inside the button, for example
            `VisuallyHidden` with label for screen readers.

        - icon (a list of or a singular dash component, string or number; optional):
            Replaces default close icon. If set, `iconSize` prop is
            ignored.

        - className (string; optional):
            Class added to the root element, if applicable.

        - style (optional):
            Inline style added to root component element, can
            subscribe to theme defined on MantineProvider.

        - hiddenFrom (boolean | number | string | dict | list; optional):
            Breakpoint above which the component is hidden with
            `display: none`.

        - visibleFrom (boolean | number | string | dict | list; optional):
            Breakpoint below which the component is hidden with
            `display: none`.

        - lightHidden (boolean; optional):
            Determines whether component should be hidden in light
            color scheme with `display: none`.

        - darkHidden (boolean; optional):
            Determines whether component should be hidden in dark
            color scheme with `display: none`.

        - mod (string | dict with strings as keys and values of type boolean | number | string | dict | list; optional):
            Element modifiers transformed into `data-` attributes, for
            example, `{ 'data-size': 'xl' }`, falsy values are
            removed.

        - m (number; optional):
            Margin, theme key: theme.spacing.

        - my (number; optional):
            MarginBlock, theme key: theme.spacing.

        - mx (number; optional):
            MarginInline, theme key: theme.spacing.

        - mt (number; optional):
            MarginTop, theme key: theme.spacing.

        - mb (number; optional):
            MarginBottom, theme key: theme.spacing.

        - ms (number; optional):
            MarginInlineStart, theme key: theme.spacing.

        - me (number; optional):
            MarginInlineEnd, theme key: theme.spacing.

        - ml (number; optional):
            MarginLeft, theme key: theme.spacing.

        - mr (number; optional):
            MarginRight, theme key: theme.spacing.

        - p (number; optional):
            Padding, theme key: theme.spacing.

        - py (number; optional):
            PaddingBlock, theme key: theme.spacing.

        - px (number; optional):
            PaddingInline, theme key: theme.spacing.

        - pt (number; optional):
            PaddingTop, theme key: theme.spacing.

        - pb (number; optional):
            PaddingBottom, theme key: theme.spacing.

        - ps (number; optional):
            PaddingInlineStart, theme key: theme.spacing.

        - pe (number; optional):
            PaddingInlineEnd, theme key: theme.spacing.

        - pl (number; optional):
            PaddingLeft, theme key: theme.spacing.

        - pr (number; optional):
            PaddingRight, theme key: theme.spacing.

        - bd (string | number; optional):
            Border.

        - bg (boolean | number | string | dict | list; optional):
            Background, theme key: theme.colors.

        - c (boolean | number | string | dict | list; optional):
            Color.

        - opacity (boolean | number | string | dict | list; optional)

        - ff (boolean | number | string | dict | list; optional):
            FontFamily.

        - fz (number; optional):
            FontSize, theme key: theme.fontSizes.

        - fw (boolean | number | string | dict | list; optional):
            FontWeight.

        - lts (string | number; optional):
            LetterSpacing.

        - ta (boolean | number | string | dict | list; optional):
            TextAlign.

        - lh (number; optional):
            LineHeight, theme key: lineHeights.

        - fs (boolean | number | string | dict | list; optional):
            FontStyle.

        - tt (boolean | number | string | dict | list; optional):
            TextTransform.

        - td (string | number; optional):
            TextDecoration.

        - w (string | number; optional):
            Width, theme key: theme.spacing.

        - miw (string | number; optional):
            MinWidth, theme key: theme.spacing.

        - maw (string | number; optional):
            MaxWidth, theme key: theme.spacing.

        - h (string | number; optional):
            Height, theme key: theme.spacing.

        - mih (string | number; optional):
            MinHeight, theme key: theme.spacing.

        - mah (string | number; optional):
            MaxHeight, theme key: theme.spacing.

        - bgsz (string | number; optional):
            BackgroundSize.

        - bgp (string | number; optional):
            BackgroundPosition.

        - bgr (boolean | number | string | dict | list; optional):
            BackgroundRepeat.

        - bga (boolean | number | string | dict | list; optional):
            BackgroundAttachment.

        - pos (boolean | number | string | dict | list; optional):
            Position.

        - top (string | number; optional)

        - left (string | number; optional)

        - bottom (string | number; optional)

        - right (string | number; optional)

        - inset (string | number; optional)

        - display (boolean | number | string | dict | list; optional)

        - flex (string | number; optional)

    - yOffset (string | number; optional):
        Top/bottom modal offset, `5dvh` by default.

    - xOffset (string | number; optional):
        Left/right modal offset, `5vw` by default.

    - centered (boolean; optional):
        Determines whether the modal should be centered vertically,
        `False` by default.

    - fullScreen (boolean; optional):
        Determines whether the modal should take the entire screen,
        `False` by default.

    - lockScroll (boolean; optional):
        Determines whether scroll should be locked when
        `opened={True}`, `True` by default.

    - removeScrollProps (dict; optional):
        Props passed down to react-remove-scroll, can be used to
        customize scroll lock behavior.

- monthLabelFormat (string; optional):
    dayjs label format to display month label or a function that
    returns month label based on month value, defaults to \"MMMM
    YYYY\".

- monthsListFormat (string; optional):
    dayjs format for months list.

- mr (number; optional):
    MarginRight, theme key: theme.spacing.

- ms (number; optional):
    MarginInlineStart, theme key: theme.spacing.

- mt (number; optional):
    MarginTop, theme key: theme.spacing.

- mx (number; optional):
    MarginInline, theme key: theme.spacing.

- my (number; optional):
    MarginBlock, theme key: theme.spacing.

- n_submit (number; default 0):
    An integer that represents the number of times that this element
    has been submitted.

- name (string; optional):
    Name prop.

- nextIcon (a list of or a singular dash component, string or number; optional):
    Change next icon.

- nextLabel (string; optional):
    aria-label for next button.

- numberOfColumns (number; optional):
    Number of columns to render next to each other.

- opacity (boolean | number | string | dict | list; optional)

- p (number; optional):
    Padding, theme key: theme.spacing.

- pb (number; optional):
    PaddingBottom, theme key: theme.spacing.

- pe (number; optional):
    PaddingInlineEnd, theme key: theme.spacing.

- persisted_props (list of strings; optional):
    Properties whose user interactions will persist after refreshing
    the component or the page. Since only `value` is allowed this prop
    can normally be ignored.

- persistence (string | number; optional):
    Used to allow user interactions in this component to be persisted
    when the component - or the page - is refreshed. If `persisted` is
    truthy and hasn't changed from its previous value, a `value` that
    the user has changed while using the app will keep that change, as
    long as the new `value` also matches what was given originally.
    Used in conjunction with `persistence_type`.

- persistence_type (a value equal to: 'local', 'session', 'memory'; optional):
    Where persisted user changes will be stored: memory: only kept in
    memory, reset on page refresh. local: window.localStorage, data is
    kept after the browser quit. session: window.sessionStorage, data
    is cleared once the browser quit.

- pl (number; optional):
    PaddingLeft, theme key: theme.spacing.

- placeholder (string; optional):
    Input placeholder.

- pointer (boolean; optional):
    Determines whether the input should have `cursor: pointer` style,
    `False` by default.

- popoverProps (dict; optional):
    Props passed down to Popover component.

    `popoverProps` is a dict with keys:

    - radius (number; optional):
        Key of `theme.radius` or any valid CSS value to set
        border-radius, `theme.defaultRadius` by default.

    - disabled (boolean; optional):
        If set, popover dropdown will not be rendered.

    - classNames (dict; optional):
        Adds class names to Mantine components.

    - styles (boolean | number | string | dict | list; optional):
        Mantine styles API.

    - unstyled (boolean; optional):
        Remove all Mantine styling from the component.

    - variant (string; optional):
        variant.

    - opened (boolean; optional):
        Controlled dropdown opened state.

    - closeOnClickOutside (boolean; optional):
        Determines whether dropdown should be closed on outside
        clicks, `True` by default.

    - clickOutsideEvents (list of strings; optional):
        Events that trigger outside clicks.

    - trapFocus (boolean; optional):
        Determines whether focus should be trapped within dropdown,
        `False` by default.

    - closeOnEscape (boolean; optional):
        Determines whether dropdown should be closed when `Escape` key
        is pressed, `True` by default.

    - withRoles (boolean; optional):
        Determines whether dropdown and target elements should have
        accessible roles, `True` by default.

    - position (a value equal to: 'top', 'left', 'bottom', 'right', 'top-end', 'top-start', 'left-end', 'left-start', 'bottom-end', 'bottom-start', 'right-end', 'right-start'; optional):
        Dropdown position relative to the target element, `'bottom'`
        by default.

    - offset (number; optional):
        Offset of the dropdown element, `8` by default.

    - positionDependencies (list of boolean | number | string | dict | lists; optional):
        `useEffect` dependencies to force update dropdown position,
        `[]` by default.

    - keepMounted (boolean; optional):
        If set dropdown will not be unmounted from the DOM when it is
        hidden, `display: none` styles will be added instead.

    - transitionProps (dict; optional):
        Props passed down to the `Transition` component that used to
        animate dropdown presence, use to configure duration and
        animation type, `{ duration: 150, transition: 'fade' }` by
        default.

        `transitionProps` is a dict with keys:

        - keepMounted (boolean; optional):
            If set element will not be unmounted from the DOM when it
            is hidden, `display: none` styles will be applied instead.

        - transition (boolean | number | string | dict | list; optional):
            Transition name or object.

        - duration (number; optional):
            Transition duration in ms, `250` by default.

        - exitDuration (number; optional):
            Exit transition duration in ms, `250` by default.

        - timingFunction (string; optional):
            Transition timing function,
            `theme.transitionTimingFunction` by default.

        - mounted (boolean; required):
            Determines whether component should be mounted to the DOM.

    - width (string | number; optional):
        Dropdown width, or `'target'` to make dropdown width the same
        as target element, `'max-content'` by default.

    - middlewares (dict; optional):
        Floating ui middlewares to configure position handling, `{
        flip: True, shift: True, inline: False }` by default.

        `middlewares` is a dict with keys:

        - shift (optional)

        - flip (dict; optional)

            `flip` is a dict with keys:

    - mainAxis (boolean; optional):
        The axis that runs along the side of the floating element.
        Determines  whether overflow along this axis is checked to
        perform a flip. @,default,True.

    - crossAxis (boolean; optional):
        The axis that runs along the alignment of the floating
        element. Determines  whether overflow along this axis is
        checked to perform a flip. @,default,True.

    - rootBoundary (dict; optional):
        The root clipping area in which overflow will be checked.
        @,default,'viewport'.

        `rootBoundary` is a dict with keys:

        - x (number; required)

        - y (number; required)

        - width (number; required)

        - height (number; required)

    - elementContext (a value equal to: 'reference', 'floating'; optional):
        The element in which overflow is being checked relative to a
        boundary. @,default,'floating'.

    - altBoundary (boolean; optional):
        Whether to check for overflow using the alternate element's
        boundary  (`clippingAncestors` boundary only).
        @,default,False.

    - padding (dict; optional):
        Virtual padding for the resolved overflow detection offsets.
        @,default,0.

        `padding` is a number

              Or dict with keys:

        - top (number; optional)

        - left (number; optional)

        - bottom (number; optional)

        - right (number; optional)

    - fallbackPlacements (list of a value equal to: 'top', 'left', 'bottom', 'right', 'top-end', 'top-start', 'left-end', 'left-start', 'bottom-end', 'bottom-start', 'right-end', 'right-start's; optional):
        Placements to try sequentially if the preferred `placement`
        does not fit. @,default,[oppositePlacement] (computed).

    - fallbackStrategy (a value equal to: 'bestFit', 'initialPlacement'; optional):
        What strategy to use when no placements fit.
        @,default,'bestFit'.

    - fallbackAxisSideDirection (a value equal to: 'end', 'start', 'none'; optional):
        Whether to allow fallback to the perpendicular axis of the
        preferred  placement, and if so, which side direction along
        the axis to prefer. @,default,'none' (disallow fallback).

    - flipAlignment (boolean; optional):
        Whether to flip to placements with the opposite alignment if
        they fit  better. @,default,True.

    - boundary (dict; optional)

        `boundary` is a dict with keys:

        - x (number; required)

        - y (number; required)

        - width (number; required)

        - height (number; required) | list of a list of or a singular dash component, string or numbers

        - inline (boolean | number | string | dict | list; optional)

        - size (optional)

    - withArrow (boolean; optional):
        Determines whether component should have an arrow, `False` by
        default.

    - arrowSize (number; optional):
        Arrow size in px, `7` by default.

    - arrowOffset (number; optional):
        Arrow offset in px, `5` by default.

    - arrowRadius (number; optional):
        Arrow `border-radius` in px, `0` by default.

    - arrowPosition (a value equal to: 'center', 'side'; optional):
        Arrow position.

    - withinPortal (boolean; optional):
        Determines whether dropdown should be rendered within the
        `Portal`, `True` by default.

    - portalProps (dict; optional):
        Props to pass down to the `Portal` when `withinPortal` is
        True.

    - zIndex (string | number; optional):
        Dropdown `z-index`, `300` by default.

    - shadow (boolean | number | string | dict | list; optional):
        Key of `theme.shadows` or any other valid CSS `box-shadow`
        value.

    - returnFocus (boolean; optional):
        Determines whether focus should be automatically returned to
        control when dropdown closes, `False` by default.

    - floatingStrategy (a value equal to: 'absolute', 'fixed'; optional):
        Changes floating ui [position
        strategy](https://floating-ui.com/docs/usefloating#strategy),
        `'absolute'` by default.

    - overlayProps (dict; optional):
        Props passed down to `Overlay` component.

    - withOverlay (boolean; optional):
        Determines whether the overlay should be displayed when the
        dropdown is opened, `False` by default.

- pos (boolean | number | string | dict | list; optional):
    Position.

- pr (number; optional):
    PaddingRight, theme key: theme.spacing.

- previousIcon (a list of or a singular dash component, string or number; optional):
    Change previous icon.

- previousLabel (string; optional):
    aria-label for previous button.

- ps (number; optional):
    PaddingInlineStart, theme key: theme.spacing.

- pt (number; optional):
    PaddingTop, theme key: theme.spacing.

- px (number; optional):
    PaddingInline, theme key: theme.spacing.

- py (number; optional):
    PaddingBlock, theme key: theme.spacing.

- radius (number; optional):
    Key of `theme.radius` or any valid CSS value to set
    `border-radius`, numbers are converted to rem,
    `theme.defaultRadius` by default.

- readOnly (boolean; optional):
    Determines whether the user can modify the value.

- required (boolean; optional):
    Adds required attribute to the input and a red asterisk on the
    right side of label, `False` by default.

- right (string | number; optional)

- rightSection (a list of or a singular dash component, string or number; optional):
    Content section rendered on the right side of the input.

- rightSectionPointerEvents (a value equal to: '-moz-initial', 'inherit', 'initial', 'revert', 'revert-layer', 'unset', 'auto', 'none', 'all', 'fill', 'painted', 'stroke', 'visible', 'visibleFill', 'visiblePainted', 'visibleStroke'; optional):
    Sets `pointer-events` styles on the `rightSection` element,
    `'none'` by default.

- rightSectionProps (dict; optional):
    Props passed down to the `rightSection` element.

- rightSectionWidth (string | number; optional):
    Right section width, used to set `width` of the section and input
    `padding-right`, by default equals to the input height.

- size (a value equal to: 'xs', 'sm', 'md', 'lg', 'xl'; optional):
    Component size.

- sortDates (boolean; optional):
    Determines whether dates value should be sorted before onChange
    call, only applicable when type=\"multiple\", True by default.

- style (optional):
    Inline style added to root component element, can subscribe to
    theme defined on MantineProvider.

- styles (boolean | number | string | dict | list; optional):
    Mantine styles API.

- ta (boolean | number | string | dict | list; optional):
    TextAlign.

- tabIndex (number; optional):
    tab-index.

- td (string | number; optional):
    TextDecoration.

- top (string | number; optional)

- tt (boolean | number | string | dict | list; optional):
    TextTransform.

- type (a value equal to: 'default', 'multiple', 'range'; optional):
    Picker type: range, multiple or default.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- value (string | list of strings; optional):
    Value for controlled component.

- valueFormat (string; optional):
    Dayjs format to display input value, \"MMMM D, YYYY\" by default.

- variant (string; optional):
    variant.

- visibleFrom (boolean | number | string | dict | list; optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- w (string | number; optional):
    Width, theme key: theme.spacing.

- weekdayFormat (string; optional):
    dayjs format for weekdays names, defaults to \"dd\".

- weekendDays (list of a value equal to: 0, 1, 2, 3, 4, 5, 6s; optional):
    Indices of weekend days, 0-6, where 0 is Sunday and 6 is Saturday,
    defaults to value defined in DatesProvider.

- withAsterisk (boolean; optional):
    Determines whether the required asterisk should be displayed.
    Overrides `required` prop. Does not add required attribute to the
    input. `False` by default.

- withCellSpacing (boolean; optional):
    Determines whether controls should be separated by spacing, True
    by default.

- withErrorStyles (boolean; optional):
    Determines whether the input should have red border and red text
    color when the `error` prop is set, `True` by default.

- wrapperProps (dict with strings as keys and values of type boolean | number | string | dict | list; optional):
    Props passed down to the root element.

- yearLabelFormat (string; optional):
    dayjs label format to display year label or a function that
    returns year label based on year value, defaults to \"YYYY\".

- yearsListFormat (string; optional):
    dayjs format for years list, `'YYYY'` by default."""
    _children_props = ['popoverProps.middlewares.flip.boundary', 'modalProps.overlayProps.children', 'modalProps.title', 'modalProps.closeButtonProps.children', 'modalProps.closeButtonProps.icon', 'clearButtonProps.children', 'clearButtonProps.icon', 'leftSection', 'rightSection', 'label', 'description', 'error', 'nextIcon', 'previousIcon']
    _base_nodes = ['leftSection', 'rightSection', 'label', 'description', 'error', 'nextIcon', 'previousIcon', 'children']
    _namespace = 'dash_mantine_components'
    _type = 'MonthPickerInput'
    LoadingState = TypedDict(
        "LoadingState",
            {
            "is_loading": bool,
            "prop_name": str,
            "component_name": str
        }
    )

    PopoverPropsTransitionProps = TypedDict(
        "PopoverPropsTransitionProps",
            {
            "keepMounted": NotRequired[bool],
            "transition": NotRequired[typing.Any],
            "duration": NotRequired[typing.Union[int, float, numbers.Number]],
            "exitDuration": NotRequired[typing.Union[int, float, numbers.Number]],
            "timingFunction": NotRequired[str],
            "mounted": bool
        }
    )

    PopoverPropsMiddlewaresFlipRootBoundary = TypedDict(
        "PopoverPropsMiddlewaresFlipRootBoundary",
            {
            "x": typing.Union[int, float, numbers.Number],
            "y": typing.Union[int, float, numbers.Number],
            "width": typing.Union[int, float, numbers.Number],
            "height": typing.Union[int, float, numbers.Number]
        }
    )

    PopoverPropsMiddlewaresFlipPadding = TypedDict(
        "PopoverPropsMiddlewaresFlipPadding",
            {
            "top": NotRequired[typing.Union[int, float, numbers.Number]],
            "left": NotRequired[typing.Union[int, float, numbers.Number]],
            "bottom": NotRequired[typing.Union[int, float, numbers.Number]],
            "right": NotRequired[typing.Union[int, float, numbers.Number]]
        }
    )

    PopoverPropsMiddlewaresFlipBoundary = TypedDict(
        "PopoverPropsMiddlewaresFlipBoundary",
            {
            "x": typing.Union[int, float, numbers.Number],
            "y": typing.Union[int, float, numbers.Number],
            "width": typing.Union[int, float, numbers.Number],
            "height": typing.Union[int, float, numbers.Number]
        }
    )

    PopoverPropsMiddlewaresFlip = TypedDict(
        "PopoverPropsMiddlewaresFlip",
            {
            "mainAxis": NotRequired[bool],
            "crossAxis": NotRequired[bool],
            "rootBoundary": NotRequired[typing.Union["PopoverPropsMiddlewaresFlipRootBoundary"]],
            "elementContext": NotRequired[Literal["reference", "floating"]],
            "altBoundary": NotRequired[bool],
            "padding": NotRequired[typing.Union[typing.Union[int, float, numbers.Number], "PopoverPropsMiddlewaresFlipPadding"]],
            "fallbackPlacements": NotRequired[typing.Sequence[Literal["top", "left", "bottom", "right", "top-end", "top-start", "left-end", "left-start", "bottom-end", "bottom-start", "right-end", "right-start"]]],
            "fallbackStrategy": NotRequired[Literal["bestFit", "initialPlacement"]],
            "fallbackAxisSideDirection": NotRequired[Literal["end", "start", "none"]],
            "flipAlignment": NotRequired[bool],
            "boundary": NotRequired[typing.Union["PopoverPropsMiddlewaresFlipBoundary", typing.Sequence[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]]]]
        }
    )

    PopoverPropsMiddlewares = TypedDict(
        "PopoverPropsMiddlewares",
            {
            "shift": NotRequired[typing.Union[typing.Any]],
            "flip": NotRequired[typing.Union["PopoverPropsMiddlewaresFlip"]],
            "inline": NotRequired[typing.Any],
            "size": NotRequired[typing.Union[typing.Any]]
        }
    )

    PopoverProps = TypedDict(
        "PopoverProps",
            {
            "radius": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "disabled": NotRequired[bool],
            "classNames": NotRequired[dict],
            "styles": NotRequired[typing.Any],
            "unstyled": NotRequired[bool],
            "variant": NotRequired[str],
            "opened": NotRequired[bool],
            "closeOnClickOutside": NotRequired[bool],
            "clickOutsideEvents": NotRequired[typing.Sequence[str]],
            "trapFocus": NotRequired[bool],
            "closeOnEscape": NotRequired[bool],
            "withRoles": NotRequired[bool],
            "position": NotRequired[Literal["top", "left", "bottom", "right", "top-end", "top-start", "left-end", "left-start", "bottom-end", "bottom-start", "right-end", "right-start"]],
            "offset": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "positionDependencies": NotRequired[typing.Sequence[typing.Any]],
            "keepMounted": NotRequired[bool],
            "transitionProps": NotRequired["PopoverPropsTransitionProps"],
            "width": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "middlewares": NotRequired["PopoverPropsMiddlewares"],
            "withArrow": NotRequired[bool],
            "arrowSize": NotRequired[typing.Union[int, float, numbers.Number]],
            "arrowOffset": NotRequired[typing.Union[int, float, numbers.Number]],
            "arrowRadius": NotRequired[typing.Union[int, float, numbers.Number]],
            "arrowPosition": NotRequired[Literal["center", "side"]],
            "withinPortal": NotRequired[bool],
            "portalProps": NotRequired[dict],
            "zIndex": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "shadow": NotRequired[typing.Any],
            "returnFocus": NotRequired[bool],
            "floatingStrategy": NotRequired[Literal["absolute", "fixed"]],
            "overlayProps": NotRequired[dict],
            "withOverlay": NotRequired[bool]
        }
    )

    ModalPropsTransitionProps = TypedDict(
        "ModalPropsTransitionProps",
            {
            "keepMounted": NotRequired[bool],
            "transition": NotRequired[typing.Any],
            "duration": NotRequired[typing.Union[int, float, numbers.Number]],
            "exitDuration": NotRequired[typing.Union[int, float, numbers.Number]],
            "timingFunction": NotRequired[str],
            "mounted": bool
        }
    )

    ModalPropsOverlayPropsTransitionProps = TypedDict(
        "ModalPropsOverlayPropsTransitionProps",
            {
            "keepMounted": NotRequired[bool],
            "transition": NotRequired[typing.Any],
            "duration": NotRequired[typing.Union[int, float, numbers.Number]],
            "exitDuration": NotRequired[typing.Union[int, float, numbers.Number]],
            "timingFunction": NotRequired[str],
            "mounted": bool
        }
    )

    ModalPropsOverlayProps = TypedDict(
        "ModalPropsOverlayProps",
            {
            "transitionProps": NotRequired["ModalPropsOverlayPropsTransitionProps"],
            "className": NotRequired[str],
            "style": NotRequired[typing.Union[typing.Any]],
            "hiddenFrom": NotRequired[typing.Any],
            "visibleFrom": NotRequired[typing.Any],
            "lightHidden": NotRequired[bool],
            "darkHidden": NotRequired[bool],
            "mod": NotRequired[typing.Union[str, typing.Dict[typing.Union[str, float, int], typing.Any]]],
            "m": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "my": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "mx": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "mt": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "mb": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "ms": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "me": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "ml": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "mr": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "p": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "py": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "px": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pt": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pb": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "ps": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pe": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pl": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pr": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "bd": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bg": NotRequired[typing.Any],
            "c": NotRequired[typing.Any],
            "opacity": NotRequired[typing.Any],
            "ff": NotRequired[typing.Any],
            "fz": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "fw": NotRequired[typing.Any],
            "lts": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "ta": NotRequired[typing.Any],
            "lh": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "fs": NotRequired[typing.Any],
            "tt": NotRequired[typing.Any],
            "td": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "w": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "miw": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "maw": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "h": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "mih": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "mah": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bgsz": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bgp": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bgr": NotRequired[typing.Any],
            "bga": NotRequired[typing.Any],
            "pos": NotRequired[typing.Any],
            "top": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "left": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bottom": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "right": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "inset": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "display": NotRequired[typing.Any],
            "flex": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "radius": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "unstyled": NotRequired[bool],
            "children": NotRequired[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]],
            "zIndex": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "center": NotRequired[bool],
            "fixed": NotRequired[bool],
            "backgroundOpacity": NotRequired[typing.Union[int, float, numbers.Number]],
            "color": NotRequired[typing.Any],
            "blur": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "gradient": NotRequired[str]
        }
    )

    ModalPropsCloseButtonProps = TypedDict(
        "ModalPropsCloseButtonProps",
            {
            "size": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "radius": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "disabled": NotRequired[bool],
            "iconSize": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "children": NotRequired[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]],
            "icon": NotRequired[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]],
            "className": NotRequired[str],
            "style": NotRequired[typing.Union[typing.Any]],
            "hiddenFrom": NotRequired[typing.Any],
            "visibleFrom": NotRequired[typing.Any],
            "lightHidden": NotRequired[bool],
            "darkHidden": NotRequired[bool],
            "mod": NotRequired[typing.Union[str, typing.Dict[typing.Union[str, float, int], typing.Any]]],
            "m": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "my": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "mx": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "mt": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "mb": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "ms": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "me": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "ml": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "mr": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "p": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "py": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "px": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pt": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pb": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "ps": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pe": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pl": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pr": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "bd": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bg": NotRequired[typing.Any],
            "c": NotRequired[typing.Any],
            "opacity": NotRequired[typing.Any],
            "ff": NotRequired[typing.Any],
            "fz": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "fw": NotRequired[typing.Any],
            "lts": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "ta": NotRequired[typing.Any],
            "lh": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "fs": NotRequired[typing.Any],
            "tt": NotRequired[typing.Any],
            "td": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "w": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "miw": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "maw": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "h": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "mih": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "mah": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bgsz": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bgp": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bgr": NotRequired[typing.Any],
            "bga": NotRequired[typing.Any],
            "pos": NotRequired[typing.Any],
            "top": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "left": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bottom": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "right": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "inset": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "display": NotRequired[typing.Any],
            "flex": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]]
        }
    )

    ModalProps = TypedDict(
        "ModalProps",
            {
            "className": NotRequired[str],
            "style": NotRequired[typing.Union[typing.Any]],
            "hiddenFrom": NotRequired[typing.Any],
            "visibleFrom": NotRequired[typing.Any],
            "lightHidden": NotRequired[bool],
            "darkHidden": NotRequired[bool],
            "mod": NotRequired[typing.Union[str, typing.Dict[typing.Union[str, float, int], typing.Any]]],
            "m": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "my": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "mx": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "mt": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "mb": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "ms": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "me": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "ml": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "mr": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "p": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "py": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "px": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pt": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pb": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "ps": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pe": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pl": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "pr": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "bd": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bg": NotRequired[typing.Any],
            "c": NotRequired[typing.Any],
            "opacity": NotRequired[typing.Any],
            "ff": NotRequired[typing.Any],
            "fz": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "fw": NotRequired[typing.Any],
            "lts": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "ta": NotRequired[typing.Any],
            "lh": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "fs": NotRequired[typing.Any],
            "tt": NotRequired[typing.Any],
            "td": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "w": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "miw": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "maw": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "h": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "mih": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "mah": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bgsz": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bgp": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bgr": NotRequired[typing.Any],
            "bga": NotRequired[typing.Any],
            "pos": NotRequired[typing.Any],
            "top": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "left": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "bottom": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "right": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "inset": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "display": NotRequired[typing.Any],
            "flex": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "size": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "radius": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "opened": NotRequired[bool],
            "closeOnClickOutside": NotRequired[bool],
            "trapFocus": NotRequired[bool],
            "closeOnEscape": NotRequired[bool],
            "keepMounted": NotRequired[bool],
            "transitionProps": NotRequired["ModalPropsTransitionProps"],
            "withinPortal": NotRequired[bool],
            "portalProps": NotRequired[dict],
            "zIndex": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "shadow": NotRequired[typing.Any],
            "returnFocus": NotRequired[bool],
            "overlayProps": NotRequired["ModalPropsOverlayProps"],
            "withOverlay": NotRequired[bool],
            "padding": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "title": NotRequired[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]],
            "withCloseButton": NotRequired[bool],
            "closeButtonProps": NotRequired["ModalPropsCloseButtonProps"],
            "yOffset": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "xOffset": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "centered": NotRequired[bool],
            "fullScreen": NotRequired[bool],
            "lockScroll": NotRequired[bool],
            "removeScrollProps": NotRequired[dict]
        }
    )

    ClearButtonProps = TypedDict(
        "ClearButtonProps",
            {
            "size": NotRequired[typing.Any],
            "radius": NotRequired[typing.Union[typing.Union[int, float, numbers.Number]]],
            "disabled": NotRequired[bool],
            "iconSize": NotRequired[typing.Union[str, typing.Union[int, float, numbers.Number]]],
            "children": NotRequired[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]],
            "icon": NotRequired[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]]
        }
    )

    AriaLabels = TypedDict(
        "AriaLabels",
            {
            "monthLevelControl": NotRequired[str],
            "yearLevelControl": NotRequired[str],
            "nextMonth": NotRequired[str],
            "previousMonth": NotRequired[str],
            "nextYear": NotRequired[str],
            "previousYear": NotRequired[str],
            "nextDecade": NotRequired[str],
            "previousDecade": NotRequired[str]
        }
    )

    @_explicitize_args
    def __init__(
        self,
        valueFormat: typing.Optional[str] = None,
        disabledDates: typing.Optional[typing.Sequence[str]] = None,
        n_submit: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        debounce: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        tabIndex: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        loading_state: typing.Optional["LoadingState"] = None,
        persistence: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        persisted_props: typing.Optional[typing.Sequence[str]] = None,
        persistence_type: typing.Optional[Literal["local", "session", "memory"]] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Union[typing.Any]] = None,
        hiddenFrom: typing.Optional[typing.Any] = None,
        visibleFrom: typing.Optional[typing.Any] = None,
        lightHidden: typing.Optional[bool] = None,
        darkHidden: typing.Optional[bool] = None,
        mod: typing.Optional[typing.Union[str, typing.Dict[typing.Union[str, float, int], typing.Any]]] = None,
        m: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        my: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        mx: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        mt: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        mb: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        ms: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        me: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        ml: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        mr: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        p: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        py: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        px: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        pt: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        pb: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        ps: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        pe: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        pl: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        pr: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        bd: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        bg: typing.Optional[typing.Any] = None,
        c: typing.Optional[typing.Any] = None,
        opacity: typing.Optional[typing.Any] = None,
        ff: typing.Optional[typing.Any] = None,
        fz: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        fw: typing.Optional[typing.Any] = None,
        lts: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        ta: typing.Optional[typing.Any] = None,
        lh: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        fs: typing.Optional[typing.Any] = None,
        tt: typing.Optional[typing.Any] = None,
        td: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        w: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        miw: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        maw: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        h: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        mih: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        mah: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        bgsz: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        bgp: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        bgr: typing.Optional[typing.Any] = None,
        bga: typing.Optional[typing.Any] = None,
        pos: typing.Optional[typing.Any] = None,
        top: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        left: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        bottom: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        right: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        inset: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        display: typing.Optional[typing.Any] = None,
        flex: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        closeOnChange: typing.Optional[bool] = None,
        dropdownType: typing.Optional[Literal["popover", "modal"]] = None,
        popoverProps: typing.Optional["PopoverProps"] = None,
        modalProps: typing.Optional["ModalProps"] = None,
        clearable: typing.Optional[bool] = None,
        clearButtonProps: typing.Optional["ClearButtonProps"] = None,
        readOnly: typing.Optional[bool] = None,
        sortDates: typing.Optional[bool] = None,
        labelSeparator: typing.Optional[str] = None,
        placeholder: typing.Optional[str] = None,
        wrapperProps: typing.Optional[typing.Dict[typing.Union[str, float, int], typing.Any]] = None,
        leftSection: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        leftSectionWidth: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        leftSectionProps: typing.Optional[dict] = None,
        leftSectionPointerEvents: typing.Optional[Literal["-moz-initial", "inherit", "initial", "revert", "revert-layer", "unset", "auto", "none", "all", "fill", "painted", "stroke", "visible", "visibleFill", "visiblePainted", "visibleStroke"]] = None,
        rightSection: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        rightSectionWidth: typing.Optional[typing.Union[str, typing.Union[int, float, numbers.Number]]] = None,
        rightSectionProps: typing.Optional[dict] = None,
        rightSectionPointerEvents: typing.Optional[Literal["-moz-initial", "inherit", "initial", "revert", "revert-layer", "unset", "auto", "none", "all", "fill", "painted", "stroke", "visible", "visibleFill", "visiblePainted", "visibleStroke"]] = None,
        required: typing.Optional[bool] = None,
        radius: typing.Optional[typing.Union[typing.Union[int, float, numbers.Number]]] = None,
        disabled: typing.Optional[bool] = None,
        pointer: typing.Optional[bool] = None,
        withErrorStyles: typing.Optional[bool] = None,
        name: typing.Optional[str] = None,
        label: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        description: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        error: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        withAsterisk: typing.Optional[bool] = None,
        labelProps: typing.Optional[typing.Dict[typing.Union[str, float, int], typing.Any]] = None,
        descriptionProps: typing.Optional[typing.Dict[typing.Union[str, float, int], typing.Any]] = None,
        errorProps: typing.Optional[typing.Dict[typing.Union[str, float, int], typing.Any]] = None,
        inputWrapperOrder: typing.Optional[typing.Sequence[Literal["label", "description", "error", "input"]]] = None,
        maxLevel: typing.Optional[Literal["year", "decade"]] = None,
        level: typing.Optional[Literal["year", "decade"]] = None,
        type: typing.Optional[Literal["default", "multiple", "range"]] = None,
        value: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
        allowDeselect: typing.Optional[bool] = None,
        allowSingleDateInRange: typing.Optional[bool] = None,
        decadeLabelFormat: typing.Optional[str] = None,
        yearsListFormat: typing.Optional[str] = None,
        size: typing.Optional[Literal["xs", "sm", "md", "lg", "xl"]] = None,
        withCellSpacing: typing.Optional[bool] = None,
        minDate: typing.Optional[str] = None,
        maxDate: typing.Optional[str] = None,
        yearLabelFormat: typing.Optional[str] = None,
        monthsListFormat: typing.Optional[str] = None,
        numberOfColumns: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        columnsToScroll: typing.Optional[typing.Union[int, float, numbers.Number]] = None,
        ariaLabels: typing.Optional["AriaLabels"] = None,
        nextIcon: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        previousIcon: typing.Optional[typing.Union[str, int, float, ComponentType, typing.Sequence[typing.Union[str, int, float, ComponentType]]]] = None,
        nextLabel: typing.Optional[str] = None,
        previousLabel: typing.Optional[str] = None,
        hasNextLevel: typing.Optional[bool] = None,
        monthLabelFormat: typing.Optional[str] = None,
        firstDayOfWeek: typing.Optional[Literal[0, 1, 2, 3, 4, 5, 6]] = None,
        weekdayFormat: typing.Optional[str] = None,
        weekendDays: typing.Optional[typing.Sequence[Literal[0, 1, 2, 3, 4, 5, 6]]] = None,
        hideOutsideDates: typing.Optional[bool] = None,
        hideWeekdays: typing.Optional[bool] = None,
        classNames: typing.Optional[dict] = None,
        styles: typing.Optional[typing.Any] = None,
        unstyled: typing.Optional[bool] = None,
        variant: typing.Optional[str] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'allowDeselect', 'allowSingleDateInRange', 'aria-*', 'ariaLabels', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'className', 'classNames', 'clearButtonProps', 'clearable', 'closeOnChange', 'columnsToScroll', 'darkHidden', 'data-*', 'debounce', 'decadeLabelFormat', 'description', 'descriptionProps', 'disabled', 'disabledDates', 'display', 'dropdownType', 'error', 'errorProps', 'ff', 'firstDayOfWeek', 'flex', 'fs', 'fw', 'fz', 'h', 'hasNextLevel', 'hiddenFrom', 'hideOutsideDates', 'hideWeekdays', 'inputWrapperOrder', 'inset', 'label', 'labelProps', 'labelSeparator', 'left', 'leftSection', 'leftSectionPointerEvents', 'leftSectionProps', 'leftSectionWidth', 'level', 'lh', 'lightHidden', 'loading_state', 'lts', 'm', 'mah', 'maw', 'maxDate', 'maxLevel', 'mb', 'me', 'mih', 'minDate', 'miw', 'ml', 'mod', 'modalProps', 'monthLabelFormat', 'monthsListFormat', 'mr', 'ms', 'mt', 'mx', 'my', 'n_submit', 'name', 'nextIcon', 'nextLabel', 'numberOfColumns', 'opacity', 'p', 'pb', 'pe', 'persisted_props', 'persistence', 'persistence_type', 'pl', 'placeholder', 'pointer', 'popoverProps', 'pos', 'pr', 'previousIcon', 'previousLabel', 'ps', 'pt', 'px', 'py', 'radius', 'readOnly', 'required', 'right', 'rightSection', 'rightSectionPointerEvents', 'rightSectionProps', 'rightSectionWidth', 'size', 'sortDates', 'style', 'styles', 'ta', 'tabIndex', 'td', 'top', 'tt', 'type', 'unstyled', 'value', 'valueFormat', 'variant', 'visibleFrom', 'w', 'weekdayFormat', 'weekendDays', 'withAsterisk', 'withCellSpacing', 'withErrorStyles', 'wrapperProps', 'yearLabelFormat', 'yearsListFormat']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['id', 'allowDeselect', 'allowSingleDateInRange', 'aria-*', 'ariaLabels', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'className', 'classNames', 'clearButtonProps', 'clearable', 'closeOnChange', 'columnsToScroll', 'darkHidden', 'data-*', 'debounce', 'decadeLabelFormat', 'description', 'descriptionProps', 'disabled', 'disabledDates', 'display', 'dropdownType', 'error', 'errorProps', 'ff', 'firstDayOfWeek', 'flex', 'fs', 'fw', 'fz', 'h', 'hasNextLevel', 'hiddenFrom', 'hideOutsideDates', 'hideWeekdays', 'inputWrapperOrder', 'inset', 'label', 'labelProps', 'labelSeparator', 'left', 'leftSection', 'leftSectionPointerEvents', 'leftSectionProps', 'leftSectionWidth', 'level', 'lh', 'lightHidden', 'loading_state', 'lts', 'm', 'mah', 'maw', 'maxDate', 'maxLevel', 'mb', 'me', 'mih', 'minDate', 'miw', 'ml', 'mod', 'modalProps', 'monthLabelFormat', 'monthsListFormat', 'mr', 'ms', 'mt', 'mx', 'my', 'n_submit', 'name', 'nextIcon', 'nextLabel', 'numberOfColumns', 'opacity', 'p', 'pb', 'pe', 'persisted_props', 'persistence', 'persistence_type', 'pl', 'placeholder', 'pointer', 'popoverProps', 'pos', 'pr', 'previousIcon', 'previousLabel', 'ps', 'pt', 'px', 'py', 'radius', 'readOnly', 'required', 'right', 'rightSection', 'rightSectionPointerEvents', 'rightSectionProps', 'rightSectionWidth', 'size', 'sortDates', 'style', 'styles', 'ta', 'tabIndex', 'td', 'top', 'tt', 'type', 'unstyled', 'value', 'valueFormat', 'variant', 'visibleFrom', 'w', 'weekdayFormat', 'weekendDays', 'withAsterisk', 'withCellSpacing', 'withErrorStyles', 'wrapperProps', 'yearLabelFormat', 'yearsListFormat']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(MonthPickerInput, self).__init__(**args)
