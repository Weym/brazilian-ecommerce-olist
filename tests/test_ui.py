import unittest
from unittest.mock import patch
from utils.ui import apply_global_css, add_sidebar_branding

class TestUI(unittest.TestCase):
    @patch("streamlit.markdown")
    def test_apply_global_css_calls_markdown(self, mock_markdown):
        """Should call st.markdown with unsafe_allow_html=True"""
        apply_global_css()
        mock_markdown.assert_called()
        args, kwargs = mock_markdown.call_args
        self.assertTrue(kwargs.get("unsafe_allow_html"))
        self.assertIn("<style>", args[0])

    @patch("streamlit.sidebar")
    def test_add_sidebar_branding_calls_sidebar(self, mock_sidebar):
        """Should use st.sidebar to add branding elements"""
        # Note: sidebar components like markdown/title are attributes of sidebar
        add_sidebar_branding()
        mock_sidebar.markdown.assert_called()

if __name__ == "__main__":
    unittest.main()
