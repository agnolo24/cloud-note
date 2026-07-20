# Lerna Monorepo Setup Guide

This guide describes how to initialize and configure a monorepo for the **Shope Management System** using [Lerna](https://lerna.js.org/) and npm workspaces.

---

## Step-by-Step Setup

### Step 1: Initialize the Root Node Project
Initialize a root-level `package.json` to manage workspaces and project-wide devDependencies.
```bash
npm init -y
```

Make the root package private to prevent it from being accidentally published:
Edit the root `package.json` and ensure it has:
```json
{
  "name": "shope-management-system",
  "private": true,
  "workspaces": [
    "packages/*"
  ]
}
```

---

### Step 2: Initialize Lerna
Run the Lerna initialization command. This installs `lerna` as a development dependency and generates a default configuration file.
```bash
npx lerna@latest init
```

This will automatically create/update:
1. `lerna.json` - Lerna configuration file.
2. `packages/` - Directory where your individual packages (e.g., frontend, backend, shared libraries) will live.
3. Dev dependencies in `package.json`.

---

### Step 3: Configure `lerna.json`
Verify that `lerna.json` is configured to use npm workspaces. Open `lerna.json` and ensure it looks like this:
```json
{
  "$schema": "node_modules/lerna/schemas/lerna-schema.json",
  "version": "0.0.0",
  "useWorkspaces": true
}
```

---

### Step 4: Create Monorepo Packages
You can place your sub-projects inside the `packages/` directory. For example, let's create a backend package (`api`) and a frontend package (`web`):

```bash
mkdir -p packages/api packages/web
```

Inside each subdirectory, initialize a basic package:
```bash
# Initialize packages/api
cd packages/api && npm init -y

# Initialize packages/web
cd packages/web && npm init -y
```

Ensure each package has a unique name in its `package.json`, e.g., `"name": "@shope/api"` and `"name": "@shope/web"`.

---

### Step 5: Install Dependencies across Packages
With npm workspaces, you can manage all dependencies from the root directory:

- To install a dependency for a specific package (e.g., `express` to `@shope/api`):
  ```bash
  npm install express -w @shope/api
  ```
- To run a script in a specific package:
  ```bash
  npm run dev -w @shope/web
  ```

---

### Step 6: Using Lerna Commands
Here are the essential Lerna commands to manage the repository:

- **Run scripts in all packages concurrently**:
  ```bash
  npx lerna run <script-name>
  ```
- **List all packages**:
  ```bash
  npx lerna list
  ```
- **Version and Publish packages** (handles Git tagging and semver updates):
  ```bash
  npx lerna publish
  ```
