---
name: graphql-patterns
description: GraphQL API design, schema patterns, and performance optimization. Use when designing GraphQL schemas, implementing resolvers, preventing N+1 queries, or building federated architectures.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 2.0
---

# GraphQL Patterns - API Design & Performance

> **Philosophy:** GraphQL is a contract, not just an API. The schema IS documentation. Design it carefully.

---

## When to Use This Skill

| ✅ Use                      | ❌ Don't Use                     |
| --------------------------- | -------------------------------- |
| Schema design               | REST API design                  |
| Resolver implementation     | Database queries (use ORM)       |
| N+1 prevention (DataLoader) | Client-side caching (use Apollo) |
| Federation architecture     | Simple CRUD APIs                 |
| Real-time subscriptions     | File uploads as primary use      |
| Query optimization          | Rate limiting (use middleware)   |

➡️ For REST patterns, see `api-patterns` skill.

---

## Core Rules (Non-Negotiable)

1. **DataLoader mandatory** - Every resolver with DB calls needs DataLoader
2. **Depth limiting required** - Prevent deep query attacks
3. **Explicit nullability** - Design nullability intentionally
4. **Auth in resolvers** - Never rely on schema directives alone
5. **Disable introspection** - Production must disable introspection

---

## Schema Design Principles

### Type Design

```graphql
# ✅ Good: Explicit nullability, clear types
type User {
  id: ID! # Always non-null
  email: String! # Required field
  name: String!
  bio: String # Optional (nullable)
  avatar: String
  posts(first: Int): [Post!]! # List of non-null posts, list itself non-null
  createdAt: DateTime!
}

# ✅ Good: Input types for mutations
input CreateUserInput {
  email: String!
  name: String!
  bio: String
}

input UpdateUserInput {
  name: String
  bio: String
}
```

### Nullability Strategy

| Pattern      | Meaning                             |
| ------------ | ----------------------------------- |
| `String`     | May be null (optional field)        |
| `String!`    | Never null (required)               |
| `[String]`   | List may be null, items may be null |
| `[String]!`  | List never null, items may be null  |
| `[String!]`  | List may be null, items never null  |
| `[String!]!` | List never null, items never null   |

**Recommendation:** Use `[Type!]!` for lists (empty list over null).

### Relay Connection Pattern

```graphql
type Query {
  users(
    first: Int
    after: String
    last: Int
    before: String
    filter: UserFilter
  ): UserConnection!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  cursor: String!
  node: User!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

---

## DataLoader Pattern (N+1 Prevention)

### The Problem

```typescript
// ❌ N+1: Each user triggers separate DB query
const resolvers = {
  Post: {
    author: (post) => db.users.findById(post.authorId), // N queries!
  },
};
```

### The Solution

```typescript
import DataLoader from "dataloader";

// Create loader (per-request)
function createLoaders() {
  return {
    userLoader: new DataLoader(async (userIds: string[]) => {
      const users = await db.users.findByIds(userIds);
      // MUST return in same order as input
      return userIds.map((id) => users.find((u) => u.id === id) || null);
    }),

    postsByUserLoader: new DataLoader(async (userIds: string[]) => {
      const posts = await db.posts.findByUserIds(userIds);
      // Group by userId
      return userIds.map((id) => posts.filter((p) => p.authorId === id));
    }),
  };
}

// Use in resolver
const resolvers = {
  Post: {
    author: (post, _, { loaders }) => loaders.userLoader.load(post.authorId),
  },
  User: {
    posts: (user, _, { loaders }) => loaders.postsByUserLoader.load(user.id),
  },
};

