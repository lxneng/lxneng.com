upstream lxneng {
    server 127.0.0.1:1986; 
}
server{
    listen 80;
    server_name lxneng.com;
    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass   http://lxneng;
    }

}
server {
    listen       80;
    server_name  www.lxneng.com;
    rewrite ^ $scheme://lxneng.com$request_uri? permanent;
}
server {
    listen       80;
    server_name  blog.lxneng.com;
    rewrite ^ $scheme://lxneng.com/posts permanent;
}
server {
    listen       80;
    server_name  *.lxneng.com;
    rewrite ^ $scheme://lxneng.com$request_uri? permanent;
}

#server {
#    listen       80;
#    server_name  lxneng.com;
#    root /var/www/lxneng.com;
#    location ~ ^/downloads/.* {
#        auth_basic "Please input your username and password!";	
#        auth_basic_user_file /etc/nginx/auth/lxneng.com.pass;
#        charset utf8;
#        autoindex on;
#    }
#    location ~ \.mp4$ {
#        mp4;
#    }
#}

server {
    listen      80;
    server_name x.lxneng.com;
    root /var/www/lxneng/wd/wordpress;
    location / { 
        index index.html index.htm index.php;
    }

     location ~ \.php$ {
         fastcgi_pass   127.0.0.1:9000;
         fastcgi_index  index.php;
         include /etc/nginx/fastcgi_params;
     }
}
