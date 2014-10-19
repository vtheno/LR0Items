all: LR0Items.py
	python3 LR0Items.py < input.txt

test: LR0Items.py
	python3 TestLR0Items.py < input.txt -v
