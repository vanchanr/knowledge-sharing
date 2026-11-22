#!/usr/bin/env python3
"""Generate perfected Java diagrams."""
import sys
sys.path.insert(0, "/data/data/com.termux/files/home/knowledge-sharing/scripts")
from diagram_builder import DiagramBuilder

def generate_jvm_memory():
    d = DiagramBuilder()
    d.add_header(
        "JVM Architecture & Runtime Data Areas (JVM Memory Model)",
        "Heap Memory (Young & Old Gen), Metaspace, and Thread-Private Execution Stacks",
        x=40, y=25, w=1140, h=65
    )

    # 1. Left Side: Shared Memory (Across All Threads)
    d.add_container(40, 110, 700, 520, label="Shared Runtime Memory (Accessible by All Threads)", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2")

    # JVM Heap Container (inside Shared)
    d.add_container(55, 150, 670, 245, label="JVM Heap Memory (-Xms, -Xmx) — Managed by Garbage Collector", stroke="#2b8a3e", badge_bg="#ebfbee", badge_stroke="#2b8a3e", label_color="#2b8a3e")

    # Young Gen Container
    d.add_container(70, 185, 640, 95, label="Young Generation (Eden + Survivor Spaces) — Minor GC", stroke="#2b8a3e", stroke_style="dotted", badge_bg="#ffffff", badge_stroke="#2b8a3e", label_color="#2b8a3e")
    d.add_box(85, 218, 200, 50, "Eden Space (~80%)", "New object allocations", bg="#d3f9d8", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)
    d.add_box(300, 218, 190, 50, "Survivor S0 (From)", "Live objects after Minor GC", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=12)
    d.add_box(505, 218, 190, 50, "Survivor S1 (To)", "Alternates each GC cycle", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=12)

    # Old Gen Box
    d.add_box(70, 295, 640, 85, "Old Generation / Tenured Space (~66% of Heap) — Major / Full GC", [
        "• Objects surviving threshold (MaxTenuringThreshold = 15) promoted here",
        "• Long-lived singletons, thread pools, and cached domain entities"
    ], bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=12)

    # Metaspace Box
    d.add_box(55, 410, 670, 95, "Metaspace (Native Off-Heap Memory — JDK 8+)", [
        "• Stores Class Metadata, Bytecode, Constant Pool, and Method Tables (replaces PermGen)",
        "• Allocated from Native OS RAM; configured via -XX:MetaspaceSize and -XX:MaxMetaspaceSize"
    ], bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=12)

    # Shared Memory Note
    d.add_box(55, 520, 670, 90, "Thread Synchronization & Memory Visibility", [
        "• All threads share the Heap and Metaspace concurrently.",
        "• JMM (Java Memory Model) guarantees visibility via volatile, synchronized, and VarHandle."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # 2. Right Side: Thread-Private Memory
    d.add_container(760, 110, 420, 520, label="Thread-Private Memory (Per Thread)", stroke="#c92a2a", badge_bg="#ffe3e3", badge_stroke="#c92a2a", label_color="#c92a2a")

    # JVM Stack Box
    d.add_box(780, 155, 380, 145, "JVM Thread Stack (-Xss)", [
        "One stack allocated per running thread",
        "",
        "• Stack Frame per method invocation",
        "• Local Variables Table (primitives, refs)",
        "• Operand Stack (push/pop bytecode ops)",
        "• Frame Data (dynamic linking & return)"
    ], bg="#ffe3e3", stroke="#e03131", text_color="#c92a2a", font_size=12)

    # PC Register Box
    d.add_box(780, 315, 380, 80, "Program Counter (PC) Register", [
        "• Tracks address of current JVM bytecode instruction",
        "• Undefined when executing Native (JNI) methods"
    ], bg="#ffe3e3", stroke="#e03131", text_color="#c92a2a", font_size=12)

    # Native Method Stack Box
    d.add_box(780, 410, 380, 95, "Native Method Stack (C / C++ / JNI)", [
        "• Supports execution of native code via JNI",
        "• Uses platform-native OS C call stack frames"
    ], bg="#ffe3e3", stroke="#e03131", text_color="#c92a2a", font_size=12)

    # Thread Private Note
    d.add_box(780, 520, 380, 90, "Thread Lifecycle & Isolation", [
        "• Created when thread is spawned; destroyed when thread exits.",
        "• Completely isolated: Zero GC overhead in thread-private memory."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    d.render("java-jvm-memory-model.png")

def generate_collections_hierarchy():
    d = DiagramBuilder()
    d.add_header(
        "Java Collections Framework: Interfaces & Implementations",
        "Collection Hierarchy (List, Set, Queue) vs Map Key-Value Architecture",
        x=40, y=25, w=1180, h=65
    )

    # 1. Left Side: Collection<E> Hierarchy
    d.add_container(40, 110, 750, 530, label="Collection<E> Interface Hierarchy (java.util)", stroke="#1971c2", badge_bg="#e7f5ff", badge_stroke="#1971c2", label_color="#1971c2")

    # Root: Iterable<E> & Collection<E>
    d.add_box(305, 150, 220, 38, "«interface» Iterable<E>", "root for for-each loops", bg="#ffffff", stroke="#1971c2", text_color="#1971c2", font_size=12)
    d.add_box(290, 205, 250, 42, "«interface» Collection<E>", "core collection contract", bg="#e7f5ff", stroke="#1971c2", text_color="#1971c2", font_size=13)
    d.add_arrow(415, 188, 415, 205, stroke="#1971c2")

    # 3 Branches: List, Set, Queue
    # Branch 1: List
    d.add_box(55, 265, 215, 42, "«interface» List<E> (Ordered)", "Indexed access, allows duplicates", bg="#d0ebff", stroke="#1971c2", text_color="#1971c2", font_size=12)
    d.add_box(55, 320, 215, 50, "ArrayList", "Dynamic array, O(1) random get(i)", bg="#ffffff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_box(55, 380, 215, 50, "LinkedList", "Doubly-linked, O(1) head/tail ops", bg="#ffffff", stroke="#1971c2", text_color="#1971c2", font_size=11)
    d.add_box(55, 440, 215, 50, "CopyOnWriteArrayList", "Thread-safe, read-heavy lockless", bg="#ffffff", stroke="#1971c2", text_color="#1971c2", font_size=11)

    # Branch 2: Set
    d.add_box(305, 265, 220, 42, "«interface» Set<E> (Unique)", "Disallows duplicate elements", bg="#d3f9d8", stroke="#2b8a3e", text_color="#2b8a3e", font_size=12)
    d.add_box(305, 320, 220, 50, "HashSet", "Backed by HashMap, O(1) add/contains", bg="#ffffff", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_box(305, 380, 220, 50, "LinkedHashSet", "Preserves predictable insertion order", bg="#ffffff", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)
    d.add_box(305, 440, 220, 50, "TreeSet (NavigableSet)", "Red-Black tree, O(log N) sorted keys", bg="#ffffff", stroke="#2b8a3e", text_color="#2b8a3e", font_size=11)

    # Branch 3: Queue
    d.add_box(555, 265, 220, 42, "«interface» Queue<E> / Deque", "FIFO / Double-ended queues", bg="#fff3bf", stroke="#f59f00", text_color="#d9480f", font_size=12)
    d.add_box(555, 320, 220, 50, "ArrayDeque", "Resizing circular buffer (fast stack/queue)", bg="#ffffff", stroke="#f59f00", text_color="#d9480f", font_size=11)
    d.add_box(555, 380, 220, 50, "PriorityQueue", "Binary min-heap, O(log N) poll/offer", bg="#ffffff", stroke="#f59f00", text_color="#d9480f", font_size=11)
    d.add_box(555, 440, 220, 50, "ConcurrentLinkedQueue", "Lock-free CAS node queue", bg="#ffffff", stroke="#f59f00", text_color="#d9480f", font_size=11)

    # Connecting branch arrows
    d.add_arrow(350, 247, 162, 265, stroke="#1971c2")
    d.add_arrow(415, 247, 415, 265, stroke="#2b8a3e")
    d.add_arrow(480, 247, 665, 265, stroke="#f59f00")

    # Bottom Note
    d.add_box(55, 510, 720, 70, "Collection<E> Unified Operations", [
        "• All implementations provide iterator(), stream(), parallelStream(), and spliterator().",
        "• Choose ArrayList for index reads, HashSet for uniqueness, ArrayDeque for queues/stacks."
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    # 2. Right Side: Map<K, V> Hierarchy
    d.add_container(810, 110, 410, 530, label="Map<K, V> Architecture (Separate Key-Value Hierarchy)", stroke="#9c36b5", badge_bg="#f3d9fa", badge_stroke="#9c36b5", label_color="#9c36b5")

    d.add_box(830, 150, 370, 50, "«interface» Map<K, V>", "Key-to-Value mappings (Does NOT extend Collection)", bg="#f3d9fa", stroke="#9c36b5", text_color="#9c36b5", font_size=12)

    d.add_box(830, 215, 370, 60, "HashMap", [
        "• Array of Node<K,V> buckets; O(1) avg lookup",
        "• Treeifies into Red-Black Tree when bucket > 8"
    ], bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5", font_size=11)

    d.add_box(830, 285, 370, 60, "ConcurrentHashMap", [
        "• High concurrency via CAS + synchronized head nodes",
        "• No table-wide locking (unlike Hashtable / synchronizedMap)"
    ], bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5", font_size=11)

    d.add_box(830, 355, 370, 60, "LinkedHashMap", [
        "• HashMap + doubly-linked list across entries",
        "• Supports insertion-order or access-order (LRU cache)"
    ], bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5", font_size=11)

    d.add_box(830, 425, 370, 60, "TreeMap (NavigableMap)", [
        "• Red-Black tree; O(log N) operations",
        "• Keys sorted via natural Comparable or custom Comparator"
    ], bg="#ffffff", stroke="#9c36b5", text_color="#9c36b5", font_size=11)

    # Map Note
    d.add_box(830, 510, 370, 70, "Map Views into Collection Ecosystem", [
        "• keySet(): returns Set<K> of all keys",
        "• values(): returns Collection<V> of all values",
        "• entrySet(): returns Set<Map.Entry<K, V>>"
    ], bg="#ffffff", stroke="#dee2e6", text_color="#495057", font_size=11)

    d.render("java-collections-hierarchy.png")

if __name__ == "__main__":
    generate_jvm_memory()
    generate_collections_hierarchy()