// Context creation
const context = ({ req }) => ({
  loaders: createLoaders(),
  user: getUserFromToken(req),
});
```

### DataLoader Rules

1. **Create per-request** - New instance for each GraphQL request
2. **Batch must match order** - Return results in exact input order
3. **Handle missing items** - Return null for not-found
4. **Key uniqueness** - Convert to string if complex keys

---

## Query Optimization

### Depth Limiting

```typescript
import depthLimit from "graphql-depth-limit";

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(10)], // Max 10 levels deep
});
```

### Query Complexity

```typescript
import { createComplexityLimitRule } from "graphql-validation-complexity";

const complexityLimitRule = createComplexityLimitRule(1000, {
  onCost: (cost) => console.log("Query cost:", cost),
  scalarCost: 1,
  objectCost: 2,
  listFactor: 10,
});

const server = new ApolloServer({
  validationRules: [complexityLimitRule],
});
```

### Field Cost Analysis

```graphql
type Query {
  users(first: Int): [User!]! @cost(complexity: 10, multipliers: ["first"])
  user(id: ID!): User @cost(complexity: 1)
}

type User {
  id: ID!
  name: String!
  posts: [Post!]! @cost(complexity: 5) # More expensive field
}
```

---

## Authorization Patterns

### Resolver-Level Auth (Recommended)

```typescript
const resolvers = {
  Query: {
    user: async (_, { id }, { user }) => {
      if (!user) throw new AuthenticationError("Not authenticated");

      const targetUser = await db.users.findById(id);

      // Authorization logic
      if (user.role !== "admin" && user.id !== id) {
        throw new ForbiddenError("Not authorized");
      }

      return targetUser;
    },
  },

  User: {
    email: (user, _, { currentUser }) => {
      // Field-level authorization
      if (currentUser?.id === user.id || currentUser?.role === "admin") {
        return user.email;
      }
      return null; // Hide from unauthorized users
    },
  },
};
```

### Directive-Based Auth (Supplement, not replace)

```graphql
directive @auth(requires: Role = USER) on FIELD_DEFINITION
directive @owner on FIELD_DEFINITION

type Query {
  users: [User!]! @auth(requires: ADMIN)
  me: User @auth
}

type User {
  id: ID!
  name: String!
  email: String! @owner # Only owner can see
  secretField: String @auth(requires: ADMIN)
}
```

---

## Error Handling

### Structured Errors

```typescript
class UserInputError extends Error {
  constructor(
    message: string,
    public extensions: Record<string, any>,
  ) {
    super(message);
  }
}

const resolvers = {
  Mutation: {
    createUser: async (_, { input }) => {
      const errors: Record<string, string> = {};

      if (!isValidEmail(input.email)) {
        errors.email = "Invalid email format";
      }

      if (Object.keys(errors).length > 0) {
        throw new UserInputError("Validation failed", {
          validationErrors: errors,
          code: "VALIDATION_ERROR",
        });
      }

      return db.users.create(input);
    },
  },
};
```

### Union Types for Errors

```graphql
type Mutation {
  createUser(input: CreateUserInput!): CreateUserResult!
}

union CreateUserResult = User | ValidationError | EmailTakenError

type ValidationError {
  message: String!
  field: String!
}

type EmailTakenError {
  message: String!
  suggestedEmail: String
}
```

---

## Subscriptions

### Basic Subscription

```typescript
import { PubSub } from "graphql-subscriptions";

const pubsub = new PubSub();

const resolvers = {
  Mutation: {
    sendMessage: async (_, { input }, { user }) => {
      const message = await db.messages.create({
        ...input,
        authorId: user.id,
      });

      // Publish event
      pubsub.publish(`CHAT_${input.chatId}`, {
        messageSent: message,
      });

      return message;
    },
  },

  Subscription: {
    messageSent: {
      subscribe: (_, { chatId }, { user }) => {
        // Auth check
        if (!user) throw new AuthenticationError("Not authenticated");

        return pubsub.asyncIterator(`CHAT_${chatId}`);
      },
    },
  },
};
```

### Filtered Subscriptions

```typescript
import { withFilter } from "graphql-subscriptions";

