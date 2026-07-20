# JWT Authentication — Full Guide for Shope Management System

This document explains what JWT is, how it works, and walks through every single file you need to create or modify in this project to implement it. Written specifically for this codebase, code-first.

---

## Table of Contents

1. [What is JWT and Why Do We Need It?](#1-what-is-jwt-and-why-do-we-need-it)
2. [How the Flow Works (Big Picture)](#2-how-the-flow-works-big-picture)
3. [What is a Token Payload?](#3-what-is-a-token-payload)
4. [Installing the Required Packages](#4-installing-the-required-packages)
5. [Adding the JWT Secret to .env](#5-adding-the-jwt-secret-to-env)
6. [Step 1 — Create the Auth DTO (Login Input Validation)](#6-step-1--create-the-auth-dto-login-input-validation)
7. [Step 2 — Create the Auth Service (Core Logic)](#7-step-2--create-the-auth-service-core-logic)
8. [Step 3 — Create the JWT Strategy (Token Verification)](#8-step-3--create-the-jwt-strategy-token-verification)
9. [Step 4 — Create the JWT Auth Guard (Protect Routes)](#9-step-4--create-the-jwt-auth-guard-protect-routes)
10. [Step 5 — Create the Roles Guard (Role-Based Access)](#10-step-5--create-the-roles-guard-role-based-access)
11. [Step 6 — Create the Roles Decorator](#11-step-6--create-the-roles-decorator)
12. [Step 7 — Create the Auth Controller (Login Endpoint)](#12-step-7--create-the-auth-controller-login-endpoint)
13. [Step 8 — Create the Auth Module](#13-step-8--create-the-auth-module)
14. [Step 9 — Register the Auth Module in App Module](#14-step-9--register-the-auth-module-in-app-module)
15. [Step 10 — Protect an Existing Route (Real Example)](#15-step-10--protect-an-existing-route-real-example)
16. [Testing the Flow End to End](#16-testing-the-flow-end-to-end)
17. [Common Mistakes and Fixes](#17-common-mistakes-and-fixes)
18. [Access and Refresh Tokens](#18-access-and-refresh-tokens)

---

## 1. What is JWT and Why Do We Need It?

### The problem JWT solves

HTTP is **stateless**. That means after a user logs in, the server immediately forgets them. On the very next request, the server has no idea who is sending it. Without a solution, every single request would require the user to send their email and password again — which is terrible.

**JWT (JSON Web Token)** solves this by giving the user a **signed token** after they log in. The user stores this token (in the browser's localStorage or a cookie) and sends it with every future request. The server reads the token, verifies it was genuinely created by itself, and trusts the identity inside.

### What a JWT looks like

A JWT is a long string divided into 3 parts, separated by dots:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImVtYWlsIjoic2hvcGVAZ21haWwuY29tIiwicm9sZSI6InNob3BlIiwiaWF0IjoxNzE4MDAwMDAwLCJleHAiOjE3MTgwODY0MDB9.abc123signature
```

These 3 parts are:

| Part | Name | What it contains |
|---|---|---|
| Part 1 | **Header** | Algorithm used to sign (e.g. HS256) |
| Part 2 | **Payload** | Your data (userId, email, role, expiry) |
| Part 3 | **Signature** | A hash of Header+Payload+Secret — proves authenticity |

> **Important:** The payload is only Base64-encoded, NOT encrypted. Anyone can decode it. Never put passwords or sensitive data in the payload. The signature is what makes it secure — only your server, which knows the secret key, can create a valid signature.

---

## 2. How the Flow Works (Big Picture)

```
┌────────────┐         POST /auth/login           ┌────────────────┐
│  Frontend  │ ─────────────────────────────────► │  NestJS API    │
│            │   { email, password }              │                │
│            │                                    │  1. Find user  │
│            │                                    │  2. Compare    │
│            │                                    │     bcrypt hash│
│            │   { access_token: "eyJ..." }       │  3. Sign JWT   │
│            │ ◄───────────────────────────────── │                │
│            │                                    └────────────────┘
│  Stores    │
│  the token │
│            │         GET /cart (protected)      ┌────────────────┐
│            │ ─────────────────────────────────► │  NestJS API    │
│  Sends:    │   Header: Bearer eyJ...            │                │
│  Bearer    │                                    │  JwtAuthGuard  │
│  token     │                                    │  1. Read token │
│            │                                    │  2. Verify sig │
│            │   { cart data... }                 │  3. Allow/Deny │
│            │ ◄───────────────────────────────── │                │
└────────────┘                                    └────────────────┘
```

---

## 3. What is a Token Payload?

The payload is the data we **embed inside** the JWT. For this project, we will put:

```ts
{
  sub: 1,              // The login table's row ID (subject — standard JWT field)
  email: "shop@gmail.com",
  role: "shope",       // From the system_users table (super admin / customer / shope / delivery boy)
}
```

When the token arrives in a future request, NestJS will decode it and this object will be attached to `request.user`. So in any controller you can do `req.user.role` to know who is making the request.

---

## 4. Installing the Required Packages

Run this command from inside the `/api` directory:

```bash
npm install @nestjs/jwt @nestjs/passport passport passport-jwt
npm install --save-dev @types/passport-jwt
```

**What each package does:**

| Package | Purpose |
|---|---|
| `@nestjs/jwt` | NestJS wrapper around the `jsonwebtoken` library. Gives us `JwtModule` and `JwtService` to sign/verify tokens. |
| `@nestjs/passport` | NestJS wrapper for `passport`. Connects passport strategies to NestJS's guard system. |
| `passport` | The core authentication middleware library for Node.js. |
| `passport-jwt` | A passport "strategy" that knows how to extract and verify a JWT from an HTTP request's `Authorization` header. |
| `@types/passport-jwt` | TypeScript type definitions for `passport-jwt`. Dev-only, not needed in production. |

---

## 5. Adding the JWT Secret to .env

Open `/home/agnolo/Desktop/Projects/shope-management-system/api/.env` and add:

```env
# Existing variables
DATABASE_URL=postgresql://...
SUPERADMIN_EMAIL=admin@shope.com
SUPERADMIN_PASSWORD=SuperadminSecurePassword123!

# Add these new ones:
JWT_SECRET=your_super_secret_key_change_this_in_production_make_it_long
JWT_EXPIRES_IN=1d
```

## 5.1 importing and configuring the 'jwt' to use it globally in the root module.ts file 'app.module.ts', if we don't need it globally we can setup it in the 'module.ts' of the module just like the step-8 
```ts
import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config'; // 1. Import ConfigModule
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { RegistrationModule } from './registration/registration.module';
import { DatabaseModule } from './database/database.module'; // 2. Import your DatabaseModule
import { SystemRollsModule } from './system-rolls/system-rolls.module';
import { StatusModule } from './status/status.module';
import { ProductCategoryModule } from './product-category/product-category.module';
import { ProductManagementModule } from './product-management/product-management.module';
import { CartModule } from './cart/cart.module';
import { AuthModule } from './auth/auth.module';
import { JwtModule } from '@nestjs/jwt';

@Module({
	imports: [
		ConfigModule.forRoot({ isGlobal: true }), // 3. Load env variables globally
		DatabaseModule, // 4. Inject Drizzle globally
// ----------------------------------------------------------------------------------------------------------
		// configuring the JWT to use it globally
		JwtModule.registerAsync({
			global: true,
			inject: [ConfigService],
			useFactory: (configService: ConfigService) =>({
				secret: configService.get<string>('JWT_SECRET') || 'fallbackSecretKey',
        signOptions: { 
          expiresIn: configService.get<string>('JWT_EXPIRES_IN') ?? '1d',
        },
			})
		}),
//------------------------------------------------------------------------------------------------------------
		RegistrationModule, SystemRollsModule, StatusModule, ProductCategoryModule, ProductManagementModule, CartModule, AuthModule,
	],
	controllers: [AppController],
	providers: [AppService],
})
export class AppModule {}
```


**What is JWT_SECRET?**

This is the private key your server uses to **sign** tokens. It's like a stamp only you own. When a token arrives, you re-sign the header+payload with this key and check if the signature matches. If someone tampers with the token, the signatures won't match and access is denied.

**Make it long and random** in production. For local dev, any string works.

**What is JWT_EXPIRES_IN?**

This is how long the token stays valid. `1d` = 1 day. After that, the user must log in again. Other formats: `15m` (15 minutes), `7d` (7 days).

---

## 6. Step 1 — Create the Auth DTO (Login Input Validation)

**File to create:** `src/auth/dto/auth.dto.ts`

This is the Zod schema that validates the login request body. Same pattern as your existing DTOs in the `registration` module.

```ts
// src/auth/dto/auth.dto.ts

import { z } from 'zod';

// This is the schema for the login request body.
// When someone hits POST /auth/login, the request body must match this.
export const loginDto = z.object({
  email: z.email({ message: 'Enter a valid email address' }),
  password: z.string().min(1, { message: 'Password is required' }),
});

// This is the TypeScript type inferred from the Zod schema.
// We use it to type function parameters so TypeScript is happy.
export type LoginSchema = z.infer<typeof loginDto>;
```

**Why a separate DTO for auth?**

The registration DTO has many fields (name, address, lat, long etc.). The login only needs email + password. A dedicated DTO keeps things clean and focused.

---

## 7. Step 2 — Create the Auth Service (Core Logic)

**File to create:** `src/auth/auth.service.ts`

This is the brain of authentication. It contains two methods:
1. `validateUser` — checks if email exists and password matches the bcrypt hash
2. `login` — signs a JWT and returns it

```ts
// src/auth/auth.service.ts

import { Inject, Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { NodePgDatabase } from 'drizzle-orm/node-postgres';
import { eq } from 'drizzle-orm';
import * as bcrypt from 'bcryptjs';

import { DRIZZLE } from 'src/database/database.module';
import * as schema from '../../database/drizzle/schema';
import type { LoginSchema } from './dto/auth.dto';

@Injectable()
export class AuthService {
  constructor(
    // Inject our Drizzle database connection (same pattern as registration.service.ts)
    @Inject(DRIZZLE)
    private db: NodePgDatabase<typeof schema>,

    // Inject NestJS's JwtService so we can sign tokens
    private jwtService: JwtService,
  ) {}

  /**
   * validateUser: Checks if the email/password combination is correct.
   *
   * Step 1: Look up the login row by email.
   * Step 2: Use bcrypt.compare() to check if the plaintext password
   *         matches the stored hash. We never store or compare raw passwords.
   * Step 3: If valid, return the login row data. If not, return null.
   *
   * bcrypt.compare() works like this:
   *   - You give it the raw password ("secret123") and the stored hash ("$2b$10$...")
   *   - bcrypt internally re-hashes the raw password with the same salt
   *     that was used originally, and checks if results match.
   *   - Returns true/false.
   */
  async validateUser(email: string, password: string){

      const result = await this.db.select({
          login: schema.login,
          systemUser: schema.systemUsers
      })
      .from(schema.login)
      .leftJoin(schema.systemUsers, eq(schema.login.userID, schema.systemUsers.id))
      .where(eq(schema.login.email, email))
      .then(rows => rows[0])    

      if(!result){
          return null
      }

      const isPasswordValid = await bcrypt.compare(password, result.login.password)

      if(!isPasswordValid){
          return null
      }

      const {password: _, ...loginWithOutPassword} = result.login

      return({
          loginWithOutPassword: loginWithOutPassword,
          systemUser: result.systemUser
      })
  }

  /**
   * login: Creates and returns the JWT access token.
   *
   * This is called AFTER validateUser confirms the credentials are correct.
   *
   * The payload is what gets embedded inside the JWT.
   * Remember: the payload is readable by anyone who has the token,
   * so we only put non-sensitive identifiers in it.
   */
  async login(body: LoginSchema) {
    // First validate the credentials
    const user = await this.validateUser(body.email, body.password);

    if (!user) {
      // 401 Unauthorized — wrong email or password
      throw new UnauthorizedException({
        message: 'Invalid email or password',
      });
    }

    // Build the JWT payload
    // 'sub' is a standard JWT field meaning "subject" (who the token is about)
    const payload = {
      sub: user.loginWithOutPassword.id,                                    // The login table's primary key
      email: user.loginWithOutPassword.email,                               // The user's email
      role: user.systemUser?.title ?? 'unknown',       // e.g. 'shope', 'customer', 'super admin'
    };

    // jwtService.sign() creates the token string using our secret key
    // The options like expiresIn come from the JwtModule configuration
    return {
      message: 'Login successful',
      access_token: this.jwtService.sign(payload)
    };
  }
}
```

**Key concept — why `bcrypt.compare()`?**

When a shope registered, you stored:
```
password: await bcrypt.hash(body.password, 10)
```

`bcrypt.hash("secret123", 10)` produces something like `$2b$10$randomsalt...hashed`. You can never reverse this. So during login, `bcrypt.compare("secret123", "$2b$10$...")` internally applies the same hashing and checks equality. This means even if your database leaks, passwords are safe.

---

## 8. Step 3 — Create the JWT Strategy (Token Verification)

**File to create:** `src/auth/strategies/jwt.strategy.ts`

A **Strategy** is a Passport concept. It defines *how* to extract and validate a credential from an incoming HTTP request.

The `JwtStrategy` does two things:
1. Tells passport WHERE to find the token in the request (in the `Authorization: Bearer <token>` header)
2. Provides a `validate()` callback that runs after passport has verified the token's signature — this is where you put `request.user`

```ts
// src/auth/strategies/jwt.strategy.ts

import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';

// The shape of data we embedded in the JWT payload when we signed it
interface JwtPayload {
  sub: number;      // login.id
  email: string;
  role: string;     // e.g. 'shope', 'customer', 'super admin', 'delivery boy'
}

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(configService: ConfigService) {
    super({
      // ExtractJwt.fromAuthHeaderAsBearerToken() means:
      // Look in the HTTP request's "Authorization" header.
      // Expect the format: "Bearer eyJ..."
      // Extract and return just the token part after "Bearer ".
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),

      // If the token's expiry time (exp) has passed, reject it automatically.
      ignoreExpiration: false,

      // The secret key to verify the signature.
      // MUST be the same key used to sign the token in AuthService.
      secretOrKey: configService.get<string>('JWT_SECRET'),
    });
  }

  /**
   * validate() is called by passport AFTER it has:
   * 1. Extracted the token from the header
   * 2. Verified the signature using our secret
   * 3. Checked the token has not expired
   *
   * If all that passes, passport calls validate(payload) with the decoded payload.
   * Whatever this function RETURNS becomes `request.user` in your controllers.
   *
   * If the token is invalid or expired, passport rejects before even calling this.
   */
  validate(payload: JwtPayload) {
    // We return a clean user object that will be attached to request.user
    return {
      id: payload.sub,
      email: payload.email,
      role: payload.role,
    };
  }
}
```

**Why `PassportStrategy(Strategy)`?**

`PassportStrategy` is a NestJS helper class. It takes a Passport strategy class (like `Strategy` from `passport-jwt`) and turns it into a NestJS-friendly injectable service. The `super({ ... })` call configures that strategy.

---

## 9. Step 4 — Create the JWT Auth Guard (Protect Routes)

**File to create:** `src/auth/guards/jwt-auth.guard.ts`

A **Guard** in NestJS is a class that runs *before* a route handler and decides whether to let the request through. Think of it as a bouncer at a door.

The `JwtAuthGuard` ties the `JwtStrategy` into the guard system. When applied to a route, it runs the strategy, and if the token is invalid, it returns a 401 Unauthorized automatically.

```ts
// src/auth/guards/jwt-auth.guard.ts

import { Injectable } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';

/**
 * JwtAuthGuard: Protects a route by requiring a valid JWT.
 *
 * AuthGuard('jwt') means: "use the strategy registered under the name 'jwt'"
 * Passport-JWT registers itself as 'jwt' by default when you extend PassportStrategy(Strategy).
 *
 * Usage in a controller:
 *   @UseGuards(JwtAuthGuard)
 *   @Get('protected-route')
 *   myProtectedMethod() { ... }
 *
 * What happens when this guard runs:
 * 1. It triggers the JwtStrategy
 * 2. JwtStrategy extracts the token from the Authorization header
 * 3. Verifies the signature + expiry
 * 4. Calls validate() — result goes to request.user
 * 5. If any step fails — 401 Unauthorized is automatically returned
 * 6. If all passes — route handler is called with request.user populated
 */
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {}
```

**That's it — just one line.** NestJS + Passport do the rest.

---

## 10. Step 5 — Create the Roles Guard (Role-Based Access)

**File to create:** `src/auth/guards/roles.guard.ts`

The `JwtAuthGuard` only verifies *that someone is logged in*. The `RolesGuard` checks *what role they have*.

For example:
- Only a `super admin` should be able to create system roles
- Only a `shope` should be able to add products to their own shop
- Only a `customer` should be able to add items to their cart

```ts
// src/auth/guards/roles.guard.ts

import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { ROLES_KEY } from '../decorators/roles.decorator';

/**
 * RolesGuard: Checks if the logged-in user has the required role for a route.
 *
 * This guard MUST be used AFTER JwtAuthGuard because it relies on request.user
 * being populated. JwtAuthGuard runs first and puts the user on the request.
 *
 * It works together with the @Roles() decorator (created in Step 6).
 * The decorator sets metadata on the route handler.
 * This guard reads that metadata and compares it to request.user.role.
 *
 * Usage in a controller:
 *   @UseGuards(JwtAuthGuard, RolesGuard)
 *   @Roles('super admin', 'shope')
 *   @Get('admin-only')
 *   myAdminMethod() { ... }
 */
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    // Read the required roles from the @Roles() decorator metadata
    const requiredRoles = this.reflector.getAllAndOverride<string[]>(ROLES_KEY, [
      context.getHandler(),   // Check method-level decorator first
      context.getClass(),     // Then check class-level decorator
    ]);

    // If no @Roles() decorator was applied, this guard passes through
    if (!requiredRoles) {
      return true;
    }

    // Get the request object and the user attached by JwtAuthGuard
    const { user } = context.switchToHttp().getRequest();

    // Check if the user's role is in the list of required roles
    return requiredRoles.includes(user.role);
  }
}
```

---

## 11. Step 6 — Create the Roles Decorator

**File to create:** `src/auth/decorators/roles.decorator.ts`

A **custom decorator** is just a helper that attaches metadata to a route. `@Roles('super admin')` above a controller method is how you declare which roles are allowed. The `RolesGuard` then reads that metadata.

```ts
// src/auth/decorators/roles.decorator.ts

import { SetMetadata } from '@nestjs/common';

// This is a unique key used to store/retrieve the roles metadata.
// It's just a string constant — naming it this way avoids typos.
export const ROLES_KEY = 'roles';

/**
 * @Roles() decorator — marks a route with the allowed roles.
 *
 * Usage:
 *   @Roles('super admin')           — only super admin can access
 *   @Roles('shope', 'super admin')  — shope OR super admin can access
 *   @Roles('customer')              — only customer can access
 *
 * SetMetadata attaches the roles array to the route handler's metadata,
 * which RolesGuard later reads using Reflector.
 */
export const Roles = (...roles: string[]) => SetMetadata(ROLES_KEY, roles);
```

---

## 12. Step 7 — Create the Auth Controller (Login Endpoint)

**File to create:** `src/auth/auth.controller.ts`

The controller creates the `POST /auth/login` endpoint. It validates the body using your existing `ZodValidationPipe` pattern, then calls `authService.login()`.

```ts
// src/auth/auth.controller.ts

import { Body, Controller, Post } from '@nestjs/common';
import { AuthService } from './auth.service';
import { ZodValidationPipe } from 'src/common/pipes/zod-validation.pipe';
import { loginDto, type LoginSchema } from './dto/auth.dto';

@Controller('auth')
export class AuthController {
  constructor(private authService: AuthService) {}

  /**
   * POST /auth/login
   *
   * Request body:
   * {
   *   "email": "myshope@gmail.com",
   *   "password": "mypassword123"
   * }
   *
   * Success response:
   * {
   *   "message": "Login successful",
   *   "access_token": "eyJhbGci...",
   *   "role": "shope"
   * }
   *
   * Failure response (wrong credentials):
   * {
   *   "statusCode": 401,
   *   "message": "Invalid email or password"
   * }
   */
  @Post('login')
  async login(@Body(new ZodValidationPipe(loginDto)) body: LoginSchema) {
    return await this.authService.login(body);
  }
}
```

---

## 13. Step 8 — Create the Auth Module

**File to create:** `src/auth/auth.module.ts`

The module is the glue that ties together the controller, service, strategy, and JWT configuration.

```ts
// src/auth/auth.module.ts

import { Module } from '@nestjs/common';
import { JwtModule } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';
import { ConfigModule, ConfigService } from '@nestjs/config';

import { AuthController } from './auth.controller';
import { AuthService } from './auth.service';
import { JwtStrategy } from './strategies/jwt.strategy';

@Module({
  imports: [
    // PassportModule registers passport in the NestJS DI system.
    // defaultStrategy: 'jwt' makes it so AuthGuard() without arguments
    // defaults to the JWT strategy.
    PassportModule.register({ defaultStrategy: 'jwt' }),

    // JwtModule provides JwtService (used in auth.service.ts to sign tokens).
    // We use registerAsync so we can read JWT_SECRET and JWT_EXPIRES_IN
    // from ConfigService (which reads from .env via ConfigModule).
    JwtModule.registerAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (configService: ConfigService) => ({
        secret: configService.get<string>('JWT_SECRET'),
        signOptions: {
          expiresIn: configService.get<string>('JWT_EXPIRES_IN') ?? '1d',
        },
      }),
    }),
  ],
  controllers: [AuthController],
  providers: [
    AuthService,
    JwtStrategy,   // Register the strategy as a provider so NestJS can inject it
  ],
  exports: [
    JwtStrategy,   // Export so other modules can use the strategy
    PassportModule, // Export so other modules can use AuthGuard
  ],
})
export class AuthModule {}
```

**Why `registerAsync`?**

`JwtModule.register({ secret: 'hardcoded' })` would work but hardcodes the secret. `registerAsync` lets you use `ConfigService` to pull the secret from `.env`, which is the correct approach.

---

## 14. Step 9 — Register the Auth Module in App Module

**File to modify:** `src/app.module.ts`

```ts
// src/app.module.ts

import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { RegistrationModule } from './registration/registration.module';
import { DatabaseModule } from './database/database.module';
import { SystemRollsModule } from './system-rolls/system-rolls.module';
import { StatusModule } from './status/status.module';
import { ProductCategoryModule } from './product-category/product-category.module';
import { ProductManagementModule } from './product-management/product-management.module';
import { CartModule } from './cart/cart.module';
import { AuthModule } from './auth/auth.module'; // ADD THIS IMPORT

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    DatabaseModule,
    RegistrationModule,
    SystemRollsModule,
    StatusModule,
    ProductCategoryModule,
    ProductManagementModule,
    CartModule,
    AuthModule, // ADD THIS LINE
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
```

---

## 15. Step 10 — Protect an Existing Route (Real Example)

Now that everything is wired up, here is how to protect routes in your existing controllers.

**Example: Protecting a cart route so only customers can access it**

```ts
import {
  Body,
  Controller,
  Get,
  Post,
  UseGuards,
  Request,
} from '@nestjs/common';
import { JwtAuthGuard } from 'src/auth/guards/jwt-auth.guard';
import { RolesGuard } from 'src/auth/guards/roles.guard';
import { Roles } from 'src/auth/decorators/roles.decorator';
import { CartService } from './cart.service';

@Controller('cart')
export class CartController {
  constructor(private cartService: CartService) {}

  // This route requires:
  // 1. A valid JWT token (JwtAuthGuard)
  // 2. The user's role to be 'customer' (RolesGuard + @Roles)
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('customer')
  @Get()
  async getMyCart(@Request() req) {
    // req.user is populated by JwtAuthGuard via the JwtStrategy.validate() method
    // It contains: { id, email, role }
    const customerId = req.user.id;
    return await this.cartService.getCartByCustomer(customerId);
  }

  // This route only needs a valid JWT (any role can access — just must be logged in)
  @UseGuards(JwtAuthGuard)
  @Post()
  async addToCart(@Request() req, @Body() body) {
    const customerId = req.user.id;
    return await this.cartService.addItem(customerId, body);
  }
}
```

**Example: Protecting a product route so only shopes can create products**

```ts
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('shope')
@Post('products')
async createProduct(@Request() req, @Body() body) {
  const shopeLoginId = req.user.id; // the login ID of the shope user
  return await this.productService.create(shopeLoginId, body);
}
```

**Example: Super admin only route**

```ts
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('super admin')
@Get('admin/all-users')
async getAllUsers() {
  return await this.adminService.getAllUsers();
}
```

---

## 16. Testing the Flow End to End

Once you start the server with `npm run start:dev`, test with curl or Postman/Insomnia:

### Step 1: Register a shop (you probably already have this)
```bash
curl -X POST http://localhost:3100/registration \
  -H "Content-Type: application/json" \
  -d '{
    "email": "myshope@gmail.com",
    "password": "password123",
    "name": "My Shop",
    "address": "123 Main Street",
    "lat": 10.0,
    "long": 76.0,
    "officialEmail": "official@myshope.com",
    "phone": "9876543210",
    "description": "A great shop that sells things"
  }'
```

### Step 2: Login to get the JWT token
```bash
curl -X POST http://localhost:3100/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "myshope@gmail.com",
    "password": "password123"
  }'
```

**Expected response:**
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "role": "shope"
}
```

Copy the `access_token` value.

### Step 3: Access a protected route with the token
```bash
curl -X GET http://localhost:3100/cart \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Step 4: Try accessing without a token (should get 401)
```bash
curl -X GET http://localhost:3100/cart
# Response: 401 Unauthorized
```

### Step 5: Try accessing with wrong role (should get 403)
If you log in as a `shope` and try to access a `customer`-only route, you get 403 Forbidden.

---

## 17. Common Mistakes and Fixes

### Mistake 1: `with: { systemUser: true }` fails in Drizzle

The `validateUser` method in `auth.service.ts` uses `with: { systemUser: true }` to join the `system_users` table. For this to work, you need to define a **Drizzle relation** in your schema.

Add this to the bottom of `database/drizzle/schema.ts`:

```ts
import { relations } from 'drizzle-orm';

// Defines that login.userID references systemUsers.id
// and names the joined result 'systemUser'
export const loginRelations = relations(login, ({ one }) => ({
  systemUser: one(systemUsers, {
    fields: [login.userID],
    references: [systemUsers.id],
  }),
}));
```

### Mistake 2: 401 on every request even with a valid token

**Possible cause:** The `JWT_SECRET` in `.env` does not match what was used to sign the token. If you change the secret, all previously issued tokens become invalid.

**Fix:** Restart the server after editing `.env`, and log in again to get a new token.

### Mistake 3: 403 Forbidden instead of 401 Unauthorized

`401 Unauthorized` = no valid token at all. `403 Forbidden` = valid token but wrong role. These are different HTTP status codes. If you're seeing 403 when you expect to get in, check that `req.user.role` matches exactly what `@Roles()` expects (case-sensitive: `'super admin'` not `'superadmin'`).

### Mistake 4: `request.user` is undefined in the controller

This means `JwtAuthGuard` is not applied to the route. Make sure you have `@UseGuards(JwtAuthGuard)` on the method or the class.

### Mistake 5: Token never expires / always expires immediately

Check `JWT_EXPIRES_IN` in `.env`. Valid formats: `1d`, `7d`, `15m`, `1h`, `3600` (seconds). If you set it to `1` (just a number with no unit), it means 1 millisecond and will expire immediately.

---

## Final Directory Structure for Auth Module

After all the above steps, your `src/auth/` folder should look like this:

```
src/
└── auth/
    ├── auth.controller.ts        ← POST /auth/login endpoint
    ├── auth.module.ts            ← Glues everything together
    ├── auth.service.ts           ← validateUser() and login() logic
    ├── dto/
    │   └── auth.dto.ts           ← Zod schema for login body
    ├── guards/
    │   ├── jwt-auth.guard.ts     ← Protects routes (requires valid JWT)
    │   └── roles.guard.ts        ← Restricts routes by role
    ├── decorators/
    │   └── roles.decorator.ts    ← @Roles() decorator
    └── strategies/
        └── jwt.strategy.ts       ← Tells passport how to verify JWT
```

---

> **Summary of what happens when a user hits a protected route:**
>
> 1. Request arrives with `Authorization: Bearer eyJ...`
> 2. `JwtAuthGuard` triggers — calls `JwtStrategy`
> 3. `JwtStrategy` extracts the token from the header
> 4. passport-jwt verifies the signature using `JWT_SECRET`
> 5. passport-jwt checks the `exp` field — token not expired
> 6. `JwtStrategy.validate(payload)` is called — returns `{ id, email, role }`
> 7. NestJS puts that object on `request.user`
> 8. `RolesGuard` (if applied) reads `@Roles()` metadata and checks `request.user.role`
> 9. If all passes — route handler runs
> 10. Controller can access `req.user.id`, `req.user.email`, `req.user.role`

---

## 18. Access and Refresh Tokens

In a real-world application, authentication needs to balance security and user experience. This section explains how Access and Refresh tokens work together to achieve this.

### The Stateless Verification Dilemma
By default, JWT authentication is **stateless**. The server does not store the `access_token` anywhere. When a request arrives, the [JwtAuthGuard](file:///home/agnolo/Desktop/Projects/shope-management-system/jwt.md#L415) triggers the [JwtStrategy](file:///home/agnolo/Desktop/Projects/shope-management-system/jwt.md#L343), which validates the signature mathematically using the server's `JWT_SECRET`. 

However, this introduces two challenges:
1. **Active Expiration**: If the `access_token` expires in `1d` (1 day), an active user will be suddenly logged out on the 24th hour + 1st minute, even if they are in the middle of using the system.
2. **No Revocation**: Since the verification is stateless, if a token is stolen, the server cannot revoke it until its expiration time passes.

### The Refresh Token Solution
To solve these challenges, we split authentication into two tokens:

| Token | Lifetime | Storage Location | Stored on Server? | Purpose |
|---|---|---|---|---|
| **Access Token** | Short-lived (e.g., `15m`) | Client memory or localStorage | **No** (Stateless validation) | Used to authenticate every API request. |
| **Refresh Token** | Long-lived (e.g., `7d`) | Secure, `HttpOnly` cookie | **Yes** (Database lookup) | Used to request a new access token when it expires. |

#### Why store the Refresh Token?
Since the Refresh Token is long-lived, it is stored in the database (or hashed/indexed by session). This allows you to:
* Instantly log a user out (by deleting their refresh token from the database).
* Block compromised sessions or force-refresh all sessions.

### Token Rotation Flow
1. **Initial Login**: The user provides credentials to `POST /auth/login`. The server creates and returns both an Access Token and a Refresh Token (and saves the refresh token in the database).
2. **Access Token Expiry**: After 15 minutes, the Access Token expires. The next request gets a `401 Unauthorized` response.
3. **Silent Refresh**: The frontend intercepts the `401` error, sends the Refresh Token to the server's `/auth/refresh` endpoint.
4. **Verification and Rotation**: The server validates the Refresh Token against the database:
   * If valid, it returns a new **Access Token** AND a **new Refresh Token** (deleting the old one from the database). This is called **Refresh Token Rotation** and prevents reuse of old tokens.
   * If invalid/expired, the user is prompted to log in again.

### Frontend Integration (Next.js Example)

In a Next.js frontend, you can automate attaching the Access Token using request interceptors:

```ts
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:3100',
});

// Axios Request Interceptor: Automatically injects token into every request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;
```

Alternatively, you can configure your backend to set the token inside an **`HttpOnly` Cookie**. When using cookies, the browser automatically attaches them to every request, eliminating the need to manually inject headers in client-side code, while protecting the token from XSS attacks.



---
---


# Implementing Refresh Tokens & Auto-Login Flow

This document details the architecture and implementation steps to set up **Refresh Token Rotation (Silent Refresh)** and **Auto-Login** using your NestJS backend and a frontend.

---

## 🔄 How the Flow Works

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant FE as Frontend (App)
    participant BE as Backend (NestJS)
    participant DB as Database (Postgres)

    Note over FE, BE: Normal Operations (Access Token Expired)
    FE->>BE: API Request (with expired Access Token)
    BE-->>FE: 401 Unauthorized
    Note over FE: Axios Interceptor catches 401
    FE->>BE: POST /auth/refresh (with Refresh Token)
    BE->>DB: Check if Refresh Token exists & is valid
    DB-->>BE: Yes, valid
    Note over BE: Generate new Access & Refresh Token (Rotation)
    BE->>DB: Update Refresh Token in DB
    BE-->>FE: Return new Access & Refresh Tokens
    Note over FE: Update memory/local storage
    FE->>BE: Retry original API Request (with new Access Token)
    BE-->>FE: Response Success
```

---

## 🛠️ Step 1: Backend implementation (NestJS)

To support this, we need to add a `/auth/refresh` endpoint on the backend.

### 1. Update `AuthService` in `src/auth/auth.service.ts`
Add a `refresh` method that validates the refresh token, hashes it, checks it against the database, and issues new tokens:

```typescript
import { UnauthorizedException } from '@nestjs/common';

// Inside AuthService class:
async refresh(refreshToken: string) {
    try {
        const refreshSecret = this.configService.get<string>('JWT_REFRESH_SECRET');
        const payload = this.jwtService.verify(refreshToken, { secret: refreshSecret });

        const tokenHash = crypto.createHash('sha256').update(refreshToken).digest('hex');

        const storedToken = await this.db.query.refreshToken.findFirst({
            where: eq(schema.refreshToken.token, tokenHash),
        });

        // 1. Refresh Token Reuse Detection
        if (!storedToken) {
            // The token is mathematically valid but not in DB -> Stolen token reused!
            // Revoke all sessions for this user.
            await this.db.delete(schema.refreshToken).where(eq(schema.refreshToken.loginId, payload.id as number));
            throw new UnauthorizedException('Invalid refresh token. All sessions revoked for security.');
        }

        if (new Date() > storedToken.expiresAt) {
            await this.db.delete(schema.refreshToken).where(eq(schema.refreshToken.id, storedToken.id));
            throw new UnauthorizedException('Expired refresh token');
        }

        // 2. Verify user is still active
        const userStatus = await this.db.select({ status: schema.status })
            .from(schema.login)
            .leftJoin(schema.status, eq(schema.login.status, schema.status.id))
            .where(eq(schema.login.id, storedToken.loginId))
            .then(rows => rows[0]);

        if (!userStatus || userStatus.status?.title !== 'active') {
            await this.db.delete(schema.refreshToken).where(eq(schema.refreshToken.loginId, storedToken.loginId));
            throw new UnauthorizedException('User account is inactive or blocked');
        }

        // 3. Create new payload (exclude JWT temporal claims like iat, exp)
        const newPayload = {
            id: payload.id,
            email: payload.email,
            status: payload.status,
            rollId: payload.rollId,
            roll: payload.roll,
            jti: crypto.randomUUID(),
        };

        // 4. Generate new access and refresh tokens (Rotation)
        const newAccessToken = this.jwtService.sign(newPayload);
        const newRefreshToken = this.jwtService.sign(newPayload, {
            secret: refreshSecret,
            expiresIn: '7d',
        });
        
        const newHash = crypto.createHash('sha256').update(newRefreshToken).digest('hex');

        // 5. Update database with the new refresh token (Rotate)
        await this.db.update(schema.refreshToken).set({
            token: newHash,
            expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days
        }).where(eq(schema.refreshToken.id, storedToken.id));

        return {
            access_token: newAccessToken,
            refreshToken: newRefreshToken,
        };
    } catch (error) {
        throw new UnauthorizedException('Invalid or expired refresh token');
    }
}
```

### 2. Update `AuthController` in `src/auth/auth.controller.ts`
Expose the refresh endpoint:

```typescript
@Post('refresh')
async refresh(@Body('refreshToken') refreshToken: string) {
    if (!refreshToken) {
        throw new BadRequestException('Refresh token is required');
    }
    return await this.auth.refresh(refreshToken);
}
```

---

## 🌐 Step 2: Frontend Implementation (Axios Interceptors)

On the frontend, write an Axios instance with an **interceptor** to catch `401 Unauthorized` responses and silently refresh the token.

### Axios Client setup (e.g. `apiClient.ts` / `axiosInstance.js`):
```javascript
import axios from 'axios';

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
    failedQueue.forEach(prom => {
        if (error) {
            prom.reject(error);
        } else {
            prom.resolve(token);
        }
    });
    failedQueue = [];
};

const apiClient = axios.create({
    baseURL: 'http://localhost:3000', // Update to your API URL
});

// Request Interceptor: Attach Access Token to headers
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response Interceptor: Catch 401 and refresh
apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // If the error is 401 (Unauthorized) and the request has not been retried yet
        if (error.response?.status === 401 && !originalRequest._retry) {
            if (isRefreshing) {
                // Queue this request while token is being refreshed
                return new Promise((resolve, reject) => {
                    failedQueue.push({ resolve, reject });
                })
                .then((token) => {
                    originalRequest.headers['Authorization'] = `Bearer ${token}`;
                    return apiClient(originalRequest);
                })
                .catch((err) => Promise.reject(err));
            }

            originalRequest._retry = true;
            isRefreshing = true;

            const refreshToken = localStorage.getItem('refresh_token');
            if (!refreshToken) {
                // No refresh token, force logout
                handleLogout();
                return Promise.reject(error);
            }

            try {
                // Call backend to refresh tokens
                const response = await axios.post('http://localhost:3000/auth/refresh', {
                    refreshToken,
                });

                const { access_token, refreshToken: newRefreshToken } = response.data;

                // Save new tokens
                localStorage.setItem('access_token', access_token);
                localStorage.setItem('refresh_token', newRefreshToken);

                // Update headers and process queued requests
                apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
                processQueue(null, access_token);

                // Retry original request
                originalRequest.headers['Authorization'] = `Bearer ${access_token}`;
                return apiClient(originalRequest);
            } catch (refreshError) {
                // If refreshing fails, log out the user
                processQueue(refreshError, null);
                handleLogout();
                return Promise.reject(refreshError);
            } finally {
                isRefreshing = false;
            }
        }

        return Promise.reject(error);
    }
);

function handleLogout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login'; // Redirect to login page
}

export default apiClient;
```

---

## 🔑 Step 3: Setting Up Auto-Login

Auto-login checks if the user has a valid session when they open the application so they don't have to log in manually every time.

### Logic for the Frontend App (e.g., `App.js` or `index.js`):
1. On app startup (e.g., React `useEffect`), check if there is a `refresh_token` stored in `localStorage`.
2. If yes, request a new `access_token` using the refresh endpoint and fetch the user profile.
3. If no token exists, redirect/show the login screen.

Here is a standard example of how to implement it:

```javascript
import React, { useEffect, useState } from 'react';
import apiClient from './apiClient';

function App() {
    const [isLoading, setIsLoading] = useState(true);
    const [user, setUser] = useState(null);

    useEffect(() => {
        const attemptAutoLogin = async () => {
            const refreshToken = localStorage.getItem('refresh_token');
            
            if (!refreshToken) {
                setIsLoading(false);
                return; // User is guest
            }

            try {
                // 1. Silent token refresh to obtain a fresh access token
                const res = await apiClient.post('/auth/refresh', { refreshToken });
                const { access_token, refreshToken: newRefreshToken } = res.data;
                
                localStorage.setItem('access_token', access_token);
                localStorage.setItem('refresh_token', newRefreshToken);

                // 2. Fetch authenticated user profile using the new access token
                const profileRes = await apiClient.get('/auth/me'); // Create a GET /auth/me profile endpoint
                setUser(profileRes.data);
            } catch (err) {
                console.error('Auto login failed', err);
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
            } finally {
                setIsLoading(false);
            }
        };

        attemptAutoLogin();
    }, []);

    if (isLoading) {
        return <div>Loading application, please wait...</div>; // Splash screen
    }

    return (
        <div>
            {user ? <Dashboard user={user} /> : <LoginForm onLoginSuccess={setUser} />}
        </div>
    );
}
```

> [!NOTE]
> **Enhancing Security:** For production, storing refresh tokens in **HTTP-only Cookies** instead of `localStorage` protects you from Cross-Site Scripting (XSS) attacks. If you choose cookies, the frontend won't have to explicitly send the refresh token in the request body because the browser will automatically attach the cookie.


Here is a step-by-step breakdown of how the Auto-Login (Silent Login) mechanism works:
  ──────
  ### 1. The App Boots Up (On Page Load/Refresh)

  When the user visits your site (e.g., opens the page or refreshes), the frontend application initializes.

  • The frontend context or store (like Redux, Vuex, or React State) starts in an unauthenticated/loading state.
  • A splash screen/loading spinner is shown to the user to prevent the login screen from flickering.
  ──────
  ### 2. Checking for Stored Credentials

  The frontend immediately checks if a  refresh_token  exists in the browser's persistent storage (like  localStorage  or  cookies ):

  • No token found: The frontend hides the loading spinner and immediately redirects/renders the Login Page.
  • Token found: The frontend initiates a silent authentication handshake with the backend.
  ──────
  ### 3. The Silent Handshake

  Without the user typing anything or seeing a login form:

  1. The Request: The frontend sends a background request to your new  POST /auth/refresh  endpoint containing the stored  refresh_token .
  2. The Verification:
      • The backend validates the signature of the refresh token.
      • It hashes the token and compares it to the hash stored in your database.
      • Token Reuse Detection: If the token is mathematically valid but not in the database, it assumes the token was stolen and revokes ALL sessions for that user.
      • It checks that the current time has not passed the `expiresAt` date.
      • Active Status Validation: It queries the user from the database to ensure their account status is still exactly `active`.
  3. Token Rotation:
      • If valid and the user is active, the backend generates a brand-new access token (15-min expiry) and a new rotated refresh token (7-day expiry).
      • It updates the database with the new refresh token's hash.
      • It returns both tokens to the frontend.

  ──────
  ### 4. Fetching the User Profile & Restoring Session

  1. Update Storage: The frontend receives the new tokens, saves the new  access_token  in memory/state, and replaces the old  refresh_token 
  in  localStorage /cookies.
  2. Retrieve Profile: Using the new  access_token  in the headers ( Authorization: Bearer <token> ), the frontend makes a request to fetch the
  user's profile details (e.g.  GET /auth/me  or similar profile endpoint).
  3. Session Restored: Once the profile is fetched, the frontend updates its state with the user's data, hides the splash screen, and renders
  the user's dashboard.
  ──────
  ### 🚨 What happens if the Refresh Token is Expired?

  If the user hasn't visited the app for more than 7 days, the  refresh_token  in the database will be expired.

  • The backend will return a  401 Unauthorized  error.
  • The frontend catches this error in the boot phase, clears all stored tokens, hides the loading spinner, and redirects the user to the Login
  Page to sign in manually.


  ---
  ---