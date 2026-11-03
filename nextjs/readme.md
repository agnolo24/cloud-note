# Next.js

## Creation and configuring Nextjs application
```
npx create-next-app@latest my-app --yes
cd my-app
npm run dev
```

- **--yes**  skips prompts using saved preferences or defaults. The default setup enables TypeScript, Tailwind CSS, ESLint, App Router, and Turbopack, with import alias @/*, and includes AGENTS.md to guide coding agents to write up-to-date Next.js code.

- when running the project by default it will run in the port 3000 if we need to change it we need to use
  ' -p 4000' in heat 4000 is the new port address the implementation is shown in the given image
  ![alt text](image.png)

## Now let's clean up the default Next.js boilerplate and keep only what we need
we are going to edit the 'app/global.css', 'app/layout.tsx', 'app/page.tsx', and remove every image in the 'public'
folder as given bellow

![img.png](img.png)

![img_1.png](img_1.png)

![img_2.png](img_2.png)

**we are completely removing the given files**
![img_3.png](img_3.png)


## Understanding the `app` folder

A cleaned-up Next.js project may look like this:

```text
project/
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── public/
├── package.json
└── next.config.ts
```

The `app` folder is one of the most important parts of Next.js. It uses **file-system-based routing**.

**In simple terms:** The folders and special files you create determine which URLs exist in your application.

Unlike a React application using React Router, you do not have to manually configure every route. Next.js uses the directory structure to define routes.

---

## What is `page.tsx`?

A `page.tsx` file defines the UI shown at a particular URL.

**File: `app/page.tsx`**

```tsx
export default function Home() {
  return (
    <div>
      <h1>Welcome to Next.js</h1>
    </div>
  );
}
```

Open:

```text
http://localhost:3000
```

Next.js finds `app/page.tsx` and renders its default-exported component.

```text
app/page.tsx  ──────>  http://localhost:3000/
```

**Remember:**

- `page.tsx` is a **special filename** in the App Router.
- `app/page.tsx` is the homepage (`/`).
- An ordinary component file such as `Home.tsx` does **not** automatically create a route.
- A route becomes a navigable page when its segment has a `page.tsx` file.

---

## Creating another page

Let's create an **About** page.

Inside the `app` directory, create an `about` folder with a `page.tsx` file:

```text
app/
├── layout.tsx
├── page.tsx
└── about/
    └── page.tsx
```

**File: `app/about/page.tsx`**

```tsx
export default function About() {
  return (
    <div>
      <h1>About Page</h1>
      <p>This is my first additional route.</p>
    </div>
  );
}
```

Now visit:

```text
http://localhost:3000/about
```

You should see:

```text
About Page
This is my first additional route.
```

### How does Next.js create the URL?

Each regular folder within `app` represents a **route segment**. A `page.tsx` file inside that folder defines the page shown at its URL.

| File | URL |
| --- | --- |
| `app/page.tsx` | `/` |
| `app/about/page.tsx` | `/about` |
| `app/contact/page.tsx` | `/contact` |
| `app/dashboard/page.tsx` | `/dashboard` |
| `app/dashboard/settings/page.tsx` | `/dashboard/settings` |

**Important:** Creating the `about` folder alone does not make `/about` a page. To visit `/about` as a page, define `app/about/page.tsx`.

---

## What is `layout.tsx`?

Imagine an application with five pages. You want the same navigation bar and footer on every page.

Without shared layouts, you might copy the header and footer into every page. Next.js avoids that repetition with **layouts**.

A `layout.tsx` file defines shared UI that wraps pages (and nested layouts) beneath it.

**File: `app/layout.tsx`**

```tsx
import type { ReactNode } from "react";
import "./globals.css";

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <header>
          <h1>My Website</h1>
        </header>

        {children}

        <footer>
          <p>Copyright 2026</p>
        </footer>
      </body>
    </html>
  );
}
```

The root layout wraps the app's pages. The header and footer appear around whichever page is currently being shown.

**Note:** In the App Router, the root layout must contain `<html>` and `<body>`.

### What is `children`?

`children` is a standard React prop. It represents the content placed inside a component.

**Example in React:**

```tsx
import type { ReactNode } from "react";

function Container({ children }: { children: ReactNode }) {
  return <div>{children}</div>;
}
```

When you use:

```tsx
<Container>
  <h1>Hello</h1>
</Container>
```

The `<h1>Hello</h1>` element becomes `Container`'s `children`.

**In Next.js:** When someone visits `/about`, the About page is rendered in the root layout's `{children}` position.

```text
RootLayout
┌──────────────────────────────────┐
│ Header: My Website               │
│                                  │
│ {children}                       │
│   ┌──────────────────────────┐   │
│   │ About Page               │   │
│   │ This is my first ...     │   │
│   └──────────────────────────┘   │
│                                  │
│ Footer: Copyright 2026           │
└──────────────────────────────────┘
```

Shared layouts are preserved during client-side navigation between pages using the same layout, helping retain layout state rather than remounting the layout each time.

---

## Nested layouts

Suppose you are building an admin dashboard. You want a sidebar on all dashboard pages, but not on public pages.

Create a layout specifically for the `dashboard` folder:

```text
app/
├── layout.tsx                  # Root layout
├── page.tsx                    # /
└── dashboard/
    ├── layout.tsx              # Shared dashboard layout
    ├── page.tsx                # /dashboard
    └── settings/
        └── page.tsx            # /dashboard/settings
```

**File: `app/dashboard/layout.tsx`**

```tsx
import type { ReactNode } from "react";

export default function DashboardLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <div>
      <aside>Dashboard Sidebar</aside>
      <main>{children}</main>
    </div>
  );
}
```

When someone visits `/dashboard/settings`, Next.js composes these components:

```text
RootLayout
└── DashboardLayout
    └── SettingsPage
```

This means:

- The root layout surrounds the whole application.
- The dashboard layout surrounds dashboard pages only.
- The settings page appears in the dashboard layout's `{children}` position.

**Real-world use:** Different areas of an application can have different shared UI—for example, a public website, staff dashboard, and manager portal.

---

## Route Groups — Organizing routes with `()`

So far, we've learned that normal folders inside `app` usually become parts of the URL. **Route Groups** are an exception.

To create a route group, wrap the folder name in parentheses:

```text
(main)
(auth)
(marketing)
```

**The name inside `()` does NOT appear in the URL.** This lets us organize related pages and give different sections their own layouts without changing their public URLs.

### 1. Route groups do not change URLs

Consider this structure:

```text
app/
├── layout.tsx
├── (main)/
│   ├── page.tsx
│   ├── about/
│   │   └── page.tsx
│   └── contact/
│       └── page.tsx
└── (auth)/
    ├── login/
    │   └── page.tsx
    └── register/
        └── page.tsx
```

| File | URL |
| --- | --- |
| `app/(main)/page.tsx` | `/` |
| `app/(main)/about/page.tsx` | `/about` |
| `app/(main)/contact/page.tsx` | `/contact` |
| `app/(auth)/login/page.tsx` | `/login` |
| `app/(auth)/register/page.tsx` | `/register` |

**Remember:** A route group is for organizing the code. It does not automatically create a page or URL. You still need `page.tsx` to render a page.

### 2. Using route groups to show different headers and footers

Suppose you want:

- The **Home** and **Blog** pages to show a *Main Header* and *Main Footer*.
- The **About** and **Company** pages to show an *About Header* and *About Footer*.
- All pages to share the same document-level root layout.

Use the following structure:

```text
app/
├── globals.css
├── layout.tsx                 # Root: html + body only
├── (main)/
│   ├── layout.tsx             # Main Header + Footer
│   ├── page.tsx               # /
│   └── blog/
│       └── page.tsx          # /blog
└── about/
    ├── layout.tsx             # About Header + Footer
    ├── page.tsx               # /about
    └── company/
        └── page.tsx          # /about/company
```

**File: `app/layout.tsx` (shared Root Layout)**

```tsx
import type { ReactNode } from "react";
import "./globals.css";

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

The Root Layout has no visible header or footer, but it still wraps **every** route.

**File: `app/(main)/layout.tsx`**

```tsx
import type { ReactNode } from "react";

export default function MainLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <div>
      <header>Main Header</header>
      <main>{children}</main>
      <footer>Main Footer</footer>
    </div>
  );
}
```

**File: `app/about/layout.tsx`**

```tsx
import type { ReactNode } from "react";

export default function AboutLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <div>
      <header>About Header</header>
      <main>{children}</main>
      <footer>About Footer</footer>
    </div>
  );
}
```

**File: `app/about/company/page.tsx`**

```tsx
export default function Company() {
  return <p>This is the Company page.</p>;
}
```

When visiting `/about/company`, the layout hierarchy is:

```text
RootLayout (app/layout.tsx)
└── AboutLayout (app/about/layout.tsx)
    └── Company Page (app/about/company/page.tsx)
```

**Visible result:**

```text
About Header
This is the Company page.
About Footer
```

The **Main Header** and **Main Footer** are not shown because the About route is **outside** `(main)`. However, the **Root Layout still renders**.

> **Important:** Route groups do not cancel or skip a parent layout. They let us decide which pages share a *group-specific* layout. This approach is usually best when we want one shared Root Layout and different UI for different sections.

### 3. Can we skip the Root Layout completely?

Not if a shared `app/layout.tsx` exists: every page beneath `app` inherits it. But Next.js does support **multiple independent Root Layouts**.

To use this approach, remove the top-level `app/layout.tsx` and give each top-level section its own root layout:

```text
app/
├── globals.css
├── (main)/
│   ├── layout.tsx             # Main Root Layout
│   ├── page.tsx               # /
│   └── blog/
│       └── page.tsx
└── about/
    ├── layout.tsx             # About Root Layout
    ├── page.tsx               # /about
    └── company/
        └── page.tsx          # /about/company
```

Now `app/(main)/layout.tsx` and `app/about/layout.tsx` are **root layouts** for separate sections. **Both** must contain `<html>` and `<body>`.

**Example: `app/about/layout.tsx` as an independent Root Layout**

```tsx
import type { ReactNode } from "react";
import "../globals.css";

export default function AboutRootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <header>About Header</header>
        {children}
        <footer>About Footer</footer>
      </body>
    </html>
  );
}
```

The Main Root Layout must also define `<html>` and `<body>` and should import the shared CSS if needed. The homepage `/` must belong to one of these sections (such as `app/(main)/page.tsx`).

**Tradeoff:** Navigating between pages with different root layouts causes a **full page load**, unlike navigation within one shared root layout.

### 4. Important rules and common mistakes

| Rule | Explanation |
| --- | --- |
| Use `(name)` | Parentheses mark a route group; the group name is omitted from the URL. |
| Don't create duplicate URLs | `app/(main)/about/page.tsx` and `app/(other)/about/page.tsx` both map to `/about` and conflict. |
| Avoid two homepages | Don't keep both `app/page.tsx` and `app/(main)/page.tsx` because both map to `/`. |
| A shared root is still inherited | `app/layout.tsx` wraps pages even if the pages are inside route groups. |
| Root layouts require `<html>` and `<body>` | Nested layouts must not create another `<html>` or `<body>`. |
| Each `layout.tsx` needs a React component | The default export must be a valid component that renders its `children` where appropriate. |
| The URL ignores route groups | To link to `app/(main)/blog/page.tsx`, use `<Link href="/blog">`, not `/main/blog`. |

### Quick comparison

| Setup | Layouts for `/about/company` | Best for |
| --- | --- | --- |
| One shared `app/layout.tsx` | Root Layout → About Layout → Company Page | Most applications; separate section UI without a full reload between roots. |
| Multiple Root Layouts (no `app/layout.tsx`) | About Root Layout → Company Page | Sections needing fully separate document-level layouts. |

**Practice:** Place your homepage in `(main)`, keep the About/Company pages outside that group, and check that `/about/company` shows only the **About Header**, **Company Page**, and **About Footer**—while still using the shared Root Layout.

**Official documentation:** [Next.js Route Groups](https://nextjs.org/docs/app/api-reference/file-conventions/route-groups) and [Next.js Layouts](https://nextjs.org/docs/app/api-reference/file-conventions/layout).

---

## Navigation using `Link`

Next.js provides a `Link` component for navigating between internal pages.

Import it with:

```tsx
import Link from "next/link";
```

**File: `app/page.tsx`**

```tsx
import Link from "next/link";

export default function Home() {
  return (
    <main>
      <h1>Home Page</h1>
      <p>Welcome to my application.</p>

      <Link href="/about">Go to About</Link>
    </main>
  );
}
```

Clicking **Go to About** navigates to `/about`.

### Why use `Link` rather than `<a>` for internal routes?

- `Link` supports optimized **client-side navigation**.
- Next.js can **prefetch** linked routes to make navigation feel faster.
- It works naturally with shared App Router layouts.

A regular `<a>` tag is still useful for external links or when a full-page navigation is intentionally needed.

**Note:** You do **not** need to add `"use client"` just to render a `Link`.

---

## Other important Next.js files

You'll encounter these special filenames as you learn more:

| File | What it does |
| --- | --- |
| `page.tsx` | Defines the page for a URL. |
| `layout.tsx` | Defines UI shared across pages in a route segment. |
| `loading.tsx` | Defines loading UI for a route segment. |
| `error.tsx` | Defines an error boundary UI for a route segment. |
| `not-found.tsx` | Defines a not-found UI. |
| `route.ts` | Defines HTTP request handlers (such as `GET` and `POST`). |
| `template.tsx` | Similar to a layout, but creates a new instance on navigation. |

You don't need to master every file now. We'll learn them one at a time as they become relevant.

---

## Quick revision

| Concept | Remember |
| --- | --- |
| `app/` | Contains routes and shared route UI in the App Router. |
| `page.tsx` | Defines an actual page at a URL. |
| Folders | Usually correspond to URL segments. |
| `layout.tsx` | Wraps pages and nested layouts with shared UI. |
| `children` | The nested page or layout rendered within a layout. |
| Nested layouts | Let sections like `/dashboard` have their own shared UI. |
| Route groups `(name)` | Organize pages and give sections different layouts without adding the group name to URLs. |
| Multiple Root Layouts | Separate root layouts for different sections when there is no shared top-level `app/layout.tsx`. |
| `Link` | Provides optimized internal navigation. |

### Important takeaway

```text
app/page.tsx                        -> /
app/about/page.tsx                  -> /about
app/dashboard/page.tsx              -> /dashboard
app/dashboard/settings/page.tsx     -> /dashboard/settings
```

And layouts compose from outermost to innermost:

```text
app/layout.tsx -> app/dashboard/layout.tsx -> app/dashboard/settings/page.tsx
```

---

## Practice quiz

**1. Which file defines the homepage in an App Router application?**

A. `app/index.tsx`  
B. `app/page.tsx`  
C. `app/home.tsx`

**2. What URL does `app/products/details/page.tsx` create?**

A. `/products`  
B. `/products/details`  
C. `/details/page`

**3. What does the `children` prop represent in a layout?**

A. The current nested page or layout  
B. A database record  
C. The current URL string

### Answers

1. **B** — `app/page.tsx` maps to `/`.
2. **B** — Each folder contributes a URL segment.
3. **A** — The nested page or layout renders inside `{children}`.

---

## Coding exercise

**Task:** Create a Contact page and link to it from the homepage.

1. Create `app/contact/page.tsx`.
2. Add a heading such as `Contact Page`.
3. Import `Link` from `next/link` in `app/page.tsx`.
4. Add a link to `/contact`.
5. Run `npm run dev` and visit `http://localhost:3000/contact`.
6. Leave `app/layout.tsx` unchanged.

**Expected folder structure:**

```text
app/
├── globals.css
├── layout.tsx
├── page.tsx
├── about/
│   └── page.tsx
└── contact/
    └── page.tsx
```

---

## What's next?

**Lesson 3 — Dynamic Routes, Route Parameters, and Nested Routing**

You'll learn how one file can handle URLs such as:

```text
/users/1
/users/2
/users/3
```

using a dynamic segment, such as `app/users/[id]/page.tsx`.
