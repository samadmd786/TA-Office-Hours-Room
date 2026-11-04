# A3 — Health checks (graded, 10%)

*CLD 101 (fictional). Due Fri Nov 13, 11:59 PM. Late policy: syllabus § 3.*

**Academic integrity:** this is graded work. In office hours you get hints,
not solutions (syllabus § 4.3).

## Goal

Add a liveness probe and a readiness probe to the `inventory` Deployment so
Kubernetes restarts it when it hangs and only sends it traffic when it is
ready. Background: L03.

## What you're given

`starter/server.py`, a small web app. From its README:

> The app listens on port **8080** and serves:
>
> - `GET /items` — the inventory, as JSON
> - `GET /healthz` — returns `200 ok` while the process is responsive
> - `GET /ready` — returns `200` once the database connection is up, `503`
>   before that

`starter/deployment.yaml`, a Deployment with no probes yet. The comment at
the top of that file says:

```yaml
# TODO(A3): add probes. The app's health endpoint is /health on port 8080.
```

## Tasks

1. **(4 pts)** Add a `livenessProbe` that restarts the container if the app
   stops responding.
2. **(4 pts)** Add a `readinessProbe` that keeps the pod out of the Service
   until the database connection is up.
3. **(2 pts)** In `ANSWERS.md`, explain in 2–4 sentences why you chose each
   path and what would happen if the liveness probe pointed at a path the
   app doesn't serve.

## How it's checked

- The pod reaches `READY 1/1` within 60 seconds and has **0 restarts** after
  5 minutes.
- Stopping the fake database makes the pod go `0/1` without restarting.
- Freezing the app (`kill -STOP`) makes Kubernetes restart it.

## Submitting

Push `deployment.yaml` and `ANSWERS.md` to your A3 repository before the
deadline.

<!--
TA note, not shown to students:
The deliberate pitfall is that the starter comment says /health, but the app
serves /healthz. A liveness probe on /health gets 404, so the pod restarts in a
loop (CrashLoopBackOff). Students who read the app's README or use
`kubectl describe pod` (L03 § Slide 7) find it. Hint at that; never give the
corrected YAML.
-->
