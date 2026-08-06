# Contributing to NexusAI OS

Thank you for your interest in contributing to NexusAI OS!

## Workflow Guidelines

1. **Fork the Repository**: Create your personal fork on GitHub.
2. **Create a Feature Branch**: `git checkout -b feat/my-new-feature`
3. **Run Unit Tests**: Ensure all existing tests pass:
   ```bash
   pytest tests/ -v
   ```
4. **Submit a Pull Request**: Provide a detailed description of changes, rationale, and test results.

## Code Style & Standards
- Python code should conform to **PEP 8** standards.
- All new async functions must include explicit return type hints.
- Write pytest test cases for every new feature or bug fix.
