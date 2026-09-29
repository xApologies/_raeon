# QMO catalog tooling

[Read-only query command](query-cycle1.mjs) exposes the actual imported Cycle-1 data; [examples and SQL](../../data/qmo/README.md). Requires Node 24 or newer. Queries never regenerate objects or run gameplay.

`cycle1_reference/` preserves exact original API, closure, render, Blender/Metal and source-test files. Their original relative paths refer to the archived package layout. They are reference snapshots, not active runtime modules; use the normalized query tool for the repository layout. [File mappings](../../provenance/sources/cycle1-originals/file-mappings.json) locate every original member.

The 16 original source tests were run against the intact extracted source package. The new [integrity validator](../validators/validate-cycle1-import.mjs) verifies the normalized files against those original archive members and cross-checks JSON, atlas and SQLite without executing generation scripts.
