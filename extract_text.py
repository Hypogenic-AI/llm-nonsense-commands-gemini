
import textract
import sys

try:
    text = textract.process("papers/2310.15140v2_AutoDAN.pdf")
    print(text.decode('utf-8'))
except Exception as e:
    print(f"An error occurred: {e}", file=sys.stderr)
    sys.exit(1)
