# Spring Boot — From Basics to Expert

## Core Foundations & Architecture
- **Inversion of Control (IoC) & Dependency Injection (DI)**:
  - **IoC**: Inverts application control flow—instead of objects creating and instantiating their dependencies, the framework creates, wires, and manages object lifecycles.
  - **DI**: The specific pattern through which dependencies are injected into a class (Constructor Injection, Setter Injection, Field Injection). Constructor injection is strongly recommended for immutability and testability.
- **Spring Container (`ApplicationContext`)**:
  - The central interface providing bean factory capabilities, environment abstraction, event publishing, and internationalization.
  - Common implementations: `AnnotationConfigApplicationContext`, `AnnotationConfigServletWebServerApplicationContext`.
- **Bean Lifecycle**:
  `Instantiation` $\to$ `Populate Properties` $\to$ `BeanNameAware / BeanFactoryAware` $\to$ `BeanPostProcessor (pre-init)` $\to$ `@PostConstruct / InitializingBean` $\to$ `BeanPostProcessor (post-init)` $\to$ **Ready for Use** $\to$ `@PreDestroy / DisposableBean`.
- **Bean Scopes**:
  - `singleton` (Default): One shared instance per Spring IoC container.
  - `prototype`: A new instance created on every request/injection.
  - Web scopes: `request`, `session`, `application`.
- **Aspect-Oriented Programming (AOP)**:
  - Decouples cross-cutting concerns (logging, security, metrics, `@Transactional`) from core business logic using dynamic proxies (JDK dynamic proxies for interfaces, CGLIB for classes).

---

## Spring Boot Internals

### Starters & Dependency Management
- **Starter POMs**: Curated dependency descriptors (e.g., `spring-boot-starter-web`, `spring-boot-starter-data-jpa`) that aggregate compatible, battle-tested dependencies and transitively pull verified versions managed by the Spring Boot BOM (Bill of Materials).

### Autoconfiguration (`@EnableAutoConfiguration`)
- Examines the classpath, configured beans, and properties to automatically configure beans you haven't explicitly declared.
- **`@SpringBootApplication`**: Meta-annotation combining:
  - `@SpringBootConfiguration`: Marks class as configuration source.
  - `@EnableAutoConfiguration`: Enables auto-configuration discovery.
  - `@ComponentScan`: Scans for components in the current package and subpackages.
- **Conditional Annotations (`@Conditional`)**:
  - `@ConditionalOnClass`: Configures bean only if specified class is on classpath.
  - `@ConditionalOnMissingBean`: Configures default bean only if developer has not defined their own bean override.
  - `@ConditionalOnProperty`: Activates based on environment configuration values.
- **Discovery Mechanism**: Discovers auto-configurations declared in `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`.

### Production Observability with Actuator
- Exposes operational and monitoring endpoints for Kubernetes health probes and Prometheus metrics:
  - `/actuator/health`: Aggregates subsystem health (DB, Redis, disk space). Supports Kubernetes `liveness` and `readiness` groups.
  - `/actuator/metrics`: JVM memory, thread states, garbage collection, HTTP request durations.
  - `/actuator/prometheus`: Formats metrics directly for Prometheus scraping.
  - `/actuator/env` & `/actuator/loggers`: Inspect runtime environment and dynamically change logging levels without application restarts.

### Embedded Web Servers
- Packs server runtimes (Tomcat by default, with Jetty and Undertow as drop-in alternatives) directly inside executable JAR files, eliminating external container deployment overhead.

---

## Web Layer (Spring MVC & REST)
- **DispatcherServlet**: The Front Controller pattern implementation orchestrating incoming HTTP requests:
  `Request` $\to$ `DispatcherServlet` $\to$ `HandlerMapping` $\to$ `HandlerAdapter` $\to$ `@RestController` $\to$ `HttpMessageConverter` (Jackson JSON serialization) $\to$ `Response`.
- **Exception Handling**:
  - Centralized global error handling using `@ControllerAdvice` / `@RestControllerAdvice` and `@ExceptionHandler`.
  - Maps domain exceptions to HTTP status codes and RFC 7807 Problem Details payloads.
