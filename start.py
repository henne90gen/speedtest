#!/usr/bin/python3

with open('run.sh', 'r') as f:
    content = f.read()

content = content.replace("exit 0", "#placeholder")

with open('run.sh', 'w') as f:
    f.write(content)

print("Speedtesting started")
