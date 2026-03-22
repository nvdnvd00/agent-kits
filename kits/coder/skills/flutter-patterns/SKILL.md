---
name: flutter-patterns
description: Flutter development with Dart 3, widget composition, state management, and multi-platform deployment. Use when building mobile, web, desktop apps with Flutter. Covers Riverpod, Bloc, performance, and testing.
allowed-tools: Read, Write, Edit, Bash
version: 1.0
priority: MEDIUM
---

# Flutter Patterns - Cross-Platform Development Excellence

## ⚡ Quick Reference

- **Widgets**: `const` constructors everywhere · `StatelessWidget` by default · `StatefulWidget` only for local state
- **State**: Local → `setState` · Feature-wide → Riverpod · App-wide → Riverpod Provider
- **Performance**: `const` widgets skip rebuilds · `RepaintBoundary` for heavy paths · ListView.builder for long lists
- **Navigation**: GoRouter for complex routing · Named routes · Pass data via constructor not global
- **Async**: `FutureBuilder`/`StreamBuilder` · Handle loading/error states always · `ref.watch()` for Riverpod
- **Testing**: Widget tests for UI · Unit tests for logic · Integration tests for flows on real device

---


---

## 🎯 Core Principles

| Principle          | Rule                                             |
| ------------------ | ------------------------------------------------ |
| **Composition**    | Compose widgets, don't inherit                   |
| **Immutability**   | Use `const` constructors for optimal performance |
| **Null Safety**    | Dart 3 null safety is mandatory                  |
| **Platform Aware** | One codebase, platform-specific polish           |
| **Test First**     | Widget tests, integration tests, golden tests    |

```
❌ WRONG: Create God widgets with everything
✅ CORRECT: Small, focused, reusable widget compositions
```

---

## 📁 Project Structure

```
lib/
├── app/                    # App configuration
│   ├── router.dart         # GoRouter configuration
│   └── theme.dart          # Theme tokens
├── features/               # Feature modules
│   ├── auth/
│   │   ├── data/           # Repositories, data sources
│   │   ├── domain/         # Entities, use cases
│   │   └── presentation/   # Widgets, pages, state
│   └── home/
├── shared/                 # Shared components
│   ├── widgets/            # Reusable UI components
│   ├── utils/              # Utilities
│   └── extensions/         # Dart extensions
└── main.dart               # App entry point
```

---

## 🏗️ State Management Selection

| Solution          | Best For                          | Complexity  |
| ----------------- | --------------------------------- | ----------- |
| **Riverpod**      | Medium-large apps, compile safety | Medium-High |
| **Bloc/Cubit**    | Event-driven, testable flows      | Medium      |
| **Provider**      | Simple apps, shared state         | Low         |
| **GetX**          | Rapid prototyping                 | Low         |
| **Flutter Hooks** | Simple local state                | Low         |

### Decision Tree

```
Need complex business logic?
├── Yes → Need event-driven architecture?
│         ├── Yes → Bloc
│         └── No → Riverpod
└── No → Simple state sharing?
         ├── Yes → Provider or Riverpod
         └── No → setState or Hooks
```

---

## 📦 Riverpod Pattern (Recommended)

```dart
// providers/auth_provider.dart
@riverpod
class Auth extends _$Auth {
  @override
  AuthState build() => const AuthState.unauthenticated();

  Future<void> signIn(String email, String password) async {
    state = const AuthState.loading();
    try {
      final user = await ref.read(authRepositoryProvider).signIn(email, password);
      state = AuthState.authenticated(user);
    } catch (e) {
      state = AuthState.error(e.toString());
    }
  }

  Future<void> signOut() async {
    await ref.read(authRepositoryProvider).signOut();
    state = const AuthState.unauthenticated();
  }
}

// Usage in widget
class LoginPage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authProvider);

    return authState.when(
      authenticated: (user) => HomePage(user: user),
      unauthenticated: () => LoginForm(),
      loading: () => const LoadingIndicator(),
      error: (message) => ErrorDisplay(message: message),
    );
  }
}
```

---

## 🎨 Widget Patterns

### Const Constructor Rule

```dart
// ✅ GOOD - Const constructor
class ActionButton extends StatelessWidget {
  const ActionButton({
    super.key,
    required this.label,
    required this.onPressed,
  });

  final String label;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      child: Text(label),
    );
  }
}

// ❌ BAD - No const constructor
class ActionButton extends StatelessWidget {
  ActionButton({required this.label, required this.onPressed});
  // ...
}
```

### Widget Keys

| Scenario                   | Key Type          |
| -------------------------- | ----------------- |
| List items with unique IDs | `ValueKey(id)`    |
| Animated list items        | `ObjectKey(item)` |
| Form fields                | `GlobalKey`       |
| Never needs identity       | No key            |

