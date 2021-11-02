#! /bin/sh
$HOME/kafka/bin/zookeeper-server-start.sh $HOME/kafka/config/zookeeper.properties &
$HOME/kafka/bin/kafka-server-start.sh $HOME/kafka/config/server.properties &
