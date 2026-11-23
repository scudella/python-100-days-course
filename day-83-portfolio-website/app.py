from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

PORTFOLIO_DATA = {
    "name": "Eduardo S. Libardi",
    "handle": "scudella",
    "role": "Full-Stack Web, Mobile & Cloud Infrastructure Engineer",
    "location": "Campinas, SP — Brazil",
    "email": "devscudella@gmail.com",
    "github": "https://github.com/scudella",
    "website": "https://portfolio.scudella.net.br",
    "avatar_url": "https://github.com/scudella.png",
    "about": (
        "Full-stack software engineer and Linux/Kubernetes administrator building "
        "end-to-end web platforms, cross-platform mobile apps, and resilient hybrid-cloud "
        "infrastructure—from React Native and Next.js frontends down to Express APIs, "
        "eBPF networking, and self-hosted clusters."
    ),
    "skills": [
        {"category": "Frontend & Mobile", "skills": ["React", "Next.js", "TypeScript", "React Native / Expo", "Tailwind CSS"]},
        {"category": "Backend & Data", "skills": ["Python / Flask", "Node.js / Express", "PostgreSQL / Prisma", "MongoDB", "AWS Lambda"]},
        {"category": "DevOps & Cloud", "skills": ["Kubernetes", "Cilium eBPF", "Podman / Containers", "Nginx", "Prometheus & Grafana"]},
    ],
    "projects": [
        {
            "title": "Spiritist Books (Livros Espíritas)",
            "description": (
                "Cross-platform mobile app (Android/Expo) and web catalog with accent-insensitive "
                "Portuguese search, author alias resolution, and an Express 5 / AWS Lambda API."
            ),
            "tags": ["React Native", "Expo", "Express 5", "AWS Lambda", "OpenAPI"],
            "live_url": "https://spiritist-books.scudella.net.br",
            "image_url": "",  
        },
        {
            "title": "Next.js Full-Stack E-Commerce",
            "description": (
                "Standalone Next.js storefront backed by PostgreSQL with Prisma, Clerk authentication, "
                "Stripe embedded checkout, and OCI Object Storage pre-authenticated assets."
            ),
            "tags": ["Next.js", "PostgreSQL", "Prisma", "Stripe", "Clerk"],
            "live_url": "https://store-nextjs.scudella.net.br",
            "image_url": "",
        },
        {
            "title": "Hybrid Cloud Kubernetes Homelab",
            "description": (
                "Multi-architecture Kubernetes cluster spanning OCI Ubuntu nodes and a WireGuard-linked "
                "Fedora workstation using Cilium eBPF CNI, automated backups, and Prometheus/Grafana observability."
            ),
            "tags": ["Kubernetes", "Cilium", "WireGuard", "Nginx", "Prometheus"],
            "live_url": "https://portfolio.scudella.net.br",
            "image_url": "",
        },
    ],
}


@app.route("/")
def index():
    return render_template(
        "index.html",
        data=PORTFOLIO_DATA,
        current_year=datetime.now().year,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)