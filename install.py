import pip
import sys
package = 'fastapi uvicorn[standard]'
if not package in sys.modules:
    pip.main(['install', package])

# Code for those who run the code directly from func+f5 instead of terminal