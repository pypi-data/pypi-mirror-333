
# safethread/thread/__init__.py

"""
This module provides classes and utilities for thread synchronization, as well as thread-safe data structures to be used in concurrent programming scenarios.

### **Classes:**
- **SafeDict**: A thread-safe dictionary implementation.
- **SafeList**: A thread-safe list implementation.
- **SafeQueue**: A thread-safe queue implementation.
- **SafeSet**: A thread-safe set implementation.
- **SafeTuple**: A thread-safe tuple implementation.
"""

from .SafeBaseObj import SafeBaseObj
from .SafeDict import SafeDict
from .SafeList import SafeList
from .SafeTuple import SafeTuple
from .SafeSet import SafeSet
from .SafeQueue import SafeQueue
