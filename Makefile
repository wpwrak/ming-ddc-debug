.PHONY:		all run poll

all:		build/top.bit

build/top.bit:	build.py
#		PYTHONPATH=$$PYTHONPATH:`pwd`/../milkymist-ng
		python3 ./build.py

run:		build/top.bit
		( echo cable milkymist; echo detect; \
		  echo pld load build/top.bit ) | jtag

poll:
		while sleep 1; do xrandr | grep DVI-1; done
