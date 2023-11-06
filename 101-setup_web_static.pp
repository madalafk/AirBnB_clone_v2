# Configures a web server for deployment of web_static.

package { 'nginx':
  ensure   => 'installed',
}

file { '/data':
  ensure  => directory,
}

file { '/data/web_static':
  ensure => directory,
}

file { '/data/web_static/releases':
  ensure => directory,
}

file { '/data/web_static/releases/test':
  ensure => directory,
}

file { '/data/web_static/shared':
  ensure => directory,
}

file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => "<html>
	  <head>
	  </head>
	< body>
		  Holberton School
	  </body>
</html>",
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/',
}

file { '/var/www':
  ensure => directory,
}

file { '/var/www/html':
  ensure => directory,
}

file { '/var/www/error':
  ensure => directory,
}

file { '/var/www/html/index.html':
  ensure  => present,
  content => "Hello World!\n",
}

file { '/var/www/error/404.html':
  ensure  => present,
  content => "Ceci n'est pas une page",
}

file { '/etc/nginx/sites-available/default':
  ensure  => present,
  content => "server {
    listen 80;
    listen [::]:80 default_server;

    add_header X-Served-By \$hostname;

	  root /var/www/html/;
    index index.html index.htm index.nginx-debian.html;

    server_name _;

    location / {
        try_files \$uri \$uri/ =404;
    }

	  location /hbnb_static/ {
        alias /data/web_static/current/;
	}

    error_page 404 /404.html;
    location = /404.html {
        root /var/www/error/;
        internal;
    }
}",
}

exec { 'nginx restart':
  path => '/etc/init.d/',
}
