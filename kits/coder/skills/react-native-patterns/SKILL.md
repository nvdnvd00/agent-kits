---
name: react-native-patterns
description: React Native with Expo development patterns. Use when building mobile apps with React Native, implementing navigation, native modules, or offline-first architecture. Covers Expo Router, EAS Build, and performance.
allowed-tools: Read, Write, Edit, Bash
version: 1.0
priority: MEDIUM
---

# React Native Patterns - Mobile Excellence with Expo

> **Philosophy:** Use Expo unless you have a very specific reason not to. OTA updates, managed native code, and faster development are worth the trade-offs.

---

## 🎯 Core Principles

| Principle          | Rule                                                  |
| ------------------ | ----------------------------------------------------- |
| **Expo First**     | Start with Expo, eject only when absolutely necessary |
| **Platform Aware** | One codebase, platform-specific polish                |
| **Offline Ready**  | Assume network is unreliable                          |
| **Performance**    | FlashList, memoization, native thread animations      |
| **Type Safe**      | TypeScript is mandatory                               |

```
❌ WRONG: Bare React Native for simple apps
✅ CORRECT: Expo with EAS Build, eject later if needed
```

---

## 📁 Project Structure

```
src/
├── app/                    # Expo Router screens
│   ├── (auth)/             # Auth group
│   │   ├── login.tsx
│   │   └── register.tsx
│   ├── (tabs)/             # Tab navigation
│   │   ├── _layout.tsx
│   │   ├── index.tsx
│   │   └── profile.tsx
│   └── _layout.tsx         # Root layout
├── components/
│   ├── ui/                 # Reusable UI components
│   └── features/           # Feature-specific components
├── hooks/                  # Custom hooks
├── services/               # API and native services
├── stores/                 # State management
├── utils/                  # Utilities
└── types/                  # TypeScript types
```

---

## 🔀 Expo vs Bare React Native

| Feature            | Expo           | Bare RN        |
| ------------------ | -------------- | -------------- |
| Setup complexity   | Low            | High           |
| Native modules     | EAS Build      | Manual linking |
| OTA updates        | Built-in       | Manual setup   |
| Build service      | EAS            | Custom CI      |
| Custom native code | Config plugins | Direct access  |
| Time to MVP        | Fast           | Slow           |

### When to Use Bare React Native

- Need custom native modules not available in Expo
- Existing native app integration
- Very specific native build requirements
- Corporate restrictions on cloud build services

---

## 🚀 Quick Start

```bash
# Create new Expo project
npx create-expo-app@latest my-app -t expo-template-blank-typescript

# Install essential dependencies
npx expo install expo-router expo-status-bar react-native-safe-area-context
npx expo install @react-native-async-storage/async-storage
npx expo install expo-secure-store expo-haptics
```

---

## 🧭 Expo Router Navigation

```typescript
// app/_layout.tsx
import { Stack } from 'expo-router'

export default function RootLayout() {
  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="(tabs)" />
      <Stack.Screen name="(auth)" />
      <Stack.Screen name="modal" options={{ presentation: 'modal' }} />
    </Stack>
  )
}

// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router'
import { Home, User } from 'lucide-react-native'

export default function TabLayout() {
  return (
    <Tabs>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color, size }) => <Home size={size} color={color} />,
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color, size }) => <User size={size} color={color} />,
        }}
      />
    </Tabs>
  )
}
```

### Programmatic Navigation

```typescript
import { router } from "expo-router";

// Navigate
router.push("/profile/123");
router.replace("/login");
router.back();

// With params
router.push({
  pathname: "/product/[id]",
  params: { id: "123", referrer: "home" },
});
```

---

## 💾 Offline-First with React Query

```typescript
// providers/QueryProvider.tsx
import { QueryClient } from "@tanstack/react-query";
import { createAsyncStoragePersister } from "@tanstack/query-async-storage-persister";
import { PersistQueryClientProvider } from "@tanstack/react-query-persist-client";
import AsyncStorage from "@react-native-async-storage/async-storage";
import NetInfo from "@react-native-community/netinfo";
import { onlineManager } from "@tanstack/react-query";

// Sync online status
onlineManager.setEventListener((setOnline) => {
  return NetInfo.addEventListener((state) => {
    setOnline(!!state.isConnected);
  });
});

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      gcTime: 1000 * 60 * 60 * 24, // 24 hours
      staleTime: 1000 * 60 * 5, // 5 minutes
      networkMode: "offlineFirst",
    },
  },
});

const persister = createAsyncStoragePersister({
  storage: AsyncStorage,
  key: "REACT_QUERY_CACHE",
});
```

