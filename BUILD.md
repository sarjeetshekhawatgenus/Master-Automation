# Building MasterAutomation Windows Executable (.exe)

This guide documents how the MasterAutomation Streamlit application is packaged into a standalone Windows desktop executable (`.exe`).

---

## 1. Architecture Overview

Streamlit applications are web services by design. Packaging them as a desktop `.exe` requires:
1. **Desktop Launcher (`launcher.py`)**:
   - Calls `multiprocessing.freeze_support()` at the very top (mandatory on Windows to prevent infinite process spawn loops / fork bombs).
   - Dynamically binds an available local TCP port (defaulting to `8501`).
   - Automatically opens the user's default web browser to `http://localhost:<port>`.
   - Boots the Streamlit engine in-process using `streamlit.web.bootstrap.run()` without spawning external CLI subprocesses.
2. **PyInstaller Spec (`MasterAutomation.spec`)**:
   - Gathers all Streamlit static assets (JavaScript bundles, CSS, Material Symbols web fonts).
   - Bundles the application package (`master_update_automation`), configuration (`.streamlit`), and templates.
   - Collects runtime dependencies (`pandas`, `openpyxl`, `uvicorn`, `starlette`).
3. **One-Click Build Script (`build.bat`)**:
   - Verifies the Python and PyInstaller environment.
   - Cleans previous artifacts and executes the spec build.

---

## 2. Building the Executable

To build the executable at any time:

### Option A: Double-Click `build.bat`
Simply double-click [`build.bat`](build.bat) in the project root.

### Option B: Command Line
```powershell
python -m PyInstaller --noconfirm --clean MasterAutomation.spec
```

The resulting standalone application will be located in:
```text
dist\MasterAutomation\
├── MasterAutomation.exe    <-- Main desktop executable
└── _internal\              <-- Python runtime, DLLs, and Streamlit assets
```

---

## 3. Running the Desktop Application

### Method 1: Compiled Executable (`.exe`)
Run `dist\MasterAutomation\MasterAutomation.exe`.
- Starts the embedded server.
- Opens your browser automatically to the modern UI.
- All dependencies, Python runtime, and assets are self-contained.

### Method 2: Instant 1-Click Runner (`MasterAutomation.bat`)
Double-click [`MasterAutomation.bat`](MasterAutomation.bat) in the project root.
- Runs directly on systems with Python installed without compiling.

---

## 4. Distributing to Other Users

To share the application with non-technical users on other Windows PCs:
1. Open the `dist` directory.
2. Right-click the `MasterAutomation` folder → **Compress to ZIP file**.
3. Name it `MasterAutomation-v3.4.1-Windows.zip`.
4. The recipient simply extracts the ZIP file and double-clicks `MasterAutomation.exe`. Python does **not** need to be installed on their PC.

---

## 5. Security & Windows App Control (WDAC / Smart App Control)

On enterprise-managed Windows PCs with **Windows Defender Application Control (WDAC)** or **Smart App Control** enabled in strict mode (`UsermodeCodeIntegrityPolicyEnforcementStatus: 2`), unsigned `.exe` binaries created in user folders may be blocked by policy:
- **For local use**: Double-click [`MasterAutomation.bat`](MasterAutomation.bat), which executes via the system-approved Python interpreter.
- **For enterprise deployment**: Sign `MasterAutomation.exe` using your organization's Code Signing Certificate via `signtool.exe`, or place it in an IT-approved folder (e.g., `C:\Program Files\MasterAutomation\`).
