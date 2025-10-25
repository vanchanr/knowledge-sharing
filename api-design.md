- Basics
    - 


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
