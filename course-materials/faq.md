# CLD 101 FAQ

*Fictional course. The TA keeps this up to date. New entries are drafted by
`@insights` and posted only after the TA approves them.*

## Logistics

**When are office hours?**
The assistants answer in the `office-hours` room at any time. The TA is
online Tue/Thu 4–6 PM. (Syllabus § 4.)

**How many late days do I have?**
Three for the term, up to two per assignment, no need to ask. After that,
10% off per day for up to 3 days. (Syllabus § 3.)

**Can an assistant give me an extension?**
No. Only the TA or instructor can grant extensions. `@triage` will route
your request to the TA. (Syllabus § 3.3.)

## Concepts

**What's the difference between an image and a container?**
An image is the template; a container is a running instance of it.
(L02 § Slide 2.)

**Liveness vs readiness?**
Liveness failing restarts the container; readiness failing takes the pod out
of the Service without restarting it. (L03 § Slide 6.)

## Assignments

**A2: My pod is stuck in `Pending`.**
Usually the cluster has no room for the CPU or memory you asked for. Run
`kubectl describe pod` and read the Events at the bottom.
