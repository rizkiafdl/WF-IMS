# Frontend Style Guide — WF-IMS
> Extracted from Figma Design System (node `22:1257`, file `jsEY5udLBSS9jGVykESsvk`)
> Stack: Flask + Jinja2 — implement as CSS custom properties + plain CSS classes

---

## 1. Color Palette

### Primary — Forest Green (`#2D6A4F`)
Used for: primary buttons, active nav items, key actions, positive status badges

```css
--color-primary-900: #1a3d2e;
--color-primary-800: #1f4d39;
--color-primary-700: #245c43;
--color-primary-600: #2D6A4F;   /* BASE */
--color-primary-500: #3a8a66;
--color-primary-400: #52a880;
--color-primary-300: #7cc4a0;
--color-primary-200: #a8dbbf;
--color-primary-100: #d4eedf;
--color-primary-50:  #edf7f2;
```

### Secondary — Slate (`#475569`)
Used for: secondary buttons, body text, table headers, neutral UI chrome

```css
--color-secondary-900: #0f172a;
--color-secondary-800: #1e293b;
--color-secondary-700: #334155;
--color-secondary-600: #475569;  /* BASE */
--color-secondary-500: #64748b;
--color-secondary-400: #94a3b8;
--color-secondary-300: #cbd5e1;
--color-secondary-200: #e2e8f0;
--color-secondary-100: #f1f5f9;
--color-secondary-50:  #f8fafc;
```

### Tertiary — Amber (`#D97706`)
Used for: warning badges, pending status, highlights, tertiary actions

```css
--color-tertiary-900: #78350f;
--color-tertiary-800: #92400e;
--color-tertiary-700: #b45309;
--color-tertiary-600: #D97706;   /* BASE */
--color-tertiary-500: #f59e0b;
--color-tertiary-400: #fbbf24;
--color-tertiary-300: #fcd34d;
--color-tertiary-200: #fde68a;
--color-tertiary-100: #fef3c7;
--color-tertiary-50:  #fffbeb;
```

### Neutral — Blue-Gray (`#6474BB`)
Used for: info badges, links, secondary highlights, chart accents

```css
--color-neutral-900: #1e2a5e;
--color-neutral-800: #2d3a7a;
--color-neutral-700: #4050a0;
--color-neutral-600: #6474BB;    /* BASE */
--color-neutral-500: #7b8fd0;
--color-neutral-400: #9daade;
--color-neutral-300: #bec7eb;
--color-neutral-200: #dde2f4;
--color-neutral-100: #eef0f9;
--color-neutral-50:  #f6f7fd;
```

### Semantic Colors (derived)
```css
--color-success:      var(--color-primary-600);    /* #2D6A4F */
--color-warning:      var(--color-tertiary-600);   /* #D97706 */
--color-danger:       #dc2626;
--color-info:         var(--color-neutral-600);    /* #6474BB */
--color-bg-page:      #f0f4f8;   /* light blue-gray page background */
--color-bg-card:      #ffffff;
--color-bg-sidebar:   var(--color-secondary-800);  /* #1e293b */
--color-text-primary: var(--color-secondary-800);  /* #1e293b */
--color-text-muted:   var(--color-secondary-500);  /* #64748b */
--color-border:       var(--color-secondary-200);  /* #e2e8f0 */
```

---

## 2. Typography

**Font**: Inter (Google Fonts)
**Import**: `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">`

```css
--font-family-base: 'Inter', sans-serif;
```

### Type Scale

| Token | Size | Weight | Letter Spacing | Usage |
|-------|------|--------|----------------|-------|
| `--text-display` | 36px | 700 (Bold) | -0.72px (-2%) | Page heroes, large numbers |
| `--text-h1` | 24px | 600 (SemiBold) | -0.48px (-2%) | Page titles |
| `--text-h2` | 20px | 500 (Medium) | -0.40px (-2%) | Section headings |
| `--text-h3` | 16px | 500 (Medium) | -0.32px (-2%) | Card headings, labels |
| `--text-p1` | 14px | 400 (Regular) | 0 | Body text, table rows |
| `--text-p2` | 12px | 400 (Regular) | 0 | Secondary text, captions |
| `--text-p3` | 10px | 400 (Regular) | 0 | Micro labels, timestamps |

```css
/* CSS custom properties */
--text-display-size: 36px;   --text-display-weight: 700;  --text-display-tracking: -0.72px;
--text-h1-size: 24px;        --text-h1-weight: 600;       --text-h1-tracking: -0.48px;
--text-h2-size: 20px;        --text-h2-weight: 500;       --text-h2-tracking: -0.40px;
--text-h3-size: 16px;        --text-h3-weight: 500;       --text-h3-tracking: -0.32px;
--text-p1-size: 14px;        --text-p1-weight: 400;       --text-p1-tracking: 0;
--text-p2-size: 12px;        --text-p2-weight: 400;       --text-p2-tracking: 0;
--text-p3-size: 10px;        --text-p3-weight: 400;       --text-p3-tracking: 0;
```

---

## 3. Buttons

Four variants extracted from Design System screenshot:

| Variant | Background | Text | Border | Use for |
|---------|-----------|------|--------|---------|
| `btn-primary` | `#2D6A4F` | white | none | Main actions (Save, Submit, Approve) |
| `btn-secondary` | white | `#475569` | `#475569` | Secondary actions (Cancel, Back) |
| `btn-inverted` | `#1e293b` | white | none | Destructive or dark-context actions |
| `btn-outlined` | transparent | `#2D6A4F` | `#2D6A4F` | Tertiary actions, less emphasis |

