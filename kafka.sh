#! /bin/sh
$HOME/kafka/bin/zookeeper-server-start.sh $HOME/kafka/config/zookeeper.properties &
sleep 10
$HOME/kafka/bin/kafka-server-start.sh $HOME/kafka/config/server.properties &
