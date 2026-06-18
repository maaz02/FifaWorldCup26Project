---
name: Elite Analytics
colors:
  surface: '#0d1322'
  surface-dim: '#0d1322'
  surface-bright: '#33394a'
  surface-container-lowest: '#080e1d'
  surface-container-low: '#151b2b'
  surface-container: '#191f2f'
  surface-container-high: '#242a3a'
  surface-container-highest: '#2f3445'
  on-surface: '#dde2f8'
  on-surface-variant: '#bdc8d1'
  inverse-surface: '#dde2f8'
  inverse-on-surface: '#2a3040'
  outline: '#87929a'
  outline-variant: '#3e484f'
  surface-tint: '#7bd0ff'
  primary: '#8ed5ff'
  on-primary: '#00354a'
  primary-container: '#38bdf8'
  on-primary-container: '#004965'
  inverse-primary: '#00668a'
  secondary: '#ffe083'
  on-secondary: '#3c2f00'
  secondary-container: '#eec200'
  on-secondary-container: '#645000'
  tertiary: '#c2cde5'
  on-tertiary: '#263143'
  tertiary-container: '#a7b2c9'
  on-tertiary-container: '#394458'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#c4e7ff'
  primary-fixed-dim: '#7bd0ff'
  on-primary-fixed: '#001e2c'
  on-primary-fixed-variant: '#004c69'
  secondary-fixed: '#ffe083'
  secondary-fixed-dim: '#eec200'
  on-secondary-fixed: '#231b00'
  on-secondary-fixed-variant: '#574500'
  tertiary-fixed: '#d8e3fb'
  tertiary-fixed-dim: '#bcc7de'
  on-tertiary-fixed: '#111c2d'
  on-tertiary-fixed-variant: '#3c475a'
  background: '#0d1322'
  on-background: '#dde2f8'
  surface-variant: '#2f3445'
typography:
  display-lg:
    fontFamily: Sora
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Sora
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Sora
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.05em
  metric-mono:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-padding-desktop: 40px
  container-padding-mobile: 20px
  gutter: 24px
  card-gap: 16px
---

## Brand & Style
The design system is engineered for a high-performance sports analytics platform, specifically tailored for the World Cup '26 AI Predictor. The visual language balances professional-grade data density with an energetic, futuristic aesthetic.

The style is **Corporate / Modern** infused with **Glassmorphism**. It utilizes deep, atmospheric backgrounds to provide a canvas for vibrant, neon-accented data visualizations. The emotional response is one of precision, authority, and technological advancement, catering to users who demand both aesthetic polish and analytical depth.

## Colors
The palette is rooted in a **Deep Navy (#0B1120)** foundation to ensure maximum contrast for data visualization. 

- **Primary (Electric Blue):** Used for interactive elements, primary CTAs, and active data states.
- **Secondary (Bright Gold):** Reserved for "Golden Moments," win probabilities, and trophy-related metrics.
- **Surface (Slate):** Backgrounds for cards and containers to create depth against the deep navy base.
- **Functional Colors:** Use standard semantic reds for "Loss" or "Critical" data, but prioritize the Electric Blue and Gold for the primary analytical narrative.

## Typography
The typography system uses a tiered approach to balance character and readability. 

- **Sora** provides a geometric, futuristic feel for headlines and hero metrics, reinforcing the "AI" aspect of the platform.
- **Inter** serves as the workhorse for all body copy and UI controls, ensuring legibility at high data densities.
- **JetBrains Mono** is introduced for secondary metrics and technical labels to emphasize the "Predictor" and algorithmic nature of the data.

All headlines should favor a tight letter-spacing to maintain a "bold" and "compact" appearance.

## Layout & Spacing
The layout employs a **12-column fluid grid** for desktop, collapsing to a single column for mobile. 

The spacing rhythm is based on an **8px linear scale**. Use wide margins (40px+) on desktop to allow the glassmorphic cards to "breathe" against the navy background. Data tables should use a "compact" vertical rhythm (8px or 12px cell padding) to maximize information density without sacrificing horizontal scanability. Breakpoints are set at 768px (Tablet) and 1280px (Desktop).

## Elevation & Depth
Depth is created through **Glassmorphism** and **Tonal Layering** rather than traditional shadows.

1.  **Level 0 (Base):** The Deep Navy (#0B1120) floor.
2.  **Level 1 (Cards):** Slate (#1E293B) at 60% opacity with a 12px backdrop blur and a 1px border (#F8FAFC, 10% opacity) to define edges.
3.  **Level 2 (Overlays/Modals):** Slate (#1E293B) at 80% opacity with a 24px backdrop blur and a subtle 1px primary-color glow at the top edge.

Avoid drop shadows; instead, use low-opacity inner borders to simulate light catching the edge of a physical glass pane.

## Shapes
This design system uses a **Rounded (Level 2)** shape language. 

Standard components (buttons, input fields) use a 0.5rem (8px) radius. Larger layout containers and cards use a 1rem (16px) radius. This softening of the "technical" typography and color palette makes the platform feel modern and approachable rather than cold or overly industrial. 

Circular elements are reserved specifically for **Progress Indicators** and **Team Crests** to create a distinct visual contrast from the rectangular grid.

## Components

### Buttons
- **Primary:** Solid Electric Blue with white text. Use a slight outer glow on hover.
- **Secondary:** Ghost style with an Electric Blue border and text.
- **Tertiary:** Slate background with white text, used for low-priority actions.

### Cards
Cards are the primary container. They must feature a subtle translucent background (Glassmorphism) and a 1px border. On hover, the border opacity should increase, and the primary accent color should appear as a 2px top-accent line.

### Data Tables
Clean, borderless rows with a faint Slate separator. The header row should use `label-caps` typography. Use the Primary color for the "key" metric in each row (e.g., predicted score).

### Circular Progress Indicators
Used for AI confidence scores and win probabilities. Use a thick stroke (8px+) for the "track" and the Gold accent color for the "progress" to highlight peak performance metrics.

### Inputs & Selection
- **Inputs:** Dark Slate background with a focus state that transitions the border to Electric Blue.
- **Chips:** Small, pill-shaped tags used for "Match Status" (e.g., Live, Final).
- **Checkboxes/Radios:** Custom circular styles using the Primary color for the active state.