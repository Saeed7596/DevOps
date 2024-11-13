var serverStatus_result = db.serverStatus();
var serverStatus = {
   version: serverStatus_result['version'],
   host: serverStatus_result['host'],
   uptime: serverStatus_result['uptime'],
   mem: serverStatus_result['mem'],
   connections: serverStatus_result['connections'],
   network: serverStatus_result['network'],
   extra_info: serverStatus_result['extra_info'],
   opLatencies: serverStatus_result['opLatencies'],
}
print(JSON.stringify({ serverStatus }));
