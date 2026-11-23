# Theme & Color Mode Customization Guide

Your portfolio includes a built-in dark/light theme switcher. This guide explains how it works and how to customize it.

## Features

✨ **Dark & Light Modes** - Switch between themes with a single click
🎨 **Custom Color Palettes** - Fully customizable color schemes for each theme
💾 **Persistent Preference** - Theme choice is saved to localStorage
🖥️ **System Preference Detection** - Defaults to your OS theme preference
⚡ **Instant Switching** - No page reload required

## How to Use

### For Visitors

Click the sun/moon icon in the navigation bar:
- 🌙 **Moon icon** = Currently in light mode (click to switch to dark)
- ☀️ **Sun icon** = Currently in dark mode (click to switch to light)

### For Developers

The theme system uses CSS custom properties (variables) that automatically update when the theme changes.

## Architecture

### 1. Theme Context (`frontend/src/context/ThemeContext.tsx`)

Manages theme state and persistence:

```typescript
const { theme, toggleTheme } = useTheme()
// theme: 'dark' | 'light'
// toggleTheme: () => void
```

### 2. CSS Variables (`frontend/src/styles/variables.css`)

All colors are defined as CSS custom properties:

```css
:root {
  /* Dark theme (default) */
  --color-primary: #0A0E27;
  --color-secondary: #6366F1;
  --color-accent: #10B981;
  /* ... more colors */
}

[data-theme="light"] {
  /* Light theme overrides */
  --color-primary: #FFFFFF;
  --color-secondary: #4F46E5;
  --color-accent: #059669;
  /* ... more colors */
}
```

### 3. Theme Toggle Button (`frontend/src/components/Navbar/Navbar.tsx`)

The navbar includes the theme toggle button with animated icons.

## Customizing Colors

### Option 1: Edit Variables (Recommended)

Edit `frontend/src/styles/variables.css`:

```css
:root {
  /* Dark Theme - Your custom colors here */
  --color-primary: #1a1a2e;        /* Background */
  --color-secondary: #0f3460;      /* Brand color */
  --color-accent: #16db65;         /* Accent/highlights */
  --color-text: #eaeaea;           /* Main text */
  --color-text-muted: #a0a0a0;     /* Secondary text */
  /* ... */
}

[data-theme="light"] {
  /* Light Theme - Your custom colors here */
  --color-primary: #f8f9fa;
  --color-secondary: #0f3460;
  --color-accent: #16db65;
  --color-text: #212529;
  --color-text-muted: #6c757d;
  /* ... */
}
```

### Option 2: Add More Themes

You can add additional theme variants:

```css
/* Add to variables.css */
[data-theme="midnight"] {
  --color-primary: #000000;
  --color-secondary: #1e90ff;
  --color-accent: #ffd700;
  /* ... */
}

[data-theme="ocean"] {
  --color-primary: #001f3f;
  --color-secondary: #0074D9;
  --color-accent: #7FDBFF;
  /* ... */
}
```

Then update `ThemeContext.tsx`:

```typescript
type Theme = 'dark' | 'light' | 'midnight' | 'ocean'

// Add a cycle function instead of toggle:
const cycleTheme = () => {
  const themes: Theme[] = ['dark', 'light', 'midnight', 'ocean']
  const currentIndex = themes.indexOf(theme)
  const nextIndex = (currentIndex + 1) % themes.length
  setTheme(themes[nextIndex])
}
```

## Color Palette Reference

### Dark Theme (Default)

| Variable | Color | Usage |
|----------|-------|-------|
| `--color-primary` | `#0A0E27` | Main background |
| `--color-secondary` | `#6366F1` | Brand/accent color (indigo) |
| `--color-accent` | `#10B981` | Success/highlights (green) |
| `--color-background` | `#0F1117` | Page background |
| `--color-surface` | `#1A1D29` | Cards, elevated surfaces |
| `--color-text` | `#E2E8F0` | Primary text |
| `--color-text-muted` | `#94A3B8` | Secondary text |
| `--color-border` | `#2D3548` | Borders, dividers |

### Light Theme

