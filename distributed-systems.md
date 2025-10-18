### Scalability
- Need to automatically scale to multiple machines to handle peaks and dips in traffic. Or else it may lead to over-utilization or under-utilization
- A scalable web app can not only handle 1 user but can also handle 100M users and can gracefully handle peaks and dips in traffic by adding and removing resources from the system

### Resiliency
- Failures in networking, new app versions, or peak load shouldn't disrupt user experience
- Resilience means designing to withstand failures. A Resilient web app continues to work despite failures of some or more system components
- Requires planning at all levels of the architecture
  - Infrastructure and Networking
  - Data storage
  - Application
---
- Scalability and Resiliency can be achieved using:
  - Automation: Automating infra, provisioning, testing, and app deployments can minimize human error, improve consistency & speed
  - Loose coupling: Treating the system as a collection of loosely coupled components increases flexibility and Resiliency
  - Data-driven design: Collect metrics from app. Decisions about when to scale an app / when a service is unhealthy need to be based on data
