# How to Connect PostgreSQL with NestJS Using Drizzle ORM

> A complete step-by-step guide based on the **shope-management-system** project.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Install Packages](#2-install-packages)
3. [Project Folder Structure](#3-project-folder-structure)
4. [Configure the `.env` File](#4-configure-the-env-file)
5. [Create the Drizzle Config (`drizzle.config.ts`)](#5-create-the-drizzle-config)
6. [Define the Database Schema](#6-define-the-database-schema)
7. [Create the Database Module (NestJS Provider)](#7-create-the-database-module)
8. [Register the Database Module in AppModule](#8-register-the-database-module-in-appmodule)
9. [Auto-Run Migrations on Startup (`main.ts`)](#9-auto-run-migrations-on-startup)
10. [Generate & Run Migrations](#10-generate--run-migrations)
11. [Inject Drizzle into Any Service (CRUD Examples)](#11-inject-drizzle-into-any-service)
12. [Bonus: Zod Validation Pipe](#12-bonus-zod-validation-pipe)
13. [Quick Reference Cheat Sheet](#13-quick-reference-cheat-sheet)

---

## 1. Prerequisites

Before starting, make sure you have:

- **Node.js** (v18+)
- **PostgreSQL** installed and running
- A **NestJS project** created with `npx @nestjs/cli new <project-name>`
- A PostgreSQL **database already created** (e.g., `shope_management`)

```bash
# Create a database using psql
psql -U postgres
CREATE DATABASE shope_management;
\q
```

---

## 2. Install Packages

### Production dependencies

```bash
npm i drizzle-orm pg
```

| Package       | Purpose                                     |
| ------------- | ------------------------------------------- |
| `drizzle-orm` | The ORM — query builder, schema, migrations |
| `pg`          | Node.js PostgreSQL driver (node-postgres)   |

### Dev dependencies

```bash
npm i -D drizzle-kit @types/pg dotenv
```

| Package     | Purpose                                        |
| ----------- | ---------------------------------------------- |
| `drizzle-kit` | CLI tool for generating & running migrations |
| `@types/pg`   | TypeScript type definitions for `pg`         |
| `dotenv`      | Loads `.env` variables (used in drizzle config)|

### Also install NestJS Config module (if not already installed)

```bash
npm i @nestjs/config
```

This lets NestJS read `.env` variables via `ConfigService`.

---

## 3. Project Folder Structure

After completing this setup, your project should look like this:

```
api/
├── .env                           ← DB connection string
├── drizzle.config.ts              ← Drizzle Kit configuration
├── database/
│   ├── drizzle/
│   │   └── schema.ts              ← All table definitions
│   └── migrations/                ← Auto-generated SQL migration files
│       ├── 0000_initial.sql
│       ├── 0001_some_change.sql
│       └── meta/
├── src/
│   ├── main.ts                    ← App bootstrap + auto-migrate
│   ├── app.module.ts              ← Root module (imports ConfigModule + DatabaseModule)
│   ├── database/
│   │   └── database.module.ts     ← Drizzle provider (creates the DB connection)
│   ├── common/
│   │   └── pipes/
│   │       └── zod-validation.pipe.ts
│   └── <feature-modules>/
│       ├── <feature>.module.ts
│       ├── <feature>.controller.ts
│       ├── <feature>.service.ts   ← Injects DRIZZLE here
│       └── dto/
│           └── <feature>.dto.ts   ← Zod schemas
├── package.json
└── tsconfig.json
```

> [!IMPORTANT]
> The `database/` folder (containing `drizzle/schema.ts` and `migrations/`) lives **outside** `src/`.
> This is intentional — `drizzle-kit` runs outside the NestJS compilation context, so the schema
> must be accessible as a plain TypeScript file from the project root.

---

## 4. Configure the `.env` File

Create a `.env` file in the project root (`api/.env`):

```env
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
```

**Example:**

```env
DATABASE_URL=postgresql://postgres:agnolo_123@localhost:5432/shope_management
```

### Format breakdown:

```
postgresql://  <username>  :  <password>  @  <host>  :  <port>  /  <database_name>
     ↑             ↑            ↑             ↑          ↑            ↑
  protocol      DB user     DB password    hostname   port number  database name
```

---

## 5. Create the Drizzle Config

Create `drizzle.config.ts` in the **project root** (e.g., `api/drizzle.config.ts`):

```typescript
import { defineConfig } from 'drizzle-kit';
import * as dotenv from 'dotenv';
import * as path from 'path';

// Load .env from the current directory (and parent as fallback)
dotenv.config({ path: path.resolve(__dirname, './.env') });
dotenv.config({ path: path.resolve(__dirname, '../.env') });

export default defineConfig({
  schema: './database/drizzle/schema.ts',  // path to your schema file
  out: './database/migrations',            // where migration SQL files go
  dialect: 'postgresql',                   // database dialect
  dbCredentials: {
    url: process.env.DATABASE_URL!,        // connection string from .env
  },
});
```

> [!NOTE]
> **Why `dotenv` is needed here:** `drizzle-kit` runs as a standalone CLI tool, not inside NestJS.
> It doesn't have access to `ConfigService`, so we manually load `.env` with `dotenv`.

---

## 6. Define the Database Schema

Create `database/drizzle/schema.ts`:

```typescript
import { pgTable, serial, varchar, integer } from 'drizzle-orm/pg-core';

// Example: A simple table
export const systemUsers = pgTable('system_users', {
  id: serial('id').primaryKey(),
  title: varchar('title', { length: 20 }).unique().notNull(),
});

// Example: Table with a foreign key reference
export const login = pgTable('login', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  password: varchar('password', { length: 60 }).notNull(),
  userID: integer('user_id')
    .notNull()
    .references(() => systemUsers.id, { onDelete: 'cascade' }),
});
```

### Common column types:

| Drizzle Function | PostgreSQL Type     | Usage                                  |
| ---------------- | ------------------- | -------------------------------------- |
| `serial()`       | `SERIAL`            | Auto-incrementing integer primary key  |
| `varchar()`      | `VARCHAR(n)`        | Variable-length text with max length   |
| `integer()`      | `INTEGER`           | Whole numbers                          |
| `text()`         | `TEXT`              | Unlimited-length text                  |
| `boolean()`      | `BOOLEAN`           | true/false                             |
| `timestamp()`    | `TIMESTAMP`         | Date & time                            |
| `uuid()`         | `UUID`              | UUID values                            |

### Common column modifiers:

| Modifier           | Purpose                                           |
| ------------------- | ------------------------------------------------- |
| `.primaryKey()`     | Makes it the primary key                          |
| `.notNull()`        | Column cannot be null                             |
| `.unique()`         | Column values must be unique                      |
| `.default(value)`   | Sets a default value                              |
| `.references(() => table.column)` | Creates a foreign key              |

### Foreign key `onDelete` options:

| Option        | Behavior                                            |
| ------------- | --------------------------------------------------- |
| `'cascade'`   | Delete child rows when parent is deleted            |
| `'set null'`  | Set the foreign key column to NULL                  |
| `'restrict'`  | Prevent deletion of parent if children exist        |
| `'no action'` | Similar to restrict (deferred check)                |

---

## 7. Create the Database Module

This is the **core step** — it creates a NestJS provider that initializes the Drizzle connection.

Create `src/database/database.module.ts`:

```bash
npm install @nestjs/config
```

```typescript
import { Module, Global } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';

import * as schema from '../../database/drizzle/schema';  // only this import is needed to change in this file sine the location of schema can be changed based on the time

// This token is used to inject the Drizzle instance anywhere in the app
export const DRIZZLE = 'DRIZZLE_CONNECTION';

@Global()  // Makes this provider available to ALL modules without re-importing
@Module({
  providers: [
    {
      provide: DRIZZLE,                    // injection token
      inject: [ConfigService],             // inject NestJS ConfigService
      useFactory: (configService: ConfigService) => {
        // 1. Create a pg connection pool
        const pool = new Pool({
          connectionString: configService.get<string>('DATABASE_URL'),
        });
        // 2. Pass pool + schema to drizzle()
        return drizzle(pool, { schema });
      },
    },
  ],
  exports: [DRIZZLE],  // Export so other modules can inject it
})
export class DatabaseModule {}
```

### How it works — step by step:

```
┌─────────────────────────────────────────────────────────────────┐
│                     DatabaseModule                              │
│                                                                 │
│  1. ConfigService reads DATABASE_URL from .env                  │
│                          ↓                                      │
│  2. new Pool({ connectionString })  →  pg connection pool       │
│                          ↓                                      │
│  3. drizzle(pool, { schema })  →  fully typed Drizzle instance  │
│                          ↓                                      │
│  4. Exported as DRIZZLE token  →  injectable anywhere           │
└─────────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **`@Global()` decorator**: This is key! Without it, every feature module that needs the database
> would have to import `DatabaseModule` in its own `imports` array. With `@Global()`, you import
> `DatabaseModule` once in `AppModule` and it's available everywhere.

> [!NOTE]
> **Why pass `{ schema }` to `drizzle()`?** This enables the **relational query API** (`db.query.tableName.findFirst()`).
> Without the schema, you can only use the SQL-like API (`db.select().from(table)`).

---

## 8. Register the Database Module in AppModule

Update `src/app.module.ts`:

```typescript
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';           // 1. Import ConfigModule
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { DatabaseModule } from './database/database.module';  // 2. Import DatabaseModule

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),  // 3. Load .env globally
    DatabaseModule,                            // 4. Initialize Drizzle globally
    // ... your other feature modules
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
```

### Order matters:

| #   | Import                           | Why                                              |
| --- | -------------------------------- | ------------------------------------------------ |
| 1st | `ConfigModule.forRoot()`         | Must load `.env` FIRST so DATABASE_URL is available |
| 2nd | `DatabaseModule`                 | Uses ConfigService to read DATABASE_URL          |
| 3rd | Feature modules                  | Can now inject DRIZZLE                           |

---

## 9. Auto-Run Migrations on Startup

Update `src/main.ts` to automatically apply pending migrations when the app starts:

```typescript
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { migrate } from 'drizzle-orm/node-postgres/migrator';
import { DRIZZLE } from './database/database.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Run any pending migrations automatically on startup
  const drizzle = app.get(DRIZZLE);
  await migrate(drizzle, { migrationsFolder: './database/migrations' });

  await app.listen(process.env.PORT ?? 3100);
}
bootstrap();
```

> [!WARNING]
> **Auto-migration in production:** Running migrations automatically on startup is convenient for
> development. For production, consider running migrations as a separate step in your CI/CD pipeline
> instead (e.g., `npm run migrate` before deploying).

---

## 10. Generate & Run Migrations

Add these scripts to your `package.json`:

```json
{
  "scripts": {
    "generate": "drizzle-kit generate",
    "migrate": "drizzle-kit migrate"
  }
}
```

### Workflow:

```bash
# Step 1: Edit your schema (database/drizzle/schema.ts)
#         Add/modify/remove tables and columns

# Step 2: Generate a migration SQL file
npm run generate

# Step 3: Apply the migration to your database
npm run migrate
```

### What happens:

```
schema.ts (edited)
      ↓
npm run generate
      ↓
database/migrations/0005_some_name.sql  (auto-generated SQL)
      ↓
npm run migrate   (or auto-runs on app startup via main.ts)
      ↓
PostgreSQL tables updated ✓
```

> [!TIP]
> Every time you modify `schema.ts`, run `npm run generate` to create a new migration file,
> then `npm run migrate` (or restart your app) to apply it.

---

## 11. Inject Drizzle into Any Service

### Step 1: Inject the DRIZZLE token

In any service, inject the Drizzle instance using the `@Inject()` decorator:

```typescript
import { Inject, Injectable } from '@nestjs/common';
import { NodePgDatabase } from 'drizzle-orm/node-postgres';
import { DRIZZLE } from 'src/database/database.module';
import * as schema from '../../database/drizzle/schema';

@Injectable()
export class YourService {
  constructor(
    @Inject(DRIZZLE)
    private db: NodePgDatabase<typeof schema>   // fully typed!
  ) {}
}
```

> [!IMPORTANT]
> **Type annotation**: `NodePgDatabase<typeof schema>` gives you full type safety.
> The `<typeof schema>` generic enables autocomplete for `db.query.tableName`.

### Step 2: Perform CRUD Operations

#### CREATE — Insert a record

```typescript
const newRecord = await this.db
  .insert(schema.systemUsers)
  .values({ title: 'admin' })
  .returning();                // returns the inserted row(s)
```

#### READ — Query records

```typescript
// Method 1: SQL-like API (always available)
const allUsers = await this.db
  .select()
  .from(schema.systemUsers);

// Method 2: Relational Query API (requires schema in drizzle config)
const user = await this.db.query.systemUsers.findFirst({
  where: eq(schema.systemUsers.title, 'admin'),
});
```

#### UPDATE — Modify a record

```typescript
import { eq } from 'drizzle-orm';

const updated = await this.db
  .update(schema.systemUsers)
  .set({ title: 'super admin' })
  .where(eq(schema.systemUsers.id, 1))
  .returning();
```

#### DELETE — Remove a record

```typescript
import { eq } from 'drizzle-orm';

const deleted = await this.db
  .delete(schema.systemUsers)
  .where(eq(schema.systemUsers.id, 1))
  .returning();
```

### Complete Service Example (from the project):

```typescript
import { BadRequestException, Inject, Injectable } from '@nestjs/common';
import { NodePgDatabase } from 'drizzle-orm/node-postgres';
import { DRIZZLE } from 'src/database/database.module';
import * as schema from '../../database/drizzle/schema';
import { eq } from 'drizzle-orm';

@Injectable()
export class SystemRollsService {
  constructor(
    @Inject(DRIZZLE)
    private db: NodePgDatabase<typeof schema>
  ) {}

  // CREATE
  async createSystemRoll(body: { title: string }) {
    // Check if it already exists
    const existing = await this.db.query.systemUsers.findFirst({
      where: eq(schema.systemUsers.title, body.title),
    });

    if (existing) {
      throw new BadRequestException({
        message: `The system roll ${body.title} already exists.`,
      });
    }

    // Insert new record
    const newRoll = await this.db
      .insert(schema.systemUsers)
      .values({ title: body.title })
      .returning();

    return { message: 'new role created', data: newRoll };
  }

  // READ (all)
  async allSystemRolls() {
    return await this.db.select().from(schema.systemUsers);
  }

  // UPDATE
  async updateSystemRoll(id: number, body: { title: string }) {
    return await this.db
      .update(schema.systemUsers)
      .set({ title: body.title })
      .where(eq(schema.systemUsers.id, id))
      .returning();
  }

  // DELETE
  async deleteSystemRoll(id: number) {
    return await this.db
      .delete(schema.systemUsers)
      .where(eq(schema.systemUsers.id, id))
      .returning();
  }
}
```

---

## 12. Bonus: Zod Validation Pipe

This project uses **Zod** (not `class-validator`) for request validation.

### Define a DTO with Zod:

```typescript
// src/<feature>/dto/<feature>.dto.ts
import { z } from 'zod';

export const systemRollDto = z.object({
  title: z
    .string({ message: 'role should be a string' })
    .min(1, { message: 'this field can not be empty' })
    .max(20, { message: 'this field takes less than 20 characters' }),
});

// Infer the TypeScript type from the Zod schema
export type SystemRollDto = z.infer<typeof systemRollDto>;
```

### Create a reusable Zod Validation Pipe:

```typescript
// src/common/pipes/zod-validation.pipe.ts
import {
  ArgumentMetadata,
  BadRequestException,
  Injectable,
  PipeTransform,
} from '@nestjs/common';
import type { ZodSchema } from 'zod';

@Injectable()
export class ZodValidationPipe implements PipeTransform {
  constructor(private schema: ZodSchema) {}

  transform(value: any, metadata: ArgumentMetadata) {
    const result = this.schema.safeParse(value);

    if (!result.success) {
      throw new BadRequestException({
        message: 'validation failed',
        error: result.error.issues,
      });
    }

    return result.data;  // returns the validated & typed data
  }
}
```

### Use it in a Controller:

```typescript
import { Body, Controller, Post, UsePipes } from '@nestjs/common';
import { systemRollDto, SystemRollDto } from './dto/systemRoll.dto';
import { ZodValidationPipe } from 'src/common/pipes/zod-validation.pipe';

@Controller('system-rolls')
export class SystemRollsController {
  constructor(private service: SystemRollsService) {}

  // Option 1: Apply to the whole method
  @Post()
  @UsePipes(new ZodValidationPipe(systemRollDto))
  async create(@Body() body: SystemRollDto) {
    return await this.service.createSystemRoll(body);
  }

  // Option 2: Apply to a specific parameter
  @Patch(':id')
  async update(
    @Param('id', ParseIntPipe) id: number,
    @Body(new ZodValidationPipe(systemRollDto)) body: SystemRollDto,
  ) {
    return await this.service.updateSystemRoll(id, body);
  }
}
```

---

## 13. Quick Reference Cheat Sheet

### Packages to install:

```bash
npm i drizzle-orm pg @nestjs/config
npm i -D drizzle-kit @types/pg dotenv
```

### Files to create/modify (in order):

| #   | File                               | Purpose                          |
| --- | ---------------------------------- | -------------------------------- |
| 1   | `.env`                             | Store `DATABASE_URL`             |
| 2   | `drizzle.config.ts`                | Tell Drizzle Kit where things are|
| 3   | `database/drizzle/schema.ts`       | Define your tables               |
| 4   | `src/database/database.module.ts`  | Create the NestJS Drizzle provider |
| 5   | `src/app.module.ts`                | Import ConfigModule + DatabaseModule |
| 6   | `src/main.ts`                      | (Optional) Auto-migrate on startup |

### Key imports per file:

```typescript
// database.module.ts
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';

// any service
import { NodePgDatabase } from 'drizzle-orm/node-postgres';
import { eq } from 'drizzle-orm';

// main.ts (for migrations)
import { migrate } from 'drizzle-orm/node-postgres/migrator';
```

### The injection pattern (memorize this):

```typescript
// 1. Import
import { DRIZZLE } from 'src/database/database.module';
import { NodePgDatabase } from 'drizzle-orm/node-postgres';
import * as schema from '../../database/drizzle/schema';

// 2. Inject in constructor
constructor(
  @Inject(DRIZZLE)
  private db: NodePgDatabase<typeof schema>
) {}

// 3. Use this.db for all queries
await this.db.select().from(schema.tableName);
await this.db.query.tableName.findFirst({ where: ... });
await this.db.insert(schema.tableName).values({ ... }).returning();
await this.db.update(schema.tableName).set({ ... }).where(...).returning();
await this.db.delete(schema.tableName).where(...).returning();
```

### Migration commands:

```bash
npm run generate    # Generate migration SQL from schema changes
npm run migrate     # Apply migrations to the database
```

---

> **Version info used in this project:**
> `drizzle-orm@0.45.2` · `drizzle-kit@0.31.10` · `pg@8.21.0` · `@nestjs/common@11.x` · `@nestjs/config@4.x` · `zod@4.4.3`
