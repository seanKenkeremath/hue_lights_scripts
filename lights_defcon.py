import urllib, urllib2, json, requests

#NOTE requests must be installed. Run "pip install requests"

user_token = "{Insert Token Here}"

get_lights_url = 'http://lights/api/' + user_token + '/lights';
get_lights_rsp = requests.get(get_lights_url)
state = get_lights_rsp.json()

for light in state:
	#set light to alert state
	print "setting %s" % light
	alert_request_url = "http://lights/api/" + user_token + "/lights/" + light + "/state"
	alert_body = {"on":True, "effect": "none", "alert": "lselect", "hue":65280, "sat":254}
	alert_rsp = requests.put(alert_request_url, json.dumps(alert_body))
	# print alert_rsp.json()

	#schedule light to return to previous state after timer
	# print "scheduling reset for %s" % light
	timer_string = "PT00:00:04" #4 seconds
	reset_state_url = "http://lights/api/%s/schedules" % user_token
	reset_state_schedule_body = {"localtime":timer_string, "command": {"address":"/api/" + user_token + "/lights/" + light + "/state","method":"PUT"}, "autodelete":True}
	
	#remove these keys from the state object to send back. Api will complain if "body" element of command is too big
	#These are redundant anyway
	state[light]["state"].pop("reachable", None)
	state[light]["state"].pop("colormode", None)
	state[light]["state"].pop("xy", None)
	state[light]["state"].pop("ct", None)

	# set the "body" element of the command for the schedule POST
	reset_state_schedule_body["command"]["body"] = state[light]["state"]

	reset_rsp = requests.post(reset_state_url, json.dumps(reset_state_schedule_body))
	# print reset_rsp.json()
