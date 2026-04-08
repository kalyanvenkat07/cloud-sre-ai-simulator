name: cloud-sre-openenv
description: Advanced SRE incident simulation environment
version: 1.0

entrypoint: app.py

observation_space:
  services: dict
  incidents: list
  metrics: dict
  steps: int

action_space:
  command: string
  target: string

reward:
  type: float
  range: [-1.0, 1.0]
