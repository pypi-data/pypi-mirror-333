# compas_grid

Model of simple grid structures for multi-storey buildings.

## Ubuntu Installation from Scratch

- **Download Installer**: Visit [www.anaconda.com](https://www.anaconda.com/products/distribution#download-section) to download `Anaconda3-2024.10-1-Linux-x86_64.sh`.
- **Run Installer**: Execute the installer with `bash Anaconda3-2024.10-1-Linux-x86_64.sh` and follow prompts.
- **Initialize Anaconda**: Run `source ~/.bashrc` and initialize with `conda init`.
- **Verify Installation**: Check Conda version with `conda --version`.
- **Update Conda**: Keep Conda updated using `conda update --all`.
- **Create Environment**: Use `conda create -n model -c conda-forge compas compas_viewer compas_occ compas_cgal python=3.9.10` to create a new environment.
- **Activate Environment**: Activate it with `conda activate model`.
- **Install Git**: `sudo apt install git -y`
- **Clone Model** go to you code directory `cd '/home/petras/code'`, then `git clone https://github.com/blockresearchgroup/compas_model` then, `cd  compas_model` then, `pip install -e .`
- **Clone Grid** go to you code directory `cd ..`, then `git clone https://github.com/BRG-research/compas_grid` then, `cd  compas_grid` then, `pip install -e .`
- **VS Code** open vscode set the environment with `CTRL+SHIFT+P` and `>Select: Python Interpreter`.
  
## Git Branch

For new features use other github branches.

To pull latest branch
```bash
git pull origin crea
```


## Commit style

```bash
git commit -m "DOC <description>"         <--- documentation related messages including readme
git commit -m "ADD <description>"         <--- for adding new elements
git commit -m "FIX <description>"         <--- for fixing (errors, typos)
git commit -m "FLASH <description>"       <--- quick checkpoint before refactoring
git commit -m "MILESTONE <description>"   <--- for capping moment in development
git commit -m "CAP <description>"         <--- for for less important milestones
git commit -m "UPDATE <description>"      <--- for moddification to the same file
git commit -m "MISC <description>"        <--- for any other reasons to be described
git commit -m "WIP <description>"         <--- for not finished work
git commit -m "REFACTOR <description>"    <--- for refactored code
git commit -m "MERGE <description>"       <--- for merging operations
git commit -m "WIP-CAP <description>"     <--- for when combining multiple commits into one
```

## Installation

Stable releases can be installed from PyPI.

```bash
pip install compas_grid
```

To install the latest version for development, do:

```bash
git clone https://github.com//compas_grid.git
cd compas_grid
pip install -e ".[dev]"
```

## Documentation

For further "getting started" instructions, a tutorial, examples, and an API reference,
please check out the online documentation here: [compas_grid docs](https://.github.io/compas_grid)

## Issue Tracker

If you find a bug or if you have a problem with running the code, please file an issue on the [Issue Tracker](https://github.com//compas_grid/issues).

