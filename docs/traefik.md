# CasaEsperta - [Traefik](https://containo.us/traefik/)

Start by installing only Traefik to test the SSL certificates generation and basic authentication. When that's setup, we can add security request headers, Google OAuth and then other containers.

Create some folders and empty files:
```
mkdir ~/docker/shared
touch ~/docker/shared/.htpasswd
mkdir ~/docker/traefik
mkdir ~/docker/traefik/acme
mkdir ~/docker/traefik/rules
touch ~/docker/traefik/acme/acme.json
chmod 600 ~/docker/traefik/acme/acme.json
touch ~/docker/traefik/traefik.log
```

Create the docker network that will be used by the stack. You can use any free subnet on your lan. `proxy_net` represents the name of the network. If you change this, make sure to change it also in the compose.yml file:
```
docker network create --gateway 192.168.50.1 --subnet 192.168.50.0/24 proxy_net
```

## Basic Auth - With staging Let's Encrypt servers

Create a valid string that represents a username and password [here](https://www.web2generators.com/apache-tools/htpasswd-generator). Copy the generated text to the `~/docker/shared/.htpasswd` file.

Some examples of needed files are given for this next section.
```
touch ~/docker/compose.yml
touch ~/docker/traefik/rules/middlewares.toml
```

Copy the content of [middlewares_example.toml](../main_server/docker/traefik/middlewares_example.toml) to `~/docker/traefik/rules/middlewares.toml` and make sure to replace example.pt with your domain.

If you want more information about this file, I recommend again reading [this article](https://www.smarthomebeginner.com/traefik-2-docker-tutorial/), specially the sections that talk about Traefik.

Copy all the content of [basic_compose.yml](../main_server/docker/basic_compose.yml) to `~/docker/compose.yml`. Read the contents and follow indications if you prefer to use DuckDNS instead of Cloudflare.

```
dcup
```
If all went well, the above command will deploy the Traefik container. Traefik will then request "fake" SSL certificates to the domain you specified nad you'll be able to navigate to `https://traefik.example.pt`. The authentication will be the user/password you defined when creating the content of `~/docker/shared/.htpasswd`.

The SSL certificate will be invalid but should reference "Fake LE Certificate" as its origin.

If you need/want to see the container logs, just type:
```
dclogs
```

## Google Auth - Production SSL servers
When the above step is concluded successfully we can go to full valid SSL certificates and Google OAuth authentication.

Create an empty file to define some "middleware chains" (if you want more info, go read [this article](https://www.smarthomebeginner.com/traefik-2-docker-tutorial/)).

```
touch ~/docker/traefik/rules/middleware-chains.toml
```

Copy the content of [middleware-chains.toml](../main_server/docker/traefik/middleware-chains.toml) to `~/docker/traefik/rules/middleware-chains.toml`.

Replace `~/docker/compose.yml` with the content of [oauth_compose.yml](../main_server/docker/oauth_compose.yml) again reading it and following indications if you prefer to use DuckDNS instead of Cloudflare.
If you changed the network name in the previous step, you might want to do it again.

### OAuth Container

This functionality is provided by the container [Traefik Forward Auth](https://github.com/thomseddon/traefik-forward-auth)

First, you'll need to get your Google tokens, secrets and Ids. To do that, follow the steps in [this article](https://www.smarthomebeginner.com/google-oauth-with-traefik-2-docker/) until you have the required values.

Then make sure that these keys have valid values on your `~/docker/.env` file:
- GOOGLE_CLIENT_ID - follow the steps on the [linked article](https://www.smarthomebeginner.com/google-oauth-with-traefik-2-docker/) to obtain the Id
- GOOGLE_CLIENT_SECRET - follow the steps on the [linked article](https://www.smarthomebeginner.com/google-oauth-with-traefik-2-docker/) to obtain the Id
- OAUTH_SECRET - follow the steps on the [linked article](https://www.smarthomebeginner.com/google-oauth-with-traefik-2-docker/) to obtain the Id
- MY_EMAIL,HER_EMAIL - a list (or just yours) of valid google emails that will be allowed to login with your server
- CLOUDFLARE_API_TOKEN - if you're using Cloudflare. To obtain it go read [this article/guide](https://www.smarthomebeginner.com/cloudflare-settings-for-traefik-docker/)
- CLOUDFLARE_ZONEID - if you're using Cloudflare. To obtain it go read [this article/guide](https://www.smarthomebeginner.com/cloudflare-settings-for-traefik-docker/)
- DUCKDNS_DOMAIN - if you're using DuckDNS instead of Cloudflare, this represents "example" if your DuckDNS domain is "example.duckdns.org"
- OAUTH_PORT - this is already set with the correct value in the provided [env_example](../docker/env_example) file.

### DDNS Companion Containers

With CloudFlare:
- [Docker CloudFlare DDNS](https://github.com/oznu/docker-cloudflare-ddns)
- [Traefik Cloudflare Companion](https://github.com/tiredofit/docker-traefik-cloudflare-companion)
With DuckDNS:
- [DuckDNS](https://hub.docker.com/r/linuxserver/duckdns/)

If you're not using Cloudflare, you should comment the sections of the file associated with the containers `cf-ddns` and `cf-companion`. If you're using DuckDNS, you have to uncomment the `duckdns` container section.

</br>
```
dcup
```
If all went well, Traefik requested new SSL certificates for the specified domain, this time valid ones. Logout of your Google account (or start an incognito session) and navigate to https://traefik.example.pt to be greeted with a Google login form. After a successfull login, you should be on the Traefik dashboard with the information of valid SSL certificates.



To continue, go [back](docker_containers.md#add-containers)