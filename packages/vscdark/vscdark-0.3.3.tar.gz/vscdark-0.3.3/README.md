# VSCDARK

This is a simple package to provide a matplotlib dark theme that fits well with the Visual Studio Code dark theme.
Additionally the package provides features to properly style interactive plots in notebooks.

## Usage

Two a `matplotlib` style and two functions are provided:

The style can be applied using matplotlib's `plt.style.use` function:
```python	
plt.style.use('vscdark.vscdark')
```

If styling for interactive plots is also desired, the provided `set_style` function should be used:

```python
def set_style(new_theme: str | None = None, dark: bool | None = None, display_css: bool = True, verbose: bool | None = None) -> None:
```

This function applies the current theme configuration and potentially changes options.

Arguments:
- `new_theme`: The name of the theme to apply. If `None`, the currently stored theme is reapplied. 
- `dark`: Only relevant for the interactive CSS. If `None`, the setting remains unchanged.
- `display_css`: Whether to `IPython.display` the `IPython.HTML` object that contains the CSS for widgets. It must be displayed somewhere in the notebook to take effect.
- `verbose`: If `True`, the css will contain "Widget CSS Active" to indicate that it is taken into account by the renderer. If `None`, the setting remains unchanged.

The `IPython.HTML` object containing the CSS can also directly be accessed using the `css` function:

```python
def css() -> IPython.HTML:
```