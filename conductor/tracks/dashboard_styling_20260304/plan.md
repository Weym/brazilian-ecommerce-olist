# Implementation Plan: Refactor Dashboard Appearance and Page Styling

## Phase 1: Research and Global Styling
- [ ] Task: Analyze current Streamlit theme and page structure
- [ ] Task: Define the "advanced look" theme in `.streamlit/config.toml`
- [ ] Task: Create a central styling utility in `utils/ui.py`
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Research and Global Styling' (Protocol in workflow.md)

## Phase 2: Page-Specific Refactoring (TDD Applied)
- [ ] Task: Refactor Home page styling (`pages/1_Home.py`)
    - [ ] Write tests for UI utility functions
    - [ ] Apply styling to Home page
- [ ] Task: Refactor Preditor page styling (`pages/2_Preditor.py`)
    - [ ] Write tests for UI utility functions
    - [ ] Apply styling to Preditor page
- [ ] Task: Refactor Mapa page styling (`pages/3_Mapa.py`)
    - [ ] Write tests for UI utility functions
    - [ ] Apply styling to Mapa page
- [ ] Task: Refactor EDA page styling (`pages/4_EDA.py`)
    - [ ] Write tests for UI utility functions
    - [ ] Apply styling to EDA page
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Page-Specific Refactoring' (Protocol in workflow.md)

## Phase 3: Final Polish and Verification
- [ ] Task: Refine sidebar and navigation styling
- [ ] Task: Final cross-page consistency check
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Final Polish and Verification' (Protocol in workflow.md)
