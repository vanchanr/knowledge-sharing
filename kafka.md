##### [Event Streaming Use Cases](https://www.confluent.io/resources/ebook/five-event-streaming-use-cases/): 
- have a centralized event streaming platform
- transform architectures to streaming from batch processing
- use the data that results from all kinds of events and respond to those events in real time
- allows data to be shareable across projects and between previously disconnected teams, like sales and marketing
- Data streaming can connect your enterprise across teams and infrastructure, creating a unified business where everyone can access the data they need
- enables asynchronous communication between applications and microservices with real-time, event-based streaming and persistent storage of events

###### Customer 360°
- Website clickstream analysis
- The original use case that spawned the creation of Apache Kafka was to give LinkedIn a deeper, more comprehensive understanding of who is clicking on what and serve users personalized, contextual, and targeted content
- Creating such customer 360° profiles renders the ability to serve up content that will resonate with the end user, in a real-time way, at massive scale
- real-time warehouse management and order management systems
- used Kafka Connect to write services that link Kafka with BigQuery

###### Legacy IT modernization
- Enabling event streaming helps business processes to transition from batch queries to real-time processing
- Data replication and streaming times reduced from hours or even days to just seconds

###### Real-time analytics
-  the phrase big data has become synonymous with legacy technology such as Apache Hadoop
-  rather than focusing on storing massive amounts of data in warehouses or lakes, today’s data move is about application building and realtime analytics.
-  Audi, for instance, has leveraged the ability to connect, process, and analyze IoT car data and interpret it in order to provide a better allaround customer experience with services like satellite navigation, predictive maintenance, and in-car entertainment.

---
- **Consumer Groups**
  - A partition can be processed by atmost 1 consumer node, while a single consumer within a cosumer group can process multiple partions of a topic
  - this is to maintain ordering within events of a single partition \
![image](https://github.com/vanchanr/knowledge-sharing/assets/43525805/143092ab-46a1-4306-9827-c6f386e2d20f)

- **Kafka APIs**
  - _Producer API_: allows apps to send streams of data to topics in a Kafka cluster
  - _Consumer API_: allows apps to read streams of data from topics in a Kafka cluster
  - _Streams API_: allows transforming streams of data from input topics to output topics
  - _Connect API_: allows implementing connectors that continually pull from some source system or application into Kafka or push from Kafka to some sink system or application
  - _Admin API_: allows managing and inspecting topics, brokers, and other Kafka objects \
![image](https://github.com/vanchanr/knowledge-sharing/assets/43525805/955f21f7-a6b8-481a-ad97-3b8ece570380)

 

