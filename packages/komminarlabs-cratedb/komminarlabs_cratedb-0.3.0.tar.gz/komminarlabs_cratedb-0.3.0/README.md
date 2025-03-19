# CrateDB Resource Provider

The CrateDB Resource Provider lets you manage [CrateDB](https://cratedb.com/database/) resources.

## Installing

This package is available for several languages/platforms:

### Node.js (JavaScript/TypeScript)

To use from JavaScript or TypeScript in Node.js, install using either `npm`:

```bash
npm install @komminarlabs/cratedb
```

or `yarn`:

```bash
yarn add @komminarlabs/cratedb
```

### Python

To use from Python, install using `pip`:

```bash
pip install komminarlabs-cratedb
```

### Go

To use from Go, use `go get` to grab the latest version of the library:

```bash
go get github.com/komminarlabs/pulumi-cratedb/sdk/go/...
```

### .NET

To use from .NET, install using `dotnet add package`:

```bash
dotnet add package KomminarLabs.CrateDB
```

## Configuration

The following configuration points are available for the `cratedb` provider:

- `cratedb:api_key` (environment: `CRATEDB_API_KEY`) - The API key
- `cratedb:api_secret` (environment: `CRATEDB_API_SECRET`) - The API secret
- `cratedb:url` (environment: `CRATEDB_URL`) - The CrateDB Cloud URL

## Reference

For detailed reference documentation, please visit [the Pulumi registry](https://www.pulumi.com/registry/packages/cratedb/api-docs/).
