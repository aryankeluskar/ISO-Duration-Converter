import sys

import pip

package = "fastapi pymongo uvicorn[standard]"
if package not in sys.modules:
    pip.main(["install", package])

# Code for those who run the code directly from func+f5 instead of
# terminal and install the required packages for Python
