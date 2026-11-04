# L02 — Containers

*CLD 101 (fictional), week 2.*

## Slide 1 — Why containers

A container packages an app with its dependencies so it runs the same way on
a laptop and in the cloud. It shares the host's kernel, so it starts in
seconds and uses less memory than a virtual machine.

## Slide 2 — Image vs container

- An **image** is a read-only template, built from a `Dockerfile`.
- A **container** is a running instance of an image.
- One image can run as many containers.

## Slide 3 — A minimal Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "server.py"]
```

`EXPOSE` documents the port; it does not publish it. You publish with
`docker run -p 8080:8080`.

## Slide 4 — Layers and caching

Each instruction makes a layer. Docker reuses unchanged layers, so copy
`requirements.txt` and install dependencies **before** copying your code:
editing code then doesn't reinstall everything.

## Slide 5 — Takeaway

Images are what you ship; containers are what runs. Kubernetes (week 3)
runs and restarts containers for you, which is why it needs to know when a
container is healthy (L03).
