# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within StatefulPy, please send an email to security@statefulpy.org. All security vulnerabilities will be promptly addressed.

Please do not publicly disclose the issue until it has been addressed by the maintainers.

## Security Considerations

### Pickle Serializer

StatefulPy includes a pickle serializer which is not safe against malicious data. Only use the pickle serializer with trusted data and when security is not a concern.

For public-facing applications or when loading untrusted data, use the JSON serializer instead:

```python
@stateful(backend="sqlite", db_path="state.db", serializer="json")
def my_function():
    # Your function code...
```

### Data Storage

StatefulPy does not encrypt stored data. Sensitive information stored in function state will be saved in cleartext (for JSON serializer) or pickle format. Do not store sensitive data (passwords, API tokens, etc.) in function state.

# Security Considerations for StatefulPy

## Serialization

- **Pickle Serializer:**  
  The default pickle serializer offers good performance but is not secure against untrusted input.
  **Recommendation:** Use the JSON serializer (or implement a custom serializer) for applications where data is coming from untrusted sources.

## Concurrency

- Ensure that your backend (SQLite or Redis) and the stateful decorator are used according to the guidelines.
- The decorator acquires locks before loading and updating state to minimize race conditions.
- For SQLite, file locks (using portalocker) are in place. If you experience issues under heavy concurrency,
  consider reviewing your system and file lock configurations.

## CLI Usage

- The CLI commands have been updated to catch migration errors. Review error messages carefully and ensure that
  both the source and target backends are available.

For further questions or contributions, please read through CONTRIBUTING.md and the project documentation.
