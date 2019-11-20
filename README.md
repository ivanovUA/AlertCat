<img src="https://bit.ly/2Ou0bCV" title="AlertCat" alt="AlertCat">

# AlertCat

AlertCat can help you export alerts from Prometheus to Google Chat

## Docker run

```
docker run -d -i --rm -p 3000:3000 -t ivanovua/alertcat:latest -e TOKEN_URL='https://chat.googleapis.com/v1/spaces/SOME-TOKEN-HERE'
```

## Kubernetes

Change env TOKEN_URL to your token.
Route all Prometheus alerts to AlertCat:
```
global:
receivers:
 - name: default-receiver
   webhook_configs:
    - url: "http://alertcat/alerts"

```

## Screenshot
<img src="https://imgur.com/m6kGzXQ">
