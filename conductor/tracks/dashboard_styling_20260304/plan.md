# Implementation Plan: Refactor Dashboard Appearance and Page Styling

## Phase 1: Research and Global Styling [checkpoint: c7e7485]
- [x] Task: Analyze current Streamlit theme and page structure cac8405
- [x] Task: Define the "advanced look" theme in `.streamlit/config.toml` 3576278
- [x] Task: Create a central styling utility in `utils/ui.py` 23aef04
- [x] Task: Conductor - User Manual Verification 'Phase 1: Research and Global Styling' (Protocol in workflow.md) c7e7485

## Phase 2: Page-Specific Refactoring (TDD Applied) [checkpoint: f64c3db]
- [x] Task: Refactor Home page styling (`pages/1_Home.py`) c80b4b3
    - [x] Write tests for UI utility functions
    - [x] Apply styling to Home page
- [x] Task: Refactor Preditor page styling (`pages/2_Preditor.py`) 294119d
    - [x] Write tests for UI utility functions
    - [x] Apply styling to Preditor page
- [x] Task: Refactor Mapa page styling (`pages/3_Mapa.py`) a5aae3f
    - [x] Write tests for UI utility functions
    - [x] Apply styling to Mapa page
- [x] Task: Refactor EDA page styling (`pages/4_EDA.py`) 511ee23
    - [x] Write tests for UI utility functions
    - [x] Apply styling to EDA page
- [x] Task: Conductor - User Manual Verification 'Phase 2: Page-Specific Refactoring' (Protocol in workflow.md) f64c3db

## Phase 3: Final Polish and Verification
- [x] Task: Refine sidebar and navigation styling 67f2985
- [x] Task: Final cross-page consistency check 67f2985
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Final Polish and Verification' (Protocol in workflow.md)
