---
name: Legado a tu paso
colors:
  surface: '#fbf9f6'
  surface-dim: '#dbdad7'
  surface-bright: '#fbf9f6'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f3f0'
  surface-container: '#efeeeb'
  surface-container-high: '#eae8e5'
  surface-container-highest: '#e4e2df'
  on-surface: '#1b1c1a'
  on-surface-variant: '#45464c'
  inverse-surface: '#30312f'
  inverse-on-surface: '#f2f0ed'
  outline: '#76777d'
  outline-variant: '#c6c6cd'
  surface-tint: '#565e73'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#131b2d'
  on-primary-container: '#7c839a'
  inverse-primary: '#bec6df'
  secondary: '#825500'
  on-secondary: '#ffffff'
  secondary-container: '#fdbe63'
  on-secondary-container: '#754c00'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#00210c'
  on-tertiary-container: '#47935d'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe2fb'
  primary-fixed-dim: '#bec6df'
  on-primary-fixed: '#131b2d'
  on-primary-fixed-variant: '#3f465b'
  secondary-fixed: '#ffddb4'
  secondary-fixed-dim: '#fabb61'
  on-secondary-fixed: '#291800'
  on-secondary-fixed-variant: '#633f00'
  tertiary-fixed: '#a5f4b6'
  tertiary-fixed-dim: '#8ad89c'
  on-tertiary-fixed: '#00210c'
  on-tertiary-fixed-variant: '#005227'
  background: '#fbf9f6'
  on-background: '#1b1c1a'
  surface-variant: '#e4e2df'
typography:
  display:
    fontFamily: Source Serif 4
    fontSize: 44px
    fontWeight: '600'
    lineHeight: 52px
  display-mobile:
    fontFamily: Source Serif 4
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg:
    fontFamily: Source Serif 4
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Source Serif 4
    fontSize: 26px
    fontWeight: '600'
    lineHeight: 34px
  headline-md:
    fontFamily: Source Serif 4
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Source Serif 4
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Atkinson Hyperlegible Next
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Atkinson Hyperlegible Next
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-strong:
    fontFamily: Atkinson Hyperlegible Next
    fontSize: 16px
    fontWeight: '700'
    lineHeight: 24px
  label-lg:
    fontFamily: Atkinson Hyperlegible Next
    fontSize: 15px
    fontWeight: '700'
    lineHeight: 20px
  label-md:
    fontFamily: Atkinson Hyperlegible Next
    fontSize: 13px
    fontWeight: '700'
    lineHeight: 18px
  caption:
    fontFamily: Atkinson Hyperlegible Next
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 2.5rem
  margin-mobile: 1.25rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style
The brand personality is dignified, welcoming, deeply grounded in historical stewardship, and unapologetically functional. Designed for visitors with hearing impairments (hearing aid and cochlear implant users) exploring the monuments and museums of Segovia, the interface avoids clinical or paternalistic tropes. Instead, it balances civic cultural heritage with calm, high-efficiency cognitive processing.

The aesthetic blends **Editorial Heritage** with **Accessible Functionalism**. Tactile architectural cues evoke the granite ashlar masonry and Roman arches of Segovia without visual clutter. The emotional goal is quiet confidence: users should feel empowered, oriented, and free from cognitive fatigue when planning or executing visits across noisy, echoing monumental spaces.

## Colors
This design system employs a strict light-first color hierarchy engineered for WCAG 2.2 AAA text contrast against monumental cream backdrops.

- **Primary Canvas & Surfaces:** `#FAF8F5` provides a glare-free stone-cream foundation that reduces optical fatigue under harsh sunlight or dark museum interiors. Elevated cards rest on pure white `#FFFFFF` with structural boundary definition.
- **Ink & Structure:** `#0F1729` (Deep Navy) serves as the primary text, structural rule, and solid CTA fill, delivering a 14.8:1 contrast ratio against the canvas. Secondary text uses `#4A5568` (Slate Grey), achieving a minimum 7:1 ratio for body metadata.
- **Accents:** `#8A5A00` (Dark Amber) provides dignified focus highlights, historic callouts, and badge borders, supported by `#FDF1D6` for warm contextual containers.
- **Verification Status System (Strict Dual-Coding):**
  - *Verified Accessibility (Bucle magnético activo / Guías visuales):* `#1B6B3A` text/icon over `#EBF7EE` surface.
  - *Unverified / Community Reported:* `#4A5568` text/icon over `#EDF2F7` surface.
  - *Outdated / Known Issues (Dispositivo fuera de servicio):* `#9B2C2C` text/icon over `#FDE8E8` surface.
- **Keyboard & Focus Ring:** Dedicated double-ring outline composed of an inner 2px `#FFFFFF` spacer and an outer 3px `#0F1729` stroke to guarantee perceptibility over any background.

## Typography
Typographic selections directly address clarity under variable lighting and visual impairments. 

**Headlines:** *Source Serif 4* introduces historical gravity and monumental beauty, evoking Segovia's inscribed stone traditions without sacrificing x-height clarity. Serifs provide rhythmic reading comfort across historical introductions.

**Interface & Body:** *Atkinson Hyperlegible Next* guarantees disambiguation across commonly confused letterforms ('I', 'l', '1' and '0', 'O'), vital for reading technical specifications (e.g., "Telebobina T", "FM 863 MHz", "Sala 1"). 

Paragraph widths must never exceed 65 characters. All body text scales proportionally with user agent zoom without clipping containers.

## Layout & Spacing
The layout follows a fluid-responsive 12-column grid on desktop (max content boundary: 1200px) and a single-column stack on mobile devices.

