# Technical Design Document: Enhanced HTTP Error Handling for Fewsats SDK

## Overview

The Fewsats SDK currently returns a raw `httpx.Response` object for every request, which forces users to call `.json()` to extract data. While this works for traditional Python developers, it becomes cumbersome when integrating with AI agents and LLMs (Large Language Models) that prefer structured data directly.

Previously, we processed responses internally so that client methods returned a dictionary. This is more ergonomic for programmers and especially beneficial for AI agents. However, error handling remains problematic: when an HTTP error (e.g., 422 Unprocessable Entity) occurs, `response.raise_for_status()` raises an exception without exposing detailed information (such as which fields are missing), which is essential for both debugging and automated recovery by LLMs.

## Problem Statement

- **Current Behavior:**  
  Client methods return an `httpx.Response` object. Errors are signaled via exceptions that lack important details from the response body.

- **Desired Behavior:**  
  - **On success:** Return the parsed JSON data as a dictionary.
  - **On error:** Provide an exception that contains the typical error message, along with extra details (like the error JSON payload), so that both developers and AI agents can handle the error effectively.

- **Challenge:**  
  Incorporating try/except logic to safely extract error details complicates the implementation. We need a solution that:
  - Fits naturally with Python's exception-based error flow.
  - Delivers detailed error information needed for effective LLM (tool) integrations.

## Evaluated Approaches

### Option 1: Enhanced Exception in `_request`

**Concept:**  
Wrap the HTTP call in a try/except block. On a successful request, parse and return the JSON data directly. On failure, catch the HTTP error, attempt to extract error details via `.json()`, and then re-raise a custom exception (`FewsatsHTTPError`) that includes this payload.

**Example Implementation:**
```python
class FewsatsHTTPError(HTTPError):
    def __init__(self, msg, payload=None):
        super().__init__(msg); self.payload = payload

@patch
def _request(self: Fewsats, method: str, path: str, **kwargs) -> dict:
    url = f"{self.base_url}/{path}"
    r = self._httpx_client.request(method, url, **kwargs)
    try: r.raise_for_status()
    except HTTPError as e:
        try: err = r.json()
        except Exception: err = None
        raise FewsatsHTTPError(str(e), payload=err) from None
    return r.json()
```

**Pros:**
- Maintains the standard exception flow expected by Python developers.
- Provides detailed error information through the custom exception's `payload`.

**Cons:**
- Increases complexity within the `_request` method.
- Requires familiarity with the custom exception for proper error handling.

### Option 2: Composite Response

**Concept:**  
Instead of raising exceptions for errors, always return a structured dictionary with keys like `{"ok": bool, "data": <parsed JSON or None>, "error": <error details or None>}`. This structure explicitly communicates status and error details.

**Example Implementation:**
```python
@patch
def _request(self: Fewsats, method: str, path: str, **kwargs) -> dict:
    url = f"{self.base_url}/{path}"
    r = self._httpx_client.request(method, url, **kwargs)
    try:
        r.raise_for_status(); d = r.json()
    except HTTPError as e:
        try: err = r.json()
        except Exception: err = str(e)
        return {"ok": False, "data": None, "error": err}
    return {"ok": True, "data": d, "error": None}
```

**Pros:**
- Offers a uniform return type.
- Simplifies integration with AI agents that can directly inspect the composite structure.

**Cons:**
- Deviates from conventional Python error handling (exceptions are not raised).
- Risks masking errors in interactive development (e.g., in notebooks) where immediate exception feedback is preferred.

### Option 3: Leave Things As They Are

**Concept:**  
Continue returning the raw `httpx.Response` object without internal processing. Traditional Python developers manually call `.json()` and handle errors using standard methods. For AI agent integrations, offer a separate response processing method or utility that converts the raw response into a structured dictionary—exposing the error details if necessary.

**Approach for LLMs:**  
- Create a dedicated utility function to process the raw response.
- This function would check for errors, extract detailed error information, and then return a structured dictionary suitable for LLM consumption.

**Pros:**
- Preserves the well-understood behavior for traditional developers.
- It may be too early to decide on a unified error handling flow, which allows the library to remain at a lower level. In the future, when additional features (e.g., Sherlock integration) are implemented, the interface can be clarified.

**Cons:**
- Shifts the responsibility of error parsing onto the developer.
- May lead to inconsistent error handling.
- If people start building on the Python SDK, they might encounter breaking changes as the interface evolves.

## Recommendation

We propose adopting **Option 1: Enhanced Exception in `_request`** as the primary error handling strategy for general development. This approach:
- Returns parsed JSON data on success.
- Raises a custom exception (`FewsatsHTTPError`) containing both error messages and detailed error payloads on failure.

At the same time, **Option 2 (Composite Response)** remains available for scenarios where a uniform return structure is preferable for AI agent integrations. For now, **Option 4 (Leave Things As They Are)** is recognized as a fallback for those who prefer to handle HTTP responses directly. Although this offers the flexibility of a lower-level interface, it comes with the risk of future breaking changes if early users build dependencies on the current behavior.


## Conclusion

This document outlines three strategies for enhanced error handling in the Fewsats SDK—each with its own advantages and trade-offs. Enhancing exception-based error reporting (Option 1) provides a clear, standard Python interface by returning parsed JSON on success and detailed error information on failure. Option 2 offers a uniform composite response for easier LLM integration, while Option 3 retains the current low-level behavior for those who prefer it, albeit with the risk of future interface changes. We invite the team to review these options and reach a consensus on the most appropriate solution.

