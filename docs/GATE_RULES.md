# StarkCore Gate Rules

## Purpose

This document defines the conditions used by StarkCore to accept or reject an evidence object.

The Gate does not determine absolute truth.

The Gate verifies whether an object satisfies declared rules.

---

## Verification Principle

A result is not accepted only because it exists.

Acceptance requires:

- Valid structure
- Required identity information
- Traceable events
- Executable process
- Available verification evidence

---

## Gate States

The Gate produces explicit outcomes:
---

## ALLOWED

An object is ALLOWED when:

- The required fields exist.
- The evidence structure is valid.
- The verification rules are satisfied.
- The execution history is consistent.

---

## DENIED

An object is DENIED when:

- Required evidence is missing.
- The schema is invalid.
- Identity information is incomplete.
- Verification conditions are not satisfied.

---

## FAILED

A FAILED state represents an execution problem.

A failure is preserved as evidence.

Example:
A failed event is not deleted.
It becomes part of the system history.

---

## Design Boundary

The Gate separates:

Existence
from
Acceptance

Failure
from
Deletion

Rule evaluation
from
Truth claims

---

## Goal

The purpose of the Gate is transparent verification.

Rules must be inspectable, reproducible, and auditable.
