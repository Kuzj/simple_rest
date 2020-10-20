#!/bin/bash

chat=
bot_name=
endpoint=http://localhost:8800/json
message=dummy

curl --header "Content-Type: application/json" --request POST --data '{"action":{"name":"icq","method":"send_message","chat":"'$chat'","message":"'$message'","bot_name":"'$bot_name'"}}' $endpoint