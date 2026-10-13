"""
Master Excel Update Automation — Streamlit entrypoint.

Run with:
    streamlit run app.py
"""

import importlib
import master_update_automation.app

importlib.reload(master_update_automation.app)
from master_update_automation.app import main

if __name__ == "__main__":
    main()

