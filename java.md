# Java — From Basics to Expert

## Core Concepts & JVM Architecture
- **JDK vs JRE vs JVM**:
  - **JVM (Java Virtual Machine)**: Executes compiled Java bytecode (`.class` files) on underlying hardware.
  - **JRE (Java Runtime Environment)**: JVM + core runtime libraries required to run Java applications.
  - **JDK (Java Development Kit)**: JRE + developer tools (compiler `javac`, debugger `jdb`, archiver `jar`, profilers).
- **Compilation & Execution**: Java source code (`.java`) → Bytecode via `javac` → JVM executes bytecode via Interpreter + JIT (Just-In-Time) compiler (HotSpot C1/C2) compiling hot code directly into machine assembly.
- **ClassLoader Subsystem**:
  - **Bootstrap ClassLoader**: Loads core runtime classes (`java.lang.*` from `rt.jar` / `java.base`).
  - **Platform/Extension ClassLoader**: Loads platform modules and extensions.
  - **Application/System ClassLoader**: Loads application classes from the classpath.
  - Follows the **Delegation Hierarchy Principle** (parent-first delegation prevents duplicate or malicious overrides).

## JVM Memory Model (JMM) & Garbage Collection
- **Memory Areas**:
  - **Heap**: Shared runtime data area where all object instances and arrays are allocated. Managed by Garbage Collection.
  - **Method Area / Metaspace**: Stores class metadata, runtime constant pool, static variables, and method bytecode. Resides in native memory (since Java 8 replaced PermGen).
  - **JVM Stack**: Thread-private memory storing frames (local variables, operand stack, method invocation/return). Throws `StackOverflowError`.
  - **Program Counter (PC) Register**: Stores the address of the currently executing JVM instruction for each thread.
  - **Native Method Stack**: Used for native C/C++ method invocations via JNI (Java Native Interface).
- **Heap Generations**:
  - **Young Generation**: Short-lived objects. Divided into **Eden** (~80%) and two **Survivor spaces (S0/S1)** (~10% each). Minor GC cleans Young Gen.
  - **Old Generation (Tenured)**: Long-lived objects promoted after surviving several minor GC cycles (controlled by `-XX:MaxTenuringThreshold`). Major / Full GC cleans Old Gen.
- **Garbage Collection Algorithms**:
  - **Serial GC** (`-XX:+UseSerialGC`): Single-threaded mark-copy/compact. Suitable for small client apps.
  - **Parallel GC** (`-XX:+UseParallelGC`): Multi-threaded throughput-focused collector.
  - **G1 GC** (`-XX:+UseG1GC`): Default since Java 9. Divides heap into equal-sized regions, prioritizes regions with the most garbage ("Garbage-First"), predictable pause times (`-XX:MaxGCPauseMillis`).
  - **ZGC** (`-XX:+UseZGC`) & **Shenandoah**: Ultra-low latency concurrent garbage collectors with pause times under 1 millisecond regardless of heap size (gigabytes to terabytes).

## Java Collections Framework
- **Hierarchy Overview**:
  - `Collection` interface roots `List`, `Set`, and `Queue`.
  - `Map` is a standalone interface for key-value mappings.
- **Lists (Ordered, allows duplicates)**:
  - **`ArrayList`**: Resizable array. Fast random access $O(1)$, slow arbitrary insertion/deletion $O(n)$ due to array copies. Grows by 50% when full.
  - **`LinkedList`**: Doubly-linked list. Fast insertion/deletion $O(1)$ at head/tail, poor random access $O(n)$ and high memory pointer overhead.
- **Sets (Unique elements)**:
  - **`HashSet`**: Backed by a `HashMap`. Unordered, $O(1)$ add/contains/remove.
  - **`LinkedHashSet`**: Hash table + doubly-linked list maintaining insertion order.
  - **`TreeSet`**: Backed by a Red-Black Tree (`NavigableMap`). Sorted order, $O(\log n)$ operations.
- **Maps (Key-Value associations)**:
  - **`HashMap`**: Array of buckets (nodes). Keys hashed via `hashCode()`, bucket index calculated via `(n - 1) & hash`. Resolves collisions using linked lists; transforms into Red-Black trees when bucket length exceeds threshold (8) and table capacity $\ge 64$ for $O(\log n)$ worst-case performance.
  - **`ConcurrentHashMap`**: Thread-safe without global locking. Uses synchronized bucket-head nodes and CAS (Compare-And-Swap) operations for fine-grained segment/bucket locking. Does not allow `null` keys or values.
  - **`TreeMap`**: Red-Black tree implementation of `SortedMap`. Keys ordered by natural comparator.
- **Queues & Deques**:
  - **`ArrayDeque`**: Resizable array implementation of deque. Faster than `Stack` and `LinkedList` for LIFO/FIFO queues.
  - **`PriorityQueue`**: Binary heap implementation ordered by natural ordering or custom comparator.

## Concurrency & Multithreading
- **Thread Lifecycle**: `NEW` → `RUNNABLE` → `BLOCKED` (waiting for lock) / `WAITING` (waiting indefinitely) / `TIMED_WAITING` (`sleep`, timed `wait`) → `TERMINATED`.
- **Synchronization & Primitives**:
  - **`synchronized`**: Intrinsic monitor locks on objects or methods. Enforces mutual exclusion and memory visibility.
  - **`volatile`**: Guarantees memory visibility across threads (reads/writes bypass CPU L1/L2 caches and write directly to main memory) and prevents instruction reordering. Does *not* guarantee atomicity (e.g., `count++` is not atomic).
  - **Atomic Variables**: `AtomicInteger`, `AtomicLong`, `AtomicReference` leverage low-level CPU CAS (Compare-And-Swap) instructions for lock-free thread safety.
