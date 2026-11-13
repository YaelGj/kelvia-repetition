# Les « machines » sont des conteneurs Docker (pas de compte cloud) : les commandes sont les mêmes.
terraform {
  required_providers {
    docker = {source = "kreuzwerker/docker", version = "4.6.0"}
  }
}

variable "nombre_vm" {
  default = 2
}

resource "docker_network" "kelvia" {
  name = "kelvia"
}
resource "docker_image" "python" {
  name = "python:3.12-slim"
}
resource "docker_container" "web" {
  count   = var.nombre_vm
  name    = "vm-web-${count.index + 1}"
  image   = docker_image.python.image_id
  command = ["python", "-m", "http.server",
             "8000", "-d", "/srv"]
  networks_advanced {
    name = docker_network.kelvia.name
  }
  ports {
    internal = 8000
    external = 8081 + count.index
  }
}