---

## ⚡ Performance Patterns

### FlashList over FlatList

```typescript
import { FlashList } from '@shopify/flash-list'
import { memo, useCallback } from 'react'

const ProductItem = memo(function ProductItem({ item, onPress }) {
  const handlePress = useCallback(() => onPress(item.id), [item.id, onPress])

  return (
    <Pressable onPress={handlePress}>
      <FastImage source={{ uri: item.image }} />
      <Text>{item.name}</Text>
    </Pressable>
  )
})

export function ProductList({ products, onProductPress }) {
  const renderItem = useCallback(
    ({ item }) => <ProductItem item={item} onPress={onProductPress} />,
    [onProductPress]
  )

  return (
    <FlashList
      data={products}
      renderItem={renderItem}
      estimatedItemSize={100}
      removeClippedSubviews={true}
    />
  )
}
```

### Reanimated for 60fps Animations

```typescript
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withSpring,
} from 'react-native-reanimated'

function AnimatedButton({ onPress, children }) {
  const scale = useSharedValue(1)

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }))

  const handlePressIn = () => {
    scale.value = withSpring(0.95)
  }

  const handlePressOut = () => {
    scale.value = withSpring(1)
  }

  return (
    <Animated.View style={animatedStyle}>
      <Pressable
        onPress={onPress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
      >
        {children}
      </Pressable>
    </Animated.View>
  )
}
```

---

## 📱 Platform-Specific Code

```typescript
import { Platform, StyleSheet } from "react-native";

const styles = StyleSheet.create({
  shadow: Platform.select({
    ios: {
      shadowColor: "#000",
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 4,
    },
    android: {
      elevation: 4,
    },
  }),
});

// Or use file-based separation
// Button.ios.tsx
// Button.android.tsx
// Button.web.tsx
```

---

## 🔐 Native Services

```typescript
// Haptics
import * as Haptics from "expo-haptics";

if (Platform.OS !== "web") {
  Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
}

// Secure Storage
import * as SecureStore from "expo-secure-store";

await SecureStore.setItemAsync("token", authToken);
const token = await SecureStore.getItemAsync("token");

// Biometrics
import * as LocalAuthentication from "expo-local-authentication";

const result = await LocalAuthentication.authenticateAsync({
  promptMessage: "Authenticate",
});
```

---

## 📦 EAS Build & Submit

```json
// eas.json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal",
      "android": { "buildType": "apk" }
    },
    "production": {
      "autoIncrement": true
    }
  }
}
```

```bash
# Build commands
eas build --platform ios --profile production
eas build --platform android --profile production

# Submit to stores
eas submit --platform ios
eas submit --platform android

# OTA updates
eas update --branch production --message "Bug fixes"
```

---

## 🚨 Anti-Patterns

| ❌ Don't                     | ✅ Do                                |
| ---------------------------- | ------------------------------------ |
| Use FlatList for large lists | Use FlashList                        |
| Inline styles                | Use StyleSheet.create                |
| Fetch in render              | Use useEffect or React Query         |
| Ignore platform differences  | Test on both iOS and Android         |
| Store secrets in code        | Use environment variables            |
| Skip error boundaries        | Handle crashes gracefully            |
| Animate on JS thread         | Use Reanimated for native animations |
| Forget offline handling      | Implement offline-first              |

---

## ✅ Self-Check Before Completing

| Check               | Question                                 |
| ------------------- | ---------------------------------------- |
| ✅ **Expo?**        | Using Expo unless specifically required? |
| ✅ **TypeScript?**  | Full type coverage?                      |
| ✅ **Offline?**     | Handles offline state gracefully?        |
| ✅ **Platform?**    | Tested on both iOS and Android?          |
| ✅ **Performance?** | FlashList, memoization, Reanimated?      |
| ✅ **Secure?**      | Tokens in SecureStore, not AsyncStorage? |
| ✅ **Navigation?**  | Expo Router properly configured?         |

---

## 🔗 Related Skills

| Need               | Skill              |
| ------------------ | ------------------ |
| Flutter comparison | `flutter-patterns` |
| Mobile design      | `mobile-design`    |
| React patterns     | `react-patterns`   |
| Testing            | `testing-patterns` |

---

> **Remember:** Mobile users expect instant responses, offline capability, and native feel. Every millisecond of loading time matters.
