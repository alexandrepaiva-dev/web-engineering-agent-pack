# Node CPU and memory

For CPU issues use CPU profiling/flame evidence.

For memory issues inspect heap growth, retained objects, buffers, caches and resource lifecycle.

Distinguish leak from legitimate high working set.

Check event-loop delay for blocking work.

Do not fix memory pressure by blindly increasing limits.