const resolvers = {
  Subscription: {
    messageSent: {
      subscribe: withFilter(
        () => pubsub.asyncIterator("MESSAGE_CREATED"),
        (payload, variables, context) => {
          // Only deliver to users in the chat
          return (
            payload.messageSent.chatId === variables.chatId &&
            context.user.chats.includes(variables.chatId)
          );
        },
      ),
    },
  },
};
```

---

## Federation Pattern

### Subgraph Schema

```graphql
# Users Service
type User @key(fields: "id") {
  id: ID!
  name: String!
  email: String!
}

extend type Query {
  user(id: ID!): User
  me: User
}

# Posts Service
type Post @key(fields: "id") {
  id: ID!
  title: String!
  content: String!
  author: User!
}

# Extend User from Users Service
extend type User @key(fields: "id") {
  id: ID! @external
  posts: [Post!]!
}
```

### Reference Resolver

```typescript
// Posts service resolves User reference
const resolvers = {
  User: {
    __resolveReference: (user) => {
      // user contains { id } from key
      return { id: user.id }; // Minimal stub, Users service fills rest
    },
    posts: (user) => db.posts.findByAuthorId(user.id),
  },
};
```

---

## Caching Strategies

### CDN/Response Caching

```typescript
const resolvers = {
  Query: {
    // Public, cacheable
    products: () => db.products.findAll(),
  },

  Product: {
    __cacheControl: { maxAge: 3600, scope: "PUBLIC" },
  },

  User: {
    __cacheControl: { maxAge: 0, scope: "PRIVATE" },
    email: {
      __cacheControl: { maxAge: 0 }, // Never cache sensitive data
    },
  },
};
```

### Automatic Persisted Queries (APQ)

```typescript
import { ApolloServer } from "@apollo/server";

const server = new ApolloServer({
  typeDefs,
  resolvers,
  persistedQueries: {
    ttl: 900, // 15 minutes
  },
});
```

---

## Production Security Checklist

```typescript
const server = new ApolloServer({
  typeDefs,
  resolvers,

  // ✅ Disable introspection in production
  introspection: process.env.NODE_ENV !== "production",

  // ✅ Disable playground in production
  playground: process.env.NODE_ENV !== "production",

  // ✅ Validation rules
  validationRules: [depthLimit(10), createComplexityLimitRule(1000)],

  // ✅ Error formatting (hide internal details)
  formatError: (error) => {
    if (process.env.NODE_ENV === "production") {
      return { message: error.message };
    }
    return error;
  },
});
```

---

## Anti-Patterns

| ❌ Don't                              | ✅ Do                                       |
| ------------------------------------- | ------------------------------------------- |
| Resolver makes DB call without loader | Use DataLoader for all DB access            |
| All fields nullable                   | Design nullability intentionally            |
| Auth only in directives               | Auth in resolvers, directives as supplement |
| Introspection in production           | Disable introspection                       |
| Deep unlimited queries                | Depth limiting + complexity analysis        |
| Return all errors as same type        | Use union types for error variants          |
| Create DataLoader once globally       | Create per-request                          |
| Subscription without auth check       | Check auth in subscribe function            |

---

## Performance Checklist

Before production:

- [ ] DataLoader for all nested resolvers?
- [ ] Depth limit configured?
- [ ] Query complexity analysis?
- [ ] Introspection disabled?
- [ ] Error details hidden in production?
- [ ] Subscription auth implemented?
- [ ] Persisted queries enabled?
- [ ] Cache headers set appropriately?

---

## Related Skills

| Need                   | Skill                 |
| ---------------------- | --------------------- |
| REST API design        | `api-patterns`        |
| Database queries       | `database-design`     |
| Real-time patterns     | `realtime-patterns`   |
| TypeScript integration | `typescript-patterns` |

---

> **Remember:** GraphQL's flexibility is its power and danger. Protect your API with DataLoader, depth limits, and auth at every level.
