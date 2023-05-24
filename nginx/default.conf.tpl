upstream starter {
    server web:$PORT;
}

server {

    listen 80;

    location /static {
        alias /vol/static;
    }
    
    location / {
        proxy_pass              http://starter;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header        Host web;
        proxy_redirect          off;
        client_max_body_size    10M;
    }

    location /ws/ {
        proxy_set_header Host               $http_host;
        proxy_set_header X-Real-IP          $remote_addr;
        proxy_set_header X-Forwarded-For    $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host   $server_name;
        proxy_set_header X-Forwarded-Proto  $scheme;
        proxy_set_header X-Url-Scheme       $scheme;
        proxy_redirect off;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;

        proxy_pass http://starter;
    }
}