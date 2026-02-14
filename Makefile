PYTHON = python3
PROJECT_NAME = QuantPy

.PHONY = run clean test

run:
	@export PYTHONPATH=$${PYTHONPATH}:$(PWD)/src && $(PYTHON) -m src.$(PROJECT_NAME).backtesting.backtests.delta_hedging_backtest

clean:
	@echo "Cleaning everything in .gitignore"
	git clean -fdX