# Specification: Refactor Dashboard Appearance and Page Styling

## Goal
Improve the visual appeal and "advanced look" of the Streamlit dashboard by applying custom styling and layout refinements, without altering the existing data visualizations or core functionality.

## Scope
- Global CSS injection for consistent branding and layout.
- Custom sidebar styling (logo, navigation, footer).
- Page-specific styling for Home, Preditor, Mapa, and EDA.
- Improved typography and spacing.
- Responsive design considerations for various screen sizes.

## Technical Approach
- Use `st.markdown(unsafe_allow_html=True)` to inject custom CSS.
- Utilize Streamlit's `config.toml` for theme settings (colors, fonts).
- Create a reusable styling module in `utils/styles.py` (or similar).
- Maintain existing graph logic and data flows.

## Acceptance Criteria
- Dashboard has a modern, professional, and "advanced" aesthetic.
- Branding is consistent across all pages.
- Sidebar is visually enhanced.
- No regression in existing graph functionality or data interactivity.
- Code follows project style guides and TDD principles where applicable.
