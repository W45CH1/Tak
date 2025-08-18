import io
import sys

output_buffer = io.StringIO()
real_buffers = sys.stdout, sys.stderr
sys.stdout, sys.stderr = output_buffer, output_buffer
print("foo")
sys.stdout, sys.stderr = real_buffers
print("done")
print(output_buffer.getvalue())

print("done2")
