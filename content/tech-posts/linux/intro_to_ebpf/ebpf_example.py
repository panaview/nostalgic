
# Code taken from "Introduction to eBPF" video
# https://www.youtube.com/watch?v=clxOil-rars

from bcc import BPF
from bcc.utils import printb

BPF_SOURCE_CODE = r"""
TRACEPOINT_PROBE(syscalls, sys_enter_mkdir) {
    bpf_trace_printk("New directory created: %s\n", args->pathname);
    return 0;
}
"""

bpf = BPF (text = BPF_SOURCE_CODE)

print("Catching any syscall for directory creation..")

while True:
    try:
        (task,pid,cpu,flags,ts,msg) = bpf.trace_fields()
        printb(b"%-18.9f %-16s %-6d %s" % (ts, task, pid, msg))
    except ValueError:
        continue
    except KeyboardInterrupt:
        break
