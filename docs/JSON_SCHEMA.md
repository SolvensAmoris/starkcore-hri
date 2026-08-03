# StarkCore JSON Schema

## Purpose

This document defines the data structure used to exchange StarkCore evidence objects.

The schema provides a common format between different implementations.

---

## Evidence Object

A minimal evidence object contains:

{
  "claim": {},
  "identity": {},
  "events": [],
  "execution": {},
  "verification": {}
}

---

## Components

### Claim

Represents the statement or object being evaluated.

Example:

{
  "type": "paper",
  "content": "verifiable claim"
}

---

### Identity

Defines the canonical identity of the object.

Contains information required to distinguish the object through time.

---

### Events

A chronological record of transformations and actions.

Example:

[
  {
    "event": "created",
    "timestamp": 0
  },
  {
    "event": "executed",
    "result": "success"
  }
]

---

### Execution

Describes the process that produced a result.

Contains:

- executor
- inputs
- outputs
- status

---

### Verification

Contains the evidence required to evaluate the object.

Example:

{
  "status": "verified",
  "proof": {}
}

---

## Design Principle

The schema separates:

Existence
from
Verification

Data
from
Interpretation

Implementation
from
Evidence

This allows multiple implementations to share the same verification language.
