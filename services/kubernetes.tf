provider "docker" {}

resource "docker_network" "pulsar_network" {
  name = "pulsar"
  driver = "bridge"
}

resource "docker_image" "pulsar_image" {
  name = "apachepulsar/pulsar:latest"
}

resource "docker_container" "zookeeper" {
  name  = "zookeeper"
  image = docker_image.pulsar_image.name
  restart = "on-failure"
  networks_advanced = [
    {
      name = docker_network.pulsar_network.name
    }
  ]
  volumes = [
    "./data/zookeeper:/pulsar/data/zookeeper"
  ]
  environment = [
    "metadataStoreUrl=zk:zookeeper:2181",
    "PULSAR_MEM=-Xms256m -Xmx256m -XX:MaxDirectMemorySize=256m"
  ]
  command = [
    "bash", "-c", "bin/apply-config-from-env.py conf/zookeeper.conf && bin/generate-zookeeper-config.sh conf/zookeeper.conf && exec bin/pulsar zookeeper"
  ]
  healthcheck {
    test     = ["CMD", "bin/pulsar-zookeeper-ruok.sh"]
    interval = "10s"
    timeout  = "5s"
    retries  = 30
  }
}

resource "docker_container" "pulsar_init" {
  name     = "pulsar-init"
  hostname = "pulsar-init"
  image    = docker_image.pulsar_image.name
  networks_advanced = [
    {
      name = docker_network.pulsar_network.name
    }
  ]
  command = [
    "bin/pulsar", "initialize-cluster-metadata",
    "--cluster", "cluster-a",
    "--zookeeper", "zookeeper:2181",
    "--configuration-store", "zookeeper:2181",
    "--web-service-url", "http://broker:8080",
    "--broker-service-url", "pulsar://broker:6650"
  ]
  depends_on = [
    docker_container.zookeeper
  ]
}

resource "docker_container" "bookie" {
  name     = "bookie"
  image    = docker_image.pulsar_image.name
  restart  = "on-failure"
  networks_advanced = [
    {
      name = docker_network.pulsar_network.name
    }
  ]
  environment = [
    "clusterName=cluster-a",
    "zkServers=zookeeper:2181",
    "metadataServiceUri=metadata-store:zk:zookeeper:2181",
    "advertisedAddress=bookie",
    "BOOKIE_MEM=-Xms512m -Xmx512m -XX:MaxDirectMemorySize=256m"
  ]
  volumes = [
    "./data/bookkeeper:/pulsar/data/bookkeeper"
  ]
  command = [
    "bash", "-c", "bin/apply-config-from-env.py conf/bookkeeper.conf && exec bin/pulsar bookie"
  ]
  depends_on = [
    docker_container.zookeeper,
    docker_container.pulsar_init
  ]
}

resource "docker_container" "broker" {
  name     = "broker"
  hostname = "broker"
  image    = docker_image.pulsar_image.name
  restart  = "on-failure"
  networks_advanced = [
    {
      name = docker_network.pulsar_network.name
    }
  ]
  environment = [
    "metadataStoreUrl=zk:zookeeper:2181",
    "zookeeperServers=zookeeper:2181",
    "clusterName=cluster-a",
    "managedLedgerDefaultEnsembleSize=1",
    "managedLedgerDefaultWriteQuorum=1",
    "managedLedgerDefaultAckQuorum=1",
    "advertisedAddress=broker",
    "advertisedListeners=external:pulsar://127.0.0.1:6650",
    "PULSAR_MEM=-Xms512m -Xmx512m -XX:MaxDirectMemorySize=256m"
  ]
  ports = [
    "6650:6650",
    "8080:8080"
  ]
  command = [
    "bash", "-c", "bin/apply-config-from-env.py conf/broker.conf && exec bin/pulsar broker"
  ]
  depends_on = [
    docker_container.zookeeper,
    docker_container.bookie
  ]
}

resource "docker_container" "mysql_db" {
  name     = "mysqldb"
  image    = "mysql:8"
  hostname = "mysqldb"
  restart  = "always"
  cap_add  = ["SYS_NICE"]
  environment = [
    "MYSQL_DATABASE=saludtech",
    "MYSQL_ROOT_PASSWORD=adminadmin"
  ]
  networks_advanced = [
    {
      name = docker_network.pulsar_network.name
    }
  ]
  ports = [
    "3306:3306"
  ]
  volumes = [
    "./data/mysql:/var/lib/mysql",
    "./init.sql:/docker-entrypoint-initdb.d/init.sql"
  ]
}

resource "docker_container" "seguridad" {
  name     = "seguridad"
  image    = "seguridad/flask"
  hostname = "seguridad"
  networks_advanced = [
    {
      name = docker_network.pulsar_network.name
    }
  ]
  environment = [
    "BROKER_HOST=broker"
  ]
  depends_on = [
    docker_container.broker,
    docker_container.mysql_db
  ]
  ports = [
    "5000:5000"
  ]
}

output "pulsar_network_id" {
  value = docker_network.pulsar_network.id
}
