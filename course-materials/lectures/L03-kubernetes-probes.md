# L03 — Kubernetes liveness and readiness probes

*CLD 101 (fictional), week 4. Needed for A3.*

## Slide 1 — The problem

Kubernetes sees that a container's process is running. It can't see whether
the app inside is stuck, still starting up, or ready for traffic. **Probes**
let the app tell it.

## Slide 2 — Liveness probe

"Is this container still alive?"

- If the liveness probe fails `failureThreshold` times in a row, the kubelet
  **kills and restarts** the container.
- Use it to recover from deadlocks or hangs.
- A wrong liveness probe is dangerous: it restarts a healthy app forever.
  The pod shows rising `RESTARTS` and often `CrashLoopBackOff`.

## Slide 3 — Readiness probe

"Should this container get traffic right now?"

- If the readiness probe fails, the pod is **removed from the Service's
  endpoints**. It is *not* restarted.
- Use it during startup, or when a dependency (like a database) is down.
- The pod shows `0/1` in the `READY` column while it fails.

## Slide 4 — An HTTP probe

```yaml
livenessProbe:
  httpGet:
    path: /some-path      # must be a path your app actually serves
    port: 8080            # must be the port your container listens on
  initialDelaySeconds: 5
  periodSeconds: 10
  failureThreshold: 3
```

Kubernetes sends `GET http://<pod-ip>:8080/some-path`. A status from **200
to 399** counts as success; anything else, including **404** and a refused
connection, is a failure.

## Slide 5 — The fields that matter

| Field | Meaning | Default |
|---|---|---|
| `initialDelaySeconds` | Wait before the first probe | 0 |
| `periodSeconds` | How often to probe | 10 |
| `timeoutSeconds` | How long one probe may take | 1 |
| `failureThreshold` | Failures in a row before acting | 3 |

## Slide 6 — Liveness vs readiness at a glance

| | Liveness fails | Readiness fails |
|---|---|---|
| What happens | Container restarted | Pod taken out of the Service |
| Typical symptom | `RESTARTS` climbing, `CrashLoopBackOff` | `READY 0/1`, requests time out |
| Use it for | Hangs and deadlocks | Startup, dependencies down |

## Slide 7 — Debugging a failing probe

1. `kubectl describe pod <name>` and read **Events**. A failing probe logs
   lines like `Liveness probe failed: HTTP probe failed with statuscode: 404`.
2. A **404** means Kubernetes reached your app but the **path** is wrong.
   Check which paths your app actually serves.
3. `connection refused` usually means the **port** is wrong or the app
   isn't listening yet (try a larger `initialDelaySeconds`).
4. Test it yourself: `kubectl port-forward pod/<name> 8080:8080`, then
   `curl -i localhost:8080/<path>`.

## Slide 8 — Takeaway

Liveness answers "restart me?"; readiness answers "send me traffic?". The
path and port in a probe must match what the app really serves.
