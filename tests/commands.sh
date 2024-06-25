url="http://127.0.0.1:8000"
headers="Content-Type: application/json"

curl $url -X POST -H $headers -d '{"name": "Foo"}' -s | jq
curl $url -X POST -H $headers -d '{"name": "Foo2"}' -s | jq
curl $url -X POST -H $headers -d '{"name": "Foo3"}' -s | jq
curl $url -X POST -H $headers -d '{"name": "Foo5"}' -s | jq
curl $url -X POST -H $headers -d '{"name": "Foo6"}' -s | jq
curl $url -X POST -H $headers -d '{"name": "Foo7"}' -s | jq