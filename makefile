# Virtual environment.
# 1. Get virtual environment name.
VENV_NAME := $(wildcard .venv_*)
# 2. Get kernel name from virtual-environment name (substitute '.' for '').
KERNEL_NAME := $(subst .,,$(VENV_NAME))
venv_get:
	scripts_shell/get_venv.sh

venv_remove:
	@echo "===removing virtual environment==="
	rm -rf $(VENV_NAME)
	@echo "===removing virtual iPython kernel==="
	rm -rf ~/Library/Jupyter/kernels/$(KERNEL_NAME)
