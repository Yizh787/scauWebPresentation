---
name: 四川农业大学在线考试系统
description: A focused, polished exam system with deliberate delight at key touchpoints
colors:
  forest: "#1a5c1a"
  canopy: "#2d8a2d"
  sprout: "#3da33d"
  sprout-glow: "rgba(45, 138, 45, 0.15)"
  sprout-tint: "#e8f8e8"
  error: "#e74c3c"
  error-tint: "#fde8e8"
  success: "#27ae60"
  warning: "#f39c12"
  ink: "#333333"
  ink-muted: "#666666"
  ink-light: "#999999"
  border: "#e0e0e0"
  surface: "#f8f9fa"
  surface-hover: "#e9ecef"
  canvas: "#f5f5f5"
  white: "#ffffff"
typography:
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif"
    fontSize: "14px"
    fontWeight: 500
    lineHeight: 1.4
  title:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif"
    fontSize: "18px"
    fontWeight: 600
    lineHeight: 1.3
  display:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif"
    fontSize: "24px"
    fontWeight: 600
    lineHeight: 1.2
rounded:
  sm: "8px"
  md: "12px"
  lg: "16px"
  pill: "20px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  xxl: "40px"
components:
  button-primary:
    backgroundColor: "linear-gradient(135deg, {colors.forest} 0%, {colors.canopy} 100%)"
    textColor: "{colors.white}"
    rounded: "{rounded.md}"
    padding: "14px 24px"
  button-primary-hover:
    backgroundColor: "{colors.canopy}"
    textColor: "{colors.white}"
  input:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "12px 15px"
  card:
    backgroundColor: "{colors.white}"
    rounded: "{rounded.lg}"
    padding: "20px"
  header:
    backgroundColor: "linear-gradient(135deg, {colors.forest} 0%, {colors.canopy} 100%)"
    textColor: "{colors.white}"
    padding: "15px 20px"
---

# Design System: 四川农业大学在线考试系统

## 1. Overview

**Creative North Star: "The Greenhouse"**

A living, contained space where knowledge grows. The greenhouse metaphor drives every choice: the green palette isn't decorative, it's the system's identity — the color of academic growth, of the campus itself. The space is warm but structured, alive but disciplined. Plants don't grow in chaos; they thrive in carefully designed environments.

This system rejects the template-default aesthetic: no Bootstrap-gray card stacks, no blue-primary autopilot, no identical rounded rectangles repeated without thought. It also rejects over-decoration — exam context demands restraint. The "wow" lives at deliberate touchpoints (login arrival, exam submission, score reveal), not on every hover. Everything else is calm, confident, and functional.

**Key Characteristics:**
- **Focused calm.** The exam interface stays out of the student's way. No animations during active exam-taking.
- **Polished surfaces.** Subtle shadows (not flat, not heavy), clean rounded corners (12–16px), smooth 200ms transitions on interactive elements.
- **Green as identity.** The university green carries 30–40% of the surface on key pages (header, primary actions), restrained to accents on content-heavy pages.
- **Dense when it matters.** Question banks, score tables, and exam lists pack information tightly. Don't pad with whitespace to look "designed."
- **One vocabulary.** Same buttons, same cards, same inputs, same spacing from login through admin dashboard.

## 2. Colors: The Forest Palette

A green-rooted palette drawn from the university's identity. Forest anchors the system, Canopy carries the primary actions, Sprout provides the lighter accents and glows. Neutrals stay clean and cool to let the green speak.

