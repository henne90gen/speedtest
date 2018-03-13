#!/usr/bin/python3

with open('run.sh', 'r') as f:
    content = f.read()

content = content.replace("#placeholder", "exit 0")

with open('run.sh', 'w') as f:
    f.write(content)
