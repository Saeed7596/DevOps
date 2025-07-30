# 📊 Resource Sizing Cheat Sheet (CPU vs RAM and More)

This table provides general proportional guidelines for allocating CPU and RAM, suitable for virtual machines, containers, or Kubernetes workloads. Adjust values based on your specific application's needs.

| CPU Cores | Recommended RAM | Suitable For                    | Notes                                                  |
|-----------|------------------|----------------------------------|--------------------------------------------------------|
| 1 vCPU    | 1 – 2 GB         | Lightweight CLI tools, microservices | Minimal background processes                          |
| 2 vCPU    | 2 – 4 GB         | Small apps, web servers         | Can handle moderate traffic                           |
| 4 vCPU    | 4 – 8 GB         | Medium apps, databases          | Ideal for staging environments or light prod workloads |
| 8 vCPU    | 8 – 16 GB        | Production-grade apps, CI runners | Can handle parallel workloads                         |
| 16 vCPU   | 16 – 32 GB       | High-performance workloads       | Suitable for databases, ML, large-scale CI/CD         |
| 32+ vCPU  | 32 – 64+ GB      | Compute-intensive, analytics     | Consider GPU if ML/AI is involved                     |

---

## Additional Considerations

- **Disk IOPS & Throughput**:
  - SSD recommended for databases and CI runners.
  - Allocate based on workload; e.g., 1000+ IOPS for I/O-heavy apps.

- **Network Bandwidth**:
  - Gigabit network sufficient for most uses.
  - Use 10Gbps+ for high-volume traffic or clustering.

- **Swap**:
  - Avoid using swap in containers.
  - Recommended only on bare-metal VMs with memory pressure.

- **CPU vs Memory Ratio**:
  - Common default: **1 vCPU per 2 GB RAM**.
  - For memory-heavy apps (e.g., Java, Node.js), increase RAM ratio.
  - For CPU-bound workloads (e.g., encoding, CI), increase vCPU.

---

## Tip

Use benchmarking tools like `stress`, `sysbench`, or monitoring (Prometheus, top, htop) to fine-tune based on real-world usage.

