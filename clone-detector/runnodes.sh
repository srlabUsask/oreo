#!/bin/bash
# run this script on master
scriptPATH=`realpath $0`
rootPATH=`dirname $scriptPATH`
echo $rootPATH
ant -buildfile $rootPATH/build.xml clean cdi
mode="${1:-search}"
num_nodes="${2:-1}"
threshold="${3:-6}"
echo "*****************************************************"
echo "running this script in $mode mode"
echo "*****************************************************"

echo $num_nodes > $rootPATH/search_metadata.txt

PIDS=""

rm -f "$rootPATH/nodes_completed.txt"

for i in $(seq 1 1 $num_nodes)
do
    echo "$rootPATH/" "$rootPATH/NODE_$i/sourcerer-cc.properties" "$rootPATH/NODE_$i/log4j2.xml" $rootPATH/dist/indexbased.SearchManager.jar $mode $threshold
    java -Dproperties.rootDir="$rootPATH/" -Dproperties.location="$rootPATH/NODE_$i/sourcerer-cc.properties" -Dlog4j.configurationFile="$rootPATH/NODE_$i/log4j2.xml" -Xms10g -Xmx10g -XX:+UseCompressedOops -jar $rootPATH/dist/indexbased.SearchManager.jar $mode $threshold &
    PIDS+="$! "
done
echo $PIDS
# wait for the processes to get over
status=0
count=1
for pid in $PIDS
do
    wait $pid
    if [ $? -eq 0 ]; then
        echo " NODE_$count SUCCESS - Job $pid exited with a status of $?"
    else
        echo "NODE_$count FAILED - Job $pid exited with a status of $?"
        status=1
    fi
    count=$((count+1))
done
exit $status
