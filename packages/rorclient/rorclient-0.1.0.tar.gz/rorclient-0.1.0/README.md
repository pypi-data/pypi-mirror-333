# RORClient


[![Become a sponsor to ADernild](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/ADernild "Become a sponsor to ADernild")
[![GitHub](https://img.shields.io/github/followers/adernild?label=follow&style=social)](https://github.com/ADernild "Follow ADernild on GitHub")
[![LinkedIn](https://img.shields.io/badge/-LinkedInd-blue?style=flat-round&logo=Linkedin&logoColor=white&link=https://linkedin.com/in/alexander-dernild)](https://linkedin.com/in/alexander-dernild "Connect with me on LinkedIn")
[![Akami Cloud Computing](https://img.shields.io/badge/Cloud_Hosting-s?style=flat-round&logo=akamai&logoColor=%230096D6&labelColor=white&color=white)](https://www.linode.com/lp/refer/?r=a1236b8e74912ccb090628165fa6bf21cb52968f "Get a $100 credit on Linode Cloud")
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
[![httpx](https://img.shields.io/badge/httpx-%5E0.28.1-orange)](https://www.python-httpx.org/)
[![Python versions](https://img.shields.io/pypi/pyversions/httpx)](https://www.python.org/downloads/)

🚀 **A Python client for interacting with the ROR API.**
RORClient provides a simple, efficient way to query the [Research Organization Registry (ROR)](https://ror.org) API using **HTTPX** and **Pydantic**.

---

## 📖 Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Synchronous Client](#synchronous-client)
- [Asynchronous Client](#asynchronous-client)
- [Models](#models)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## ⚡ Installation
> ⚠ **Work in Progress**: RORClient is not yet available via PyPI.
> Clone the repository and install dependencies manually:

```sh
git clone https://github.com/ADernild/rorclient.git
cd rorclient
uv sync
```
---

## 🚀 Quick Start

### Synchronous Client
```python
from rorclient import RORClient

with RORClient() as client:
    # Get institution details
    org = client.get_institution("03yrm5c26")
    if org:
        print(f"Found institution: {org.name}")

    # Fetch multiple institutions
    multiple_orgs = client.get_multiple_institutions(["03yrm5c26", "029z82x56"])
    print(f"Fetched {len(multiple_orgs)} institutions")

```

### Asynchronous Client
```python
import asyncio
from rorclient import AsyncRORClient

async def main():
    async with AsyncRORClient() as client:
        # Get institution details
        org = await client.get_institution("03yrm5c26")
        if org:
            print(f"Found institution: {org.name}")

        # Fetch multiple institutions
        multiple_orgs = await client.get_multiple_institutions(["03yrm5c26", "029z82x56"])
        print(f"Fetched {len(multiple_orgs)} institutions")

asyncio.run(main())

```

---

## 🏛 Models
RORClient uses **Pydantic** models to structure API responses. The main model is `Institution`, which represents an organization in ROR.

Example usage:

```python
from rorclient import RORClient

client = RORClient()
org = client.get_institution("03yrm5c26")

if org:
    print(org.name)  # Stanford University
    print(org.external_ids)  # External identifiers like GRID, ISNI
    print(org.location.country)  # Country of the institution
```

For a full list of available fields, see the [institution.py](rorclient/models/institution.py) file.
You can also have a look at the [ROR API documentation](https://ror.readme.io/v2/docs/data-structure)

---

## 🧪 Testing

To run the test suite, run:

```sh
uv run pytest
```

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
