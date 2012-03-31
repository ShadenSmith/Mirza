CXX = g++
DEBUG = -DDEBUG

virtualmachine: virtualmachine.cpp opset.h
	$(CXX) virtualmachine.cpp -o virtualmachine

debug: virtualmachine.cpp opset.h
	$(CXX) $(DEBUG) virtualmachine.cpp -o virtualmachine

clean:
	rm -f virtualmachine