- **Grid Architecture:** 
  - Desktop (>= 1024px): 12 columns, 1.5rem gutters, 2.5rem outer canvas margin.
  - Tablet (768px - 1023px): 8 columns, 1.25rem gutters, 2rem margin.
  - Mobile (< 768px): 4 columns / single vertical flow, 1rem gutters, 1.25rem margin.
- **Rhythm & Touch Margins:** A base 8px increment dictates all internal component padding. Minimum touch target boundaries are strictly preserved at `44x44px` across all interactive elements, with an explicit `8px` non-interactive buffer between adjacent actionable areas to eliminate mis-taps during movement.
- **Reflow Guarantees:** Horizontal scrolling is prohibited; interface layouts support text magnification up to 200% without breaking card layouts or overlapping metadata tags.

## Elevation & Depth
In alignment with accessible clarity, elevation avoids diffuse, indeterminate drop shadows that can create visual mud for users with low contrast sensitivity. 

Hierarchy is established via **structural boundaries and planar tinting**:
- **Layer 0 (Canvas):** Base background `#FAF8F5`.
- **Layer 1 (Cards & Modules):** Pure white `#FFFFFF` surface bordered by a crisp 1px solid stroke (`#0F1729` at 12% alpha). A subtle ambient offset (`0 2px 4px rgba(15, 23, 41, 0.05)`) grounds the element.
- **Layer 2 (Interactive Floating / Modals):** Pure white `#FFFFFF` backed by a definitive 2px solid border (`#0F1729`) and an elevated structural drop (`0 8px 24px rgba(15, 23, 41, 0.12)`).
- **Architectural Motif:** Key structural dividers, section breaks, and card headers incorporate a stylized subtle vector arc profile (64px wide, 16px high) inspired by the Roman arches of the Segovia Aqueduct. This appears as a single-color decorative stroke (`#0F1729` at 15% opacity), providing brand identity without competing with content.

## Shapes
A roundedness factor of `2` provides standard base radii of 12px (`0.75rem`) to 16px (`1rem`), mirroring the gentle curved vaults of Romanesque masonry found across Segovian cloisters and the Aqueduct arches.

- **Standard Cards & Containers:** 16px (`rounded-lg`) border radius.
- **Form Controls & Inputs:** 12px (`rounded-md`) border radius.
- **Badges, Status Chips & Interactive Tags:** 8px to 12px radius, avoiding full pill shapes to maintain sufficient corner real estate for dual-coded indicators (icon + text).
- **Interactive Focus States:** Focus rings follow the exact contour of the element radius, offset by 3px.

## Components

### Buttons
- **Primary:** Filled `#0F1729` with `#FFFFFF` text. Minimum height `48px` (touch-safe). Border-radius `12px`. Hover shifts to `#1E293B`; active state adds an inset border. Focus state renders a 3px outer outline in `#8A5A00` with 2px canvas separation.
- **Secondary:** Transparent fill with a 2px `#0F1729` solid stroke and `#0F1729` text. Hover shifts to `#FAF8F5` background.
- **Accessibility Feature Button (Audio/Loop Presets):** Solid `#FDF1D6` background with `#8A5A00` text and 1.5px `#8A5A00` border, featuring a dedicated left-aligned hearing aid/cochlear loop SVG glyph.

### Verification Chips & Badges
Badges communicate status through compulsory **dual coding** (stroke/fill paired with unambiguous text and an explicit SVG icon; never color alone):
- **Verificado (Verified):** Green forest `#1B6B3A` text, `#EBF7EE` background, 1px `#1B6B3A` border. Prepended with a checkmark-in-shield SVG.
- **Sin verificar (Unverified):** Grey slate `#4A5568` text, `#EDF2F7` background, 1px `#4A5568` border. Prepended with an information-circle SVG.
- **Desfasado (Outdated/Reported):** Brick red `#9B2C2C` text, `#FDE8E8` background, 1.5px `#9B2C2C` border. Prepended with an alert-triangle SVG.

### Cards (Monuments & Venues)
Built on Layer 1 `#FFFFFF` with 16px radius and 1px border (`#0F1729` at 12%). 
- Structured internal layout: Top banner with monumental photo or architectural arch watermark, followed by monument name in `headline-md`, verified acoustic status badge group, acoustic metrics summary (e.g., "Reverberación: Alta", "Bucle Magnético: Disponible"), and explicit CTA button.
- Card hover elevates the outline to 2px solid `#0F1729`.

### Input Fields & Controls
- **Text Inputs:** Minimum height `48px`, background `#FFFFFF`, border 2px `#4A5568` at rest, upgrading to 2px `#0F1729` on focus. Placeholder text in `#4A5568` with 4.5:1 minimum contrast.
- **Checkboxes & Radios:** Hit targets of `44x44px` enclosing a `24x24px` visual box with a 2px stroke in `#0F1729`. Check indicators use bold, geometric SVG checkmarks in `#FFFFFF` over `#0F1729` active fill.

### Specialized Accessibility Components
- **Acoustic Profile Matrix:** An informational card pattern displaying reverberation ratings, ambient noise index (dB estimations during peak hours), and certified hearing-loop locations inside Segovian stone structures (e.g., Alcázar chapel, Cathedral nave).
- **Visual Transcript Drawer:** Persistent expandable panel with high-contrast text and copy-to-clipboard support for audio-guide content.
- **Iconography Standard:** SVG line weights fixed at 2px matching typography stems. Geometric, unshaded, and paired with explicit `aria-label` or visible text.