# L01 — Cloud basics

*CLD 101 (fictional), week 1.*

## Slide 1 — What "the cloud" means

Renting computing (servers, storage, networks) from a provider over the
internet, paying for what you use, instead of buying and running hardware.

## Slide 2 — Five properties

1. On-demand self-service
2. Broad network access
3. Resource pooling (many customers share hardware)
4. Rapid elasticity (scale up and down quickly)
5. Measured service (you pay by usage)

## Slide 3 — Service models

| Model | You manage | Provider manages | Example shape |
|---|---|---|---|
| IaaS | OS, runtime, app | Hardware, virtualization | A virtual machine |
| PaaS | Your app and data | Everything below it | A managed app platform |
| SaaS | Just your settings | Everything | A hosted email service |

## Slide 4 — Regions and availability zones

A **region** is a geographic area. A region has several **availability
zones**: separate data centers with independent power and networking.
Spreading an app across zones keeps it up when one zone fails.

## Slide 5 — Takeaway

The cloud trades capital cost for operating cost, and gives you elasticity.
The rest of the course is about running apps reliably on it.
