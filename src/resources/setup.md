## **uv : A Fast Python Management Setup**

**[Official Docs](https://docs.astral.sh/uv/getting-started/installation/)** `Click this link to install`

`uv` replaces standard tools (`pip`, `venv`, `virtualenv`) with a single, unified toolkit that is significantly faster.

---

### **Core Commands**

| Action | Command | Description |
| --- | --- | --- |
| **Add Library** | `uv add <package>` | Installs the package and adds it to `pyproject.toml`. |
| **View Graph** | `uv tree` | Visualizes the full dependency tree (parents & children). |
| **Restore** | `uv sync` | **The only command needed after cloning.** Installs everything from `uv.lock`. |
| **Run Script** | `uv run <script.py>` | Runs a script inside the managed environment automatically. |

---

### **Dependency Management Files**

* **`pyproject.toml` ( The "Wishlist" )**
* Lists the high-level packages you explicitly requested (e.g., `langchain`, `numpy`).
* This is the file you edit if you want to change project settings.


* **`uv.lock` ( The "Snapshot" )**
* Contains the **exact** version and hash of every single package installed (including transitive dependencies).
* Ensures that everyone working on the project has the exact same environment.



---

### **Generated File Hierarchy**

When you initialize and use `uv`, your project structure will look like this:

```text
my_project/
├── .venv/               # [Hidden] The actual virtual environment containing binaries/libs.
├── .python-version      # Pins the specific Python version (e.g., 3.12).
├── pyproject.toml       # User-defined dependencies.
├── uv.lock              # Machine-generated freeze of all dependencies.
└── src/                 # (Recommended) Your source code folder.
    └── main.py

```

---

### **Workflow for Cloning**

`uv sync`

This single command reads `uv.lock`, creates the `.venv`, and installs all locked dependencies to match the original environment perfectly.


## API Key Configuration

Create a `.env` file in your project directory:

```
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here
```

**⚠️ Important**: Never commit your `.env` file to GitHub! Add it to `.gitignore`