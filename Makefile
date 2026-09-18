.PHONY: help score
help:
	@echo "Run: python runner/run_benchmark.py --model YOUR_MODEL --suite all --vision"
	@echo "Score: python scoring/score_results.py results/*.json"
score:
	python scoring/score_results.py $(RESULTS)