- **Validation**: Declarative validation using `@Valid`, `@Validated`, and Jakarta Validation constraints (`@NotNull`, `@Size`, `@Pattern`, `@Email`).

---

## Data Access: Spring Data & Persistence

### Spring Data JPA & Hibernate
- **Repository Abstraction**: Extends `JpaRepository<T, ID>` providing out-of-the-box CRUD, pagination, and sorting without boilerplate implementations.
- **Query Creation**: Dynamic query derivation from method names (`findByEmailAndStatus`), `@Query` with JPQL, or native SQL queries.
- **Entity State Lifecycle**: `Transient` $\to$ `Persistent / Managed` $\to$ `Detached` $\to$ `Removed`.
- **N+1 Query Problem**: Fetching a parent collection executes 1 query for parents and $N$ queries for child entities.
  - *Fixes*: `JOIN FETCH` in JPQL, `@EntityGraph(attributePaths = {"children"})`, or batch fetching (`hibernate.default_batch_fetch_size = 30`).

### Transactions (`@Transactional`)
- Proxy-based declarative transaction management wrapping method execution in begin/commit/rollback blocks.
- **ACID Guarantees**: Atomicity, Consistency, Isolation, and Durability.
- **Propagation Levels**:
  - `REQUIRED` (Default): Joins active transaction if exists; creates new one if none.
  - `REQUIRES_NEW`: Suspends current transaction and executes in a brand new isolated transaction.
  - `SUPPORTS`, `MANDATORY`, `NOT_SUPPORTED`, `NEVER`.
- **Gotchas**: Calling `@Transactional` method from within the same class bypasses the Spring CGLIB proxy, preventing transaction interceptors from firing.

---

## Security: Spring Security
- **Filter Chain Architecture**:
  - Requests pass through `SecurityFilterChain` comprised of specialized filters (`SecurityContextPersistenceFilter`, `UsernamePasswordAuthenticationFilter`, `BearerTokenAuthenticationFilter`, `FilterSecurityInterceptor`).
- **Modern Security Configuration**:
  ```java
  @Configuration
  @EnableWebSecurity
  public class SecurityConfig {
      @Bean
      public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
          http
              .csrf(csrf -> csrf.disable())
              .sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
              .authorizeHttpRequests(auth -> auth
                  .requestMatchers("/api/public/**", "/actuator/health/**").permitAll()
                  .requestMatchers("/api/admin/**").hasRole("ADMIN")
                  .anyRequest().authenticated()
              )
              .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
          return http.build();
      }
  }
  ```
- **Authentication vs Authorization**:
  - `AuthenticationManager` authenticates credentials and produces an authenticated `Authentication` token stored in `SecurityContextHolder`.
  - Method security via `@PreAuthorize("hasRole('ADMIN') or #userId == authentication.principal.id")`.

---

## Cloud Native: Spring Cloud
- **Spring Cloud Gateway**: High-performance, non-blocking API gateway built on Project Reactor and Netty, providing rate limiting, circuit breaking, and path rewriting.
- **Service Discovery (Eureka / Consul)**: Centralized registry where microservice instances register their ephemeral IP/port locations and resolve peers dynamically.
- **Declarative REST Clients (OpenFeign)**: Generates HTTP clients from annotated interfaces:
  ```java
  @FeignClient(name = "order-service")
  public interface OrderClient {
      @GetMapping("/orders/{id}")
      OrderDto getOrderById(@PathVariable("id") Long id);
  }
  ```
- **Resilience & Fault Tolerance (Resilience4j)**:
  - Declarative `@CircuitBreaker`, `@Retry`, `@RateLimiter`, and `@Bulkhead` decorators around downstream calls.

---

## Testing Framework & Best Practices
- **`@SpringBootTest`**: Boots the full `ApplicationContext` for comprehensive integration testing.
- **`@WebMvcTest`**: Slices only the web layer (controllers, converters, advice); mocks the service layer via `@MockBean`.
- **`@DataJpaTest`**: Slices only the persistence layer (JPA repositories, EntityManager, DataSource); disables full context loading for ultra-fast repository tests.
- **Testcontainers**: Spins up real Docker containers (e.g., PostgreSQL, Kafka, Redis) for hermetic integration testing directly from JUnit 5.
