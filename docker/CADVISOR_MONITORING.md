# Container Monitoring with cAdvisor

## Overview
cAdvisor (Container Advisor) has been added to monitor resource usage and performance characteristics of running containers.

## What cAdvisor Monitors

### Resource Metrics
- **CPU Usage**: Real-time CPU utilization per container
- **Memory Usage**: Memory consumption and limits
- **Network I/O**: Bytes sent/received per network interface
- **Disk I/O**: Read/write operations and throughput
- **GPU Utilization**: GPU usage when available (requires GPU support)

### Container Metrics
- Container lifecycle events
- Resource limits and reservations
- Performance statistics
- Historical resource usage

## Access cAdvisor

Once the containers are running, access cAdvisor at:
```
http://localhost:8081
```

## Configuration

### Docker Compose Setup
```yaml
cadvisor:
  image: gcr.io/cadvisor/cadvisor:latest
  container_name: mediassist-cadvisor
  privileged: true
  ports:
    - "8081:8080"
  volumes:
    - /:/rootfs:ro
    - /var/run:/var/run:ro
    - /sys:/sys:ro
    - /var/lib/docker/:/var/lib/docker:ro
    - /dev/disk/:/dev/disk:ro
  devices:
    - /dev/kmsg
```

### Prometheus Integration
cAdvisor metrics are automatically scraped by Prometheus:
```yaml
- job_name: "cadvisor"
  static_configs:
    - targets: ["cadvisor:8080"]
```

## Monitored Containers
- **mediassist-api**: Backend API service
- **mediassist-db**: PostgreSQL database
- **mediassist-chroma**: ChromaDB vector database
- **mediassist-mlflow**: MLflow tracking server
- **mediassist-prometheus**: Prometheus monitoring
- **mediassist-grafana**: Grafana dashboards

## Usage

### Start Monitoring
```bash
docker-compose up -d
```

### View Container Metrics
1. Navigate to http://localhost:8081
2. Click on "Docker Containers"
3. Select a container to view detailed metrics

### Query Metrics via Prometheus
Access metrics at: http://localhost:9090

Example queries:
```promql
# CPU usage by container
container_cpu_usage_seconds_total

# Memory usage by container
container_memory_usage_bytes

# Network bytes received
container_network_receive_bytes_total

# Disk I/O
container_fs_io_current
```

### Visualize in Grafana
1. Access Grafana at http://localhost:3000
2. Add Prometheus as data source
3. Import cAdvisor dashboard (ID: 193)
4. View real-time container metrics

## Key Metrics to Monitor

### Performance
- CPU throttling
- Memory pressure
- Network latency
- Disk I/O wait times

### Resource Limits
- Memory limit violations
- CPU quota exhaustion
- Disk space usage

### Health Indicators
- Container restarts
- OOM (Out of Memory) events
- High resource consumption trends

## Troubleshooting

### cAdvisor not starting
Ensure privileged mode is enabled and required volumes are mounted.

### Missing metrics
Check that containers are running:
```bash
docker ps
```

### High resource usage
Use cAdvisor to identify resource-intensive containers and optimize accordingly.

## Security Note
cAdvisor runs in privileged mode to access host resources. Ensure it's only accessible within trusted networks.

## Integration with Monitoring Stack

```
┌─────────────┐
│  Containers │
└──────┬──────┘
       │
       v
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   cAdvisor  │────>│ Prometheus  │────>│   Grafana   │
└─────────────┘     └─────────────┘     └─────────────┘
   Collects            Stores             Visualizes
   Metrics             Metrics            Metrics
```

## Next Steps
1. Configure alerting rules in Prometheus for resource thresholds
2. Create custom Grafana dashboards for specific monitoring needs
3. Set up log aggregation for comprehensive observability