```css
.btn {
  font-family: var(--font-family-base);
  font-size: var(--text-p1-size);
  font-weight: 500;
  border-radius: 8px;
  padding: 10px 20px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  border: 1.5px solid transparent;
  transition: opacity 0.15s;
}
.btn-primary  { background: var(--color-primary-600); color: #fff; }
.btn-secondary { background: #fff; color: var(--color-secondary-600); border-color: var(--color-secondary-400); }
.btn-inverted  { background: var(--color-secondary-800); color: #fff; }
.btn-outlined  { background: transparent; color: var(--color-primary-600); border-color: var(--color-primary-600); }
.btn:hover { opacity: 0.88; }
.btn:disabled { opacity: 0.45; cursor: not-allowed; }
```

---

## 4. Status Badges / Labels

| Status | Color | Background |
|--------|-------|-----------|
| Approved / Available / Passed | `#2D6A4F` | `#edf7f2` |
| Pending / Draft / In Progress | `#D97706` | `#fffbeb` |
| Rejected / Failed / Danger | `#dc2626` | `#fef2f2` |
| Info / Neutral | `#6474BB` | `#f6f7fd` |
| Completed / Closed | `#475569` | `#f1f5f9` |

```css
.badge {
  font-size: var(--text-p3-size);
  font-weight: 500;
  padding: 3px 10px;
  border-radius: 999px;
  display: inline-block;
}
.badge-success  { color: #2D6A4F; background: #edf7f2; }
.badge-warning  { color: #D97706; background: #fffbeb; }
.badge-danger   { color: #dc2626; background: #fef2f2; }
.badge-info     { color: #6474BB; background: #f6f7fd; }
.badge-neutral  { color: #475569; background: #f1f5f9; }
```

---

## 5. Layout

### Page Structure
```
┌─────────────────────────────────────────────┐
│  Navbar (64px height, full width)            │
├───────────────┬─────────────────────────────┤
│  Sidebar      │  Main Content               │
│  (260px)      │  (flex-1, padding 24px)     │
│               │                             │
└───────────────┴─────────────────────────────┘
```

```css
/* Page skeleton */
.layout-wrapper  { display: flex; flex-direction: column; min-height: 100vh; }
.layout-body     { display: flex; flex: 1; }
.sidebar         { width: 260px; min-height: 100%; background: var(--color-bg-sidebar); flex-shrink: 0; }
.main-content    { flex: 1; padding: 24px; background: var(--color-bg-page); }
.navbar          { height: 64px; background: #fff; border-bottom: 1px solid var(--color-border); }
```

### Card
```css
.card {
  background: var(--color-bg-card);
  border-radius: 12px;
  padding: 20px 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.07);
}
```

### Spacing Scale (8px base)
```css
--space-1: 4px;   --space-2: 8px;   --space-3: 12px;  --space-4: 16px;
--space-5: 20px;  --space-6: 24px;  --space-8: 32px;  --space-10: 40px;
--space-12: 48px; --space-16: 64px;
```

---

## 6. Forms & Inputs

```css
.form-input, .form-select, .form-textarea {
  font-family: var(--font-family-base);
  font-size: var(--text-p1-size);
  color: var(--color-text-primary);
  background: #fff;
  border: 1.5px solid var(--color-border);
  border-radius: 8px;
  padding: 10px 14px;
  width: 100%;
  transition: border-color 0.15s;
}
.form-input:focus {
  outline: none;
  border-color: var(--color-primary-600);
  box-shadow: 0 0 0 3px rgba(45,106,79,0.12);
}
.form-label {
  font-size: var(--text-p2-size);
  font-weight: 500;
  color: var(--color-text-primary);
  margin-bottom: 6px;
  display: block;
}
```

---

## 7. Tables

```css
.table { width: 100%; border-collapse: collapse; font-size: var(--text-p1-size); }
.table th {
  background: var(--color-secondary-50);
  color: var(--color-text-muted);
  font-weight: 500;
  font-size: var(--text-p2-size);
  text-align: left;
  padding: 10px 16px;
  border-bottom: 1px solid var(--color-border);
}
.table td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-primary);
  vertical-align: middle;
}
.table tr:last-child td { border-bottom: none; }
.table tr:hover td { background: var(--color-secondary-50); }
```

---

## 8. Jinja2 Base Template Pattern

```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}WF-IMS{% endblock %}</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/tokens.css') }}">
  <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
  {% block extra_css %}{% endblock %}
</head>
<body>
  <div class="layout-wrapper">
    {% include 'partials/navbar.html' %}
    <div class="layout-body">
      {% include 'partials/sidebar.html' %}
      <main class="main-content">
        {% block content %}{% endblock %}
      </main>
    </div>
  </div>
</body>
</html>
```

---

## 9. File Structure (CSS)

```
static/css/
├── tokens.css     ← all CSS custom properties (colors, type, spacing)
├── base.css       ← reset, body, html defaults
├── layout.css     ← sidebar, navbar, main-content
├── components.css ← btn, badge, card, table, form
└── main.css       ← imports all of the above in order
```

---

## 10. DO / DON'T

| DO | DON'T |
|----|-------|
| Use CSS custom properties for all color/size values | Hardcode hex values in templates |
| Use `.badge-*` classes for all status displays | Use raw `<span style="color:...">` |
| Use `card` wrapper for all content sections | Nest content directly in `main-content` |
| Use Inter font at defined weights only (400/500/600/700) | Use font-weight 300 or 800 |
| Keep Jinja2 templates focused on structure | Put business logic in templates |