- **Explicit Locks (`java.util.concurrent.locks`)**:
  - **`ReentrantLock`**: Explicit locking supporting fairness policies, `tryLock()`, and interruptible lock acquisitions.
  - **`ReentrantReadWriteLock`**: Multiple concurrent readers or single exclusive writer. Dramatically increases read throughput.
- **Thread Pools (`ExecutorService`)**:
  - Use `ThreadPoolExecutor` over raw threads to reuse expensive OS threads and prevent resource exhaustion.
  - Core parameters: `corePoolSize`, `maximumPoolSize`, `keepAliveTime`, `workQueue` (e.g., `ArrayBlockingQueue`, `LinkedBlockingQueue`), and `RejectedExecutionHandler`.
- **CompletableFuture**: Functional, non-blocking asynchronous programming pipeline.
  ```java
  CompletableFuture.supplyAsync(() -> fetchUserData(userId))
      .thenApplyAsync(user -> enrichProfile(user))
      .thenAccept(profile -> renderDashboard(profile))
      .exceptionally(ex -> handleFallback(ex));
  ```
- **Virtual Threads (Project Loom - Java 21+)**:
  - Lightweight user-mode threads managed by the JVM rather than the OS kernel.
  - Millions of virtual threads can run concurrently over a small pool of carrier OS threads.
  - Blocking operations (I/O, sockets) unmount the virtual thread from the carrier thread without consuming OS thread resources, reviving high-throughput synchronous coding models.
  ```java
  try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
      IntStream.range(0, 10_000).forEach(i -> executor.submit(() -> performHttpCall()));
  }
  ```

## Java Generics
- Enhances type system by enabling compile-time type checking to avoid runtime `ClassCastException`.
- Eliminates the need for explicit type casting and promotes code reusability.
- **Type Erasure**: Generics exist strictly at compile time; the compiler erases type parameters to their bounds (or `Object`) in bytecode, inserting necessary casts for backwards compatibility.
```java
// Generic method example
public <T> List<T> replicate(T element, int count) {
    List<T> list = new ArrayList<>();
    for (int i = 0; i < count; ++i) {
        list.add(element);
    }
    return list;
}

// Upper-bounded wildcard: read-only access (covariance - Producer Extends)
public double sumOfList(List<? extends Number> list) {
    double sum = 0.0;
    for (Number n : list) {
        sum += n.doubleValue();
    }
    return sum;
}

// Lower-bounded wildcard: write access (contravariance - Consumer Super)
public void addIntegers(List<? super Integer> list) {
    list.add(42);
}
```
- **PECS Rule**: *Producer Extends, Consumer Super*. If you only read from a collection, use `? extends T`. If you only write to a collection, use `? super T`.

## Modern Java Features (Java 8 to 21+)
- **Lambdas & Functional Interfaces** (Java 8): `Function<T, R>`, `Predicate<T>`, `Consumer<T>`, `Supplier<T>`, `BiFunction<T, U, R>`.
- **Streams API** (Java 8): Declarative pipeline processing with intermediate operations (`filter`, `map`, `flatMap`, `sorted`) and terminal operations (`collect`, `reduce`, `forEach`).
- **Optional<T>** (Java 8): Container object to prevent `NullPointerException` and represent optional return values clearly.
- **Records** (Java 16): Immutable data carriers with auto-generated constructor, getters, `equals()`, `hashCode()`, and `toString()`.
  ```java
  public record UserDto(Long id, String username, String email) {}
  ```
- **Sealed Classes & Interfaces** (Java 17): Restricts which classes or interfaces may extend or implement them.
  ```java
  public sealed interface PaymentMethod permits CreditCard, UPI, NetBanking {}
  ```
- **Pattern Matching for `switch` & `instanceof`** (Java 17–21):
  ```java
  static String formatValue(Object obj) {
      return switch (obj) {
          case Integer i -> String.format("Integer: %d", i);
          case String s  -> String.format("String: %s (len: %d)", s, s.length());
          case UserDto u -> String.format("User: %s", u.username());
          case null      -> "Null value";
          default        -> obj.toString();
      };
  }
  ```
- **Sequenced Collections** (Java 21): Unified interfaces (`SequencedCollection`, `SequencedSet`, `SequencedMap`) providing defined encounter orders with `getFirst()`, `getLast()`, `addFirst()`, `addLast()`, and `reversed()`.

## Best Practices & Performance Optimization
- **`equals()` and `hashCode()` Contract**: Always override both together. If two objects are equal via `equals()`, they must return the same `hashCode()`. Failing to do so breaks `HashSet` and `HashMap` lookups.
- **String Handling**: Use `StringBuilder` (non-synchronized, fast) or `StringBuffer` (thread-safe) for multi-step string manipulations inside loops rather than string concatenation (`+`).
- **Resource Management**: Always use `try-with-resources` for objects implementing `AutoCloseable` (database connections, file streams, network sockets) to prevent resource leaks.
- **JVM Flags & Diagnostics**:
  - `-Xms4g -Xmx4g`: Pin initial and maximum heap to eliminate dynamic heap resizing overhead in production.
  - `-XX:+UseG1GC -XX:MaxGCPauseMillis=200`: Standard production G1 tuning baseline.
  - `-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/var/log/dumps`: Automatic heap dump capture on fatal OOM conditions.
