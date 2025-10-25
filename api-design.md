- Basics
    - APIs provide a way in which software applications communicate with each other by hiding the complexity of each other
    - They define the methods and data formats an application should use in order to perform tasks, like sending, retrieving, or modifying data
    - They allow applications to exchange data and functionality with ease, thus enabling integration and convergence of technological services
    - DNS
    - TCP/IP
    - HTTP:
        - HTTP versions: HTTP/1.0, HTTP/2, HTTP/3
            - Selecting an appropriate HTTP version is crucial for API efficiency and performance
        - HTTP Methods: GET, POST, PUT, DELETE, and PATCH
            - Each of these methods signifies a different type of request, allowing for various interactions with your API endpoints
        - HTTP Status Codes: provide important information about the result of a request made to a server
            - 2xx, 4xx, 5xx
        - HTTP Headers: They can define parameters such as content type, authentication, response status, cookies, and more
        - HTTP Caching: When an API receives the same request multiple times, instead of processing each request separately, it can use a previously stored response, thereby improving performance and efficiency
            - The cache is governed by headers on the HTTP requests and responses
        - Cookies: cookies are small bits of data stored on a user's browser that enables stateful HTTP sessions
            - cookies are especially useful when authentication is required. Cookies can store session tokens, thereby allowing users to stay logged in across multiple sessions or different web pages
        - CORS: It is a mechanism that uses HTTP headers to tell browsers to give a web application running at one origin, access to selected resources from a different origin.
            - By default, web browsers prohibit web pages from making requests to a different domain than the one the web page came from. CORS is the guideline that lets you configure a set of rules on the server to define which types of cross-domain requests are allowed, providing much-needed flexibility without compromising security
    - Request and Response formats: query/path parameters, body

- API styles
    - RESTful APIs
    - gRPC APIs
    - graphql APIs

- REST APIs
    - REST principles
    - pagination
    - rate limiting
    - idempotency
    - versioning
    - error handling

- API authentication and authorization
    - Authentication:
        - Basic Auth
        - JWT
        - OAuth 2.0
        - Token based Auth
        - Session based Auth
    - Authorization:
        - RBAC
        - ABAC
        - ReBAC

- API integration patterns
    - 

- API testing
    - unit tests: testing the individual components or functions of an API independently to ensure that each part is working correctly
    - integration tests: individual units or components are combined and tested as a group
        - It helps detect issues related to the network, database, and performance, which unit tests cannot uncover
    - functional tests: it ensures the server response works as expected and assesses the functionality of the API whether it is performing all the intended functions correctly
        - Various approaches like testing request-response pairs, error codes, and data accuracy are used
    - load tests: ensures reliability, efficiency and performance under varying loads
        - primarily focuses on identifying the maximum capacity of the API in terms of the volume of requests it can handle and its subsequent behavior when this threshold is reached or overloaded
        - By simulating varying degrees of user load, developers can identify and rectify bottlenecks or breakdown points in the system, hence enhancing overall API resilience

- Real-time APIs
    - websockets: provide a long-lived connection between a client and a server over which messages can be sent bi-directionally, in real-time.
        - used for developing APIs that require real-time data transfer, such as chat applications, live sports updates, and real-time analytics
        - offers a faster, responsive, dynamic and more efficient communication method over the traditional HTTP

    - server sent events
        - Unlike traditional approaches where a client sends a request and awaits a response from the server, SSE enables a server to push data to clients whenever a particular event takes place
        - applications where real-time data is essential, such as live news updates, real-time gaming, or live-streaming services
        - Designing APIs with the SSE approach ensures a more dynamic and responsive user experience
