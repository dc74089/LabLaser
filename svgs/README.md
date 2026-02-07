# SVG Templates Directory

Place your SVG template files in this directory. They will be automatically loaded when the application starts (PyInstaller builds only).

## Template Syntax

Use Django template variables in your SVG files:
- `{{ data.0 }}` - First customization field
- `{{ data.1 }}` - Second customization field
- `{{ data.2 }}` - Third customization field
- And so on...

## Example SVG Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg width="100mm" height="50mm" viewBox="0 0 100 50" xmlns="http://www.w3.org/2000/svg">
  <!-- Guest Name -->
  <text x="50" y="20" text-anchor="middle" font-size="8" fill="black">
    {{ data.0 }}
  </text>

  <!-- Message Line 1 -->
  <text x="50" y="30" text-anchor="middle" font-size="5" fill="black">
    {{ data.1 }}
  </text>

  <!-- Message Line 2 -->
  <text x="50" y="35" text-anchor="middle" font-size="5" fill="black">
    {{ data.2 }}
  </text>
</svg>
```

## How It Works

1. **Save SVG files** in this directory with `.svg` extension
2. **Use template tags** like `{{ data.0 }}`, `{{ data.1 }}`, etc.
3. **Run the .exe** - Templates are automatically imported
4. **File name** becomes the template name (e.g., `badge.svg` → "badge")
5. **Slot count** is automatically detected from the highest `{{ data.X }}` number

## Notes

- Template names are based on the filename (without .svg extension)
- If a template with the same name already exists, it will be skipped
- The number of customization fields is automatically detected
- Only runs when launching from the PyInstaller executable (not during development)