| Variable | Color | Usage |
|----------|-------|-------|
| `--color-primary` | `#FFFFFF` | Main background |
| `--color-secondary` | `#4F46E5` | Brand/accent color |
| `--color-accent` | `#059669` | Success/highlights |
| `--color-background` | `#F1F5F9` | Page background |
| `--color-surface` | `#FFFFFF` | Cards, elevated surfaces |
| `--color-text` | `#0F172A` | Primary text |
| `--color-text-muted` | `#475569` | Secondary text |
| `--color-border` | `#CBD5E1` | Borders, dividers |

## Using Theme Colors in Components

### In CSS/Module CSS

```css
.myComponent {
  background: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.myComponent:hover {
  border-color: var(--color-secondary);
  box-shadow: var(--shadow-glow);
}
```

### In Inline Styles (React)

```tsx
<div style={{
  background: 'var(--color-surface)',
  color: 'var(--color-text)',
  padding: 'var(--spacing-4)',
  borderRadius: 'var(--radius-lg)'
}}>
  Content here
</div>
```

### Accessing Current Theme in JavaScript

```tsx
import { useTheme } from './context/ThemeContext'

function MyComponent() {
  const { theme, toggleTheme } = useTheme()
  
  return (
    <div>
      <p>Current theme: {theme}</p>
      <button onClick={toggleTheme}>Toggle Theme</button>
    </div>
  )
}
```

## Gradients

Pre-defined gradients that adapt to the theme:

```css
/* Available gradients */
background: var(--gradient-primary);  /* Indigo to purple */
background: var(--gradient-accent);   /* Green to teal */
background: var(--gradient-dark);     /* Dark background gradient */
```

## Shadows & Effects

Theme-aware shadows:

```css
.card {
  box-shadow: var(--shadow-lg);      /* Standard shadow */
}

.button:hover {
  box-shadow: var(--shadow-glow);    /* Glowing effect (brand color) */
}

.badge {
  box-shadow: var(--shadow-glow-accent);  /* Green glow */
}
```

## Best Practices

### ✅ Do:
- Use CSS custom properties for all colors
- Test both themes when making changes
- Ensure sufficient contrast for accessibility (WCAG AA minimum)
- Use semantic variable names (`--color-text` not `--color-gray`)

### ❌ Don't:
- Hardcode color values in components
- Use colors that don't work in both themes
- Forget to update both theme variants
- Use extremely low contrast combinations

## Accessibility

Ensure your color choices meet WCAG guidelines:

- **Normal text**: Contrast ratio of at least 4.5:1
- **Large text** (18pt+): Contrast ratio of at least 3:1
- **Interactive elements**: Clear visual indicators

Test your colors: https://webaim.org/resources/contrastchecker/

## Advanced: Theme Transition Animations

Add smooth transitions when switching themes:

```css
/* Add to global.css */
* {
  transition: background-color 0.3s ease, 
              color 0.3s ease, 
              border-color 0.3s ease;
}
```

## Exporting Theme Preferences

Users can export their theme preference:

```typescript
// In ThemeContext
const exportThemePreference = () => {
  return {
    theme,
    timestamp: new Date().toISOString()
  }
}
```

## Troubleshooting

### Theme not persisting after refresh
- Check browser localStorage isn't disabled
- Verify ThemeProvider is wrapping your App
- Check for JavaScript errors in console

### Colors not updating
- Make sure you're using CSS variables (`var(--color-name)`)
- Check for hardcoded colors overriding variables
- Clear browser cache

### Flash of unstyled content (FOUC)
- The theme is set via `data-theme` attribute on `<html>`
- Initial theme is loaded from localStorage before render
- If needed, add a `<style>` tag in `index.html` with critical theme CSS

## Future Enhancements

Consider adding:
- 🎨 Theme preview before switching
- 🌈 More theme variants (midnight, ocean, forest, etc.)
- ⚙️ Custom color picker for users
- 📱 Theme sync across devices
- 🎯 Per-section theme overrides
- ⏰ Auto-switch based on time of day

## Need Help?

- Check the browser console for errors
- Verify `data-theme` attribute on `<html>` element
- Inspect CSS variables in browser DevTools
- Test with default colors first before customizing