```dart
ListView.builder(
  itemBuilder: (context, index) {
    final item = items[index];
    return ProductCard(
      key: ValueKey(item.id),  // Stable identity
      product: item,
    );
  },
)
```

---

## 🚀 Performance Optimization

### Widget Rebuild Prevention

| Technique            | When to Use                        |
| -------------------- | ---------------------------------- |
| `const` constructors | Always when possible               |
| `Consumer` widgets   | Scope Riverpod rebuilds            |
| `select` in Riverpod | Watch only needed parts            |
| `RepaintBoundary`    | Isolate expensive paint operations |
| `ListView.builder`   | Large lists (virtualized)          |

### Image Optimization

```dart
// Use cached_network_image
CachedNetworkImage(
  imageUrl: url,
  placeholder: (context, url) => const Shimmer(),
  errorWidget: (context, url, error) => const Icon(Icons.error),
  memCacheWidth: 300,  // Limit memory cache size
)

// For assets, use appropriate resolution
Image.asset(
  'assets/images/logo.png',
  width: 100,
  height: 100,
  cacheWidth: 200,  // 2x for retina
)
```

### Isolates for Heavy Work

```dart
// Run CPU-intensive work in isolate
final result = await compute(heavyComputation, data);

// Or use Isolate.spawn for more control
Future<void> processLargeData(List<Data> data) async {
  final receivePort = ReceivePort();
  await Isolate.spawn(
    _processInIsolate,
    (data, receivePort.sendPort),
  );
  return await receivePort.first;
}
```

---

## 🧪 Testing Patterns

### Widget Tests

```dart
testWidgets('LoginForm submits credentials', (tester) async {
  await tester.pumpWidget(
    const ProviderScope(
      child: MaterialApp(home: LoginForm()),
    ),
  );

  await tester.enterText(find.byKey(const Key('email')), 'test@email.com');
  await tester.enterText(find.byKey(const Key('password')), 'password');
  await tester.tap(find.text('Sign In'));
  await tester.pump();

  expect(find.byType(CircularProgressIndicator), findsOneWidget);
});
```

### Golden Tests

```dart
testWidgets('ProductCard matches golden', (tester) async {
  await tester.pumpWidget(
    const MaterialApp(
      home: ProductCard(product: mockProduct),
    ),
  );

  await expectLater(
    find.byType(ProductCard),
    matchesGoldenFile('goldens/product_card.png'),
  );
});
```

---

## 📱 Platform-Specific Code

```dart
// Use Platform for runtime checks
if (Platform.isIOS) {
  // iOS-specific code
} else if (Platform.isAndroid) {
  // Android-specific code
}

// Or use kIsWeb for web detection
if (kIsWeb) {
  // Web-specific code
}

// Use .ios.dart / .android.dart for file-based separation
// lib/widgets/button.dart        -> Default
// lib/widgets/button.ios.dart    -> iOS override
// lib/widgets/button.android.dart -> Android override
```

---

## 🚨 Anti-Patterns

| ❌ Don't                         | ✅ Do                                 |
| -------------------------------- | ------------------------------------- |
| Inherit from StatelessWidget/ful | Compose widgets                       |
| Skip `const` constructors        | Add `const` everywhere possible       |
| setState in large widgets        | Use state management solution         |
| Fetch data in build()            | Use FutureBuilder or state management |
| Large build() methods            | Extract smaller widget functions      |
| Hardcode colors/sizes            | Use Theme and design tokens           |
| Skip null safety                 | Embrace Dart 3 null safety            |
| Test only happy paths            | Test edge cases and errors            |

---

## ✅ Self-Check Before Completing

| Check               | Question                                |
| ------------------- | --------------------------------------- |
| ✅ **Const?**       | Are const constructors used everywhere? |
| ✅ **Keys?**        | Do list items have stable keys?         |
| ✅ **State?**       | Is state management properly scoped?    |
| ✅ **Null safe?**   | Is null safety properly handled?        |
| ✅ **Tested?**      | Are widgets and logic tested?           |
| ✅ **Platform?**    | Tested on both iOS and Android?         |
| ✅ **Performance?** | No jank, smooth scrolling?              |

---

## 🔗 Related Skills

| Need                    | Skill                   |
| ----------------------- | ----------------------- |
| React Native comparison | `react-native-patterns` |
| Mobile design           | `mobile-design`         |
| Testing patterns        | `testing-patterns`      |
| Performance profiling   | `performance-profiling` |

---

> **Remember:** Flutter's power is in composition. Small, focused widgets that compose together create maintainable, testable, and performant apps.
