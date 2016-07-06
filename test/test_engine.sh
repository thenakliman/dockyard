count=2
psid=$1

while [ $count -lt 254 ]
do
    ip="10.0.9.$count"
    abc=`curl http://10.0.9.1:5869/dockyard/network -XPOST -d "{'psid': '$psid', 'ip': '$ip', 'gateway': '10.0.9.1', 'mask': '24'}"`
    count=`expr $count + 1`
    echo "adding ..... $ip"
done
