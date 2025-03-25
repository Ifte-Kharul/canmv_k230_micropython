import sys
import gc

def get_platform_info():
    """Provides platform and CPU architecture info (assumptions for K230)."""
    print("MicroPython Platform:", sys.platform)
#    print("Platform: CanMV K230 (RISC-V 64-bit)")
#    print("CPU: Dual-core RISC-V (1.6GHz + 800MHz)")
#    print("RAM: 1GB/2GB LPDDR4 (Check board specifications)")

def get_memory_info():
    """Displays available heap memory."""
    print("Free Memory (bytes):", gc.mem_free())

# Example usage:
get_platform_info()
get_memory_info()