### Primary
- **Forest** (#1a5c1a): The deepest green. Used for the darkest gradient endpoints, heading accents, and high-emphasis text on light surfaces. This is the anchor — not a background, but a weight.
- **Canopy** (#2d8a2d): The working green. Primary button fills, focus borders, link text, active nav states. This is what the user touches most.
- **Sprout** (#3da33d): The lightest brand green. Gradient endpoints, hover glows, success-adjacent contexts. Used sparingly to lift without washing out.

### Accent
- **Sprout Glow** (rgba(45, 138, 45, 0.15)): Focus ring color on inputs and interactive elements. A soft halo that says "this is active" without shouting.
- **Sprout Tint** (#e8f8e8): Tag backgrounds, knowledge badges, subtle highlight surfaces. The lightest green touch.

### Semantic
- **Error** (#e74c3c): Form validation errors, failed exam scores, destructive action feedback. Always paired with Error Tint (#fde8e8) background.
- **Success** (#27ae60): Completed exam badges, pass indicators, confirmation messages.
- **Warning** (#f39c12): In-progress exam states, time-running-low indicators.

### Neutral
- **Ink** (#333333): Primary body text, headings, labels. Maximum readability.
- **Ink Muted** (#666666): Secondary text, descriptions, supporting information.
- **Ink Light** (#999999): Placeholder text, timestamps, metadata. Minimum contrast that still passes for normal text.
- **Border** (#e0e0e0): Input borders, dividers, card outlines. Visible but never heavy.
- **Surface** (#f8f9fa): Card backgrounds, list item backgrounds, secondary containers.
- **Surface Hover** (#e9ecef): Hover state for surface-colored elements.
- **Canvas** (#f5f5f5): Page-level background. The quietest neutral.
- **White** (#ffffff): Card backgrounds, input backgrounds, modal surfaces.

### Named Rules

**The Green Weight Rule.** Forest and Canopy are used for structural elements (header, primary buttons, focus states), not decorative flourishes. If a green element doesn't carry meaning (action, identity, state), remove it.

**The 30/10 Rule.** On identity-heavy pages (login, dashboard header), green carries ~30% of the visible surface. On content-heavy pages (exam lists, question banks), green drops to ~10% — accents only. The green breathes with the content density.

## 3. Typography

**Display Font:** System UI stack (PingFang SC on macOS, Microsoft YaHei on Windows, Segoe UI fallback)
**Body Font:** Same system stack

**Character:** Clean, contemporary, unpretentious. The system font stack is deliberate — it matches the user's OS, renders instantly (no FOUT), and feels native on every device. For a university exam system, trust and readability beat personality.

### Hierarchy
- **Display** (600, 24px, line-height 1.2): Page titles, dashboard headings, exam names. Used once per view maximum.
- **Title** (600, 18px, line-height 1.3): Section headings within cards, modal headers, form section labels.
- **Label** (500, 14px, line-height 1.4): Form labels, button text, navigation items, tab labels. The workhorse weight.
- **Body** (400, 14px, line-height 1.5): Paragraph text, descriptions, list content. Max line length 65–75ch for prose; data tables can run denser.
- **Caption** (400, 12px, line-height 1.4): Timestamps, metadata, helper text, secondary information.

### Named Rules

**The One Weight Rule.** Font-weight 500 (medium) is reserved for interactive elements: buttons, labels, nav items, tags. Non-interactive text stays at 400. Weight contrast carries meaning — it tells the user "this is tappable."

**The System Stack Doctrine.** No custom web fonts. The system stack loads instantly, renders crisply at every DPI, and supports CJK characters natively. A custom font would add latency and FOUT on a system where students may have slow connections during exams.

## 4. Elevation

The system uses a layered approach: surfaces rest on a flat canvas, with subtle shadows to lift interactive containers and modals above the content plane. Shadows are structural, not decorative — they communicate "this is a distinct, interactive surface."

### Shadow Vocabulary

- **Card lift** (`box-shadow: 0 2px 10px rgba(0,0,0,0.05)`): Default card shadow. Gentle, barely perceptible — just enough to separate the card from the canvas.
- **Card hover** (`box-shadow: 0 5px 20px rgba(45, 138, 45, 0.2)`): Admin card hover state. The green tint in the shadow ties the lift to the brand identity.
- **Modal backdrop** (`background: rgba(0,0,0,0.5)`): Full-screen overlay for modals. Not a shadow per se, but the elevation context for modal content.
- **Header shadow** (`box-shadow: 0 2px 10px rgba(0,0,0,0.1)`): Bottom shadow on the sticky header, creating a subtle separation from scrolling content.
- **Nav bar shadow** (`box-shadow: 0 -2px 10px rgba(0,0,0,0.1)`): Top shadow on the fixed bottom nav bar.

### Named Rules

**The Flat-By-Default Rule.** Surfaces are flat at rest. Shadows appear only as a response to interaction (hover, elevation, focus) or structural separation (header, nav). No decorative shadows on static content.

**The Green Tint Rule.** Hover shadows on brand-colored elements use a green-tinted shadow (`rgba(45, 138, 45, 0.2)`), not a neutral dark shadow. This ties the interaction feedback to the brand identity.

## 5. Components

### Buttons
- **Shape:** Gently curved (10px radius on standard buttons, 20px pill on compact action buttons like "开始考试").
- **Primary:** Green gradient fill (`linear-gradient(135deg, #1a5c1a 0%, #2d8a2d 100%)`), white text, 14px vertical padding. Full-width on forms, auto-width on inline actions.
- **Hover:** Subtle lift (`translateY(-2px)`) with green-tinted shadow (`0 10px 20px rgba(45, 138, 45, 0.4)`). 200ms ease-out transition.
- **Active:** Return to flat (`translateY(0)`), shadow removed. Press feedback.
- **Disabled:** Gray fill (#ccc), no lift, no shadow, `cursor: not-allowed`.
- **Secondary:** Light gray fill (#f0f0f0), muted text (#666). Used for cancel/dismiss actions.
- **Ghost (link-style):** No background, green text (#2d8a2d), underline on hover. Used for secondary navigation links.

### Cards / Containers
- **Corner Style:** Softly rounded (15px on student cards, 12px on admin cards).
- **Background:** White (#ffffff) on canvas (#f5f5f5) page background.
- **Shadow:** Card lift at rest, green-tinted shadow on hover (admin cards only).
- **Border:** None — shadow provides separation.
- **Internal Padding:** 20px standard, 25px on admin feature cards.
- **Content Density:** Cards pack content tightly. No excessive internal whitespace.

### Inputs / Fields
- **Style:** White background, 2px border (#e0e0e0), softly rounded (10px).
- **Focus:** Border shifts to Canopy (#2d8a2d) with a soft green glow ring (`0 0 0 3px rgba(45, 138, 45, 0.15)`). 300ms transition.
- **Placeholder:** Ink Light (#999999) — meets contrast requirements.
- **Label:** Positioned above input, Label typography (500, 14px), Ink color (#333).
- **Error:** Error red (#e74c3c) border and text, Error Tint background (#fde8e8).

### Navigation
- **Header:** Full-width sticky bar with green gradient background. Logo + title left, user info + logout right. White text throughout.
- **Bottom Nav (student):** Fixed bottom bar, white background, three tabs with emoji icons. Active state uses Canopy (#2d8a2d) text, inactive uses Ink Light (#999). Top shadow for separation.
- **Admin Nav:** Tab-based navigation within the dashboard. Same green active state.

### Chips / Tags
- **Style:** Sprout Tint background (#e8f8e8), Canopy text (#2d8a2d), pill-shaped (10px radius), compact padding (2px 8px).
- **Use:** Knowledge point tags, category labels, status indicators.

### Modal
- **Backdrop:** Semi-transparent dark overlay (rgba(0,0,0,0.5)).
- **Content:** White background, softly rounded (15px), max-width 500px, scrollable if content exceeds 80vh.
- **Header:** Flex row with title and close button, bottom border separator.
- **Close Button:** Circular (50% radius), light gray background (#f0f0f0), centered "×" symbol.

## 6. Do's and Don'ts

### Do:
- **Do** use the green gradient (`linear-gradient(135deg, #1a5c1a, #2d8a2d)`) for primary buttons and the header bar. This is the system's signature.
- **Do** maintain the 30/10 green density ratio: ~30% on identity pages (login, dashboard), ~10% on content pages (exam lists, question banks).
- **Do** use the system font stack. No custom web fonts — instant rendering and native CJK support matter more than typographic personality.
- **Do** provide hover feedback on every interactive element: lift + shadow on cards, border shift on inputs, color shift on links.
- **Do** use the Sprout Glow (`rgba(45, 138, 45, 0.15)`) for focus rings. Consistent focus language across all inputs.
- **Do** keep transitions at 200–300ms with ease-out timing. Fast enough to feel responsive, slow enough to notice.
- **Do** use Error Tint (#fde8e8) as background for error messages, not just red text on white.
- **Do** pack information densely in tables and lists. Don't pad with whitespace to look "designed."

### Don't:
- **Don't** use Bootstrap-default aesthetics: gray-white backgrounds, blue primary buttons, identical rounded cards stacked without thought. Per PRODUCT.md: "looks like a template, not a product."
- **Don't** add animations during active exam-taking. Per PRODUCT.md: "exam context demands restraint, not a party."
- **Don't** use oversized whitespace and huge fonts that make a feature-rich system look empty. Per PRODUCT.md: "show the work, don't pad with whitespace."
- **Don't** change the visual language between pages. Per PRODUCT.md: "one vocabulary, every screen."
- **Don't** ship interactive elements without hover/focus/active/disabled states. Per PRODUCT.md: "buttons with no hover feedback feels abandoned."
- **Don't** use `border-radius` above 16px on cards. Pill shape (20px+) is reserved for compact action buttons and tags only.
- **Don't** use green for decorative purposes (background patterns, decorative borders, illustration fills). Green carries meaning: identity, action, or state.
- **Don't** add bounce, elastic, or spring easing. Ease-out only. The system is calm, not playful.
- **Don't** use gradient text (`background-clip: text` with gradients). Solid color for all text.
- **Don't** add numbered section markers (01 / 02 / 03) as default scaffolding. Per PRODUCT.md anti-reference: "looks like a template."
