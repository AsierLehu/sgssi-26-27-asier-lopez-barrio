# Laboratorio: TOR, ONION

## Requisitos previos

- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP).
- Servidor remoto Google Cloud configurado, con Apache funcionando y el firewall permitiendo conexiones.

## Deep Web

La red habitual y conocida (Clearnet) está formada por direcciones conocidas (Ej: www.ehu.eus), con contenidos en HTML que están indexados y permiten realizar búsquedas para encontrar lo que nos interese.

La Deep Web (internet profunda) está formada por todos aquellos contenidos que no son directamente accesibles a través de internet. Se estima que de todo el contenido que existe:

- El 10% está en Clearnet (el internet que conocemos).
- El 90% está en la Deep Web.

Contenido de la Deep Web:

- Información confidencial o protegida (No suelen estar indexados por buscadores ni se puede acceder directamente a ellos): registros sanitarios, registros académicos, datos bancarios, etc.
- Información "suelta": por ejemplo un archivo HTML que no esté enlazado desde ningún otro.
- Información en formatos no HTML que un navegador no puede leer.
- Contenido no publicable (Censura): contenidos que no pueden publicarse libremente porque pueden acarrear consecuencias.
- Contenido ilegal y/o desagradable (Darknet): tráfico de armas, drogas, personas; material pedófilo; malware; alquiler de hackers, matones, etc.; películas snuff.

Para acceder a la Deep Web hace falta un software especial que proporcione privacidad, anonimato y ejerza de proxy.

Existen varias alternativas que darán acceso a distintos contenidos de la Deep Web: TOR, I2P, Freenet, Zeronet, etc.

## TOR

TOR (The Onion Router) ofrece un método para navegar de forma segura, ya que se oculta la IP de fuente y destino de los nodos que forman la [red](https://community.torproject.org/). Los sitios Onion son direcciones alfanuméricas muy largas, no legibles para humanos, a las que se puede acceder mediante HTTP(S), después de que los paquetes hayan viajado por varios nodos ONION, ocultando el origen y destino de los paquetes. 

Cada vez que hay que hacer una conexión, se calcula un camino aleatorio basado en los nodos de la red:

![TOR](tor.png)

La información se cifra a capas (como una cebolla) con las claves públicas de los distintos nodos, de modo que cada nodo sólo puede ver cuál es el siguiente:

![capas](capas.png)

Utilizando la red TOR se puede acceder a URLs que son inaccesibles de otro modo:

- Dominio `.onion`.
- URLs alfanuméricas: `http://3g2upl4pq6kufc4m.onion/`.

Para encontrar contenidos hay que usar buscadores específicos o sitios donde se recopilen las URLs:

- Buscador Torch (`http://xmh57jrzrnw6insl.onion/`).
- The Hidden Wiki (`http://kpvz7ki2v5agwt35.onion`).

## Navegador TOR

Para acceder a sitios ONION hay que usar un navegador TOR. Descarga el [navegador TOR oficial](https://www.torproject.org/download/) y úsalo para conectarte a [diferentes sitios](https://community.torproject.org/es/onion-services/), como por ejemplo el [New York Times](https://www.nytimesn7cgmftshazwhfgzm37qxb44r64ytbb2dj3x62d2lljsciiyd.onion/).


1. Descargar el [navegador TOR oficial](https://www.torproject.org/download/).
2. Extraer el archivo descargado.
3. En GNU/Linux, entrar en el directorio extraído y ejecutar `./start-tor-browser.desktop`.
4. Pulsar `Conectar` y esperar a que se establezca el circuito con la red TOR.
5. Abrir un servicio ONION conocido, por ejemplo el del [New York Times]
 
(El del NY Times no me va, he probado el de la BBC y sí va: https://www.bbcnewsd73hkzno2ini43t4gblxvycyac5aw4gnv7t2rccijh7745uqd.onion/)

Otros servicios de ejemplo están listados en la [documentación de onion services](https://community.torproject.org/es/onion-services/).

> ¿Por qué crees que abundan los periódicos entre los sitios que ofrecen servicios ONION?

## Servicio ONION en Google Cloud

### Instalar TOR

Para instalar TOR en el servidor sigue las [instrucciones comunes](https://community.torproject.org/onion-services/setup/install/) (Hay que tener en cuenta que para instalar TOR hay que configurar unos [repositorios APT específicos](https://support.torproject.org/apt/tor-deb-repo/)).

Para instalarlo simplemente meterse con SSH y ejecutar:
```bash
sudo apt update
sudo apt install tor
```

Un vez instalado TOR, para verificar su funcionamiento, ejecutar en el servidor:

```bash
curl -x socks5h://localhost:9050 -s https://check.torproject.org/api/ip
```

Debería devolver algo así:

```json
{"IsTor":true,"IP":"xxx.xxx.xxx.xxx"}
```

### Configurar servicio ONION

Sigue las [instrucciones comunes](https://community.torproject.org/onion-services/setup/) para configurar el servicio ONION. Ten en cuenta que:

- Apache debe estar funcionando y el firewall debe permitir conexiones. Conviene crear una página web nueva para verificar la conexión mediante ONION.
- Hay que editar el archivo de configuración de TOR para añadir un nuevo Hidden Service.
- Para comprobar la conexión ONION deberás usar la dirección ONION generada en el Hidden Service y el navegador TOR.

### Pasos

En el laboratorio de cifrado, el puerto 80 redirige todo a `https://IP_EXTERNA` y la página «Conexión SSL» se sirve por el 443. Si el Hidden Service entregara las peticiones en ese puerto 80, el navegador TOR saltaría a la IP pública y saldría de la red onion. La página onion va en otro puerto, solo en la propia máquina.

#### 1. Entrar al servidor

```bash
ssh usuario@IP_EXTERNA
```

#### 2. Crear una página distinta de la del sitio SSL

Así se distingue el acceso por onion del acceso por la IP.

```bash
sudo mkdir /var/www/onion-site
sudo nano /var/www/onion-site/index.html
```

```html
<h1>Servicio ONION</h1>
```

#### 3. Crear sitio para apache

No se modifica el VirtualHost del puerto 80 ni el del 443.
En sites-available tenemos para diferentes puertos: 000-default.conf  default-ssl.conf  ssl-site.conf


Y creamos el del sitio de onion-site.conf
```bash
sudo nano /etc/apache2/sites-available/onion-site.conf
```

```apache
Listen 127.0.0.1:8080

<VirtualHost 127.0.0.1:8080>
    DocumentRoot /var/www/onion-site
    <Directory /var/www/onion-site>
        Require all granted
    </Directory>
</VirtualHost>
```
Por que ponemos el Listen?
Los otros sitios no abren ningún puerto. Se enganchan a puertos que Apache ya abrió al instalarse.
En Ubuntu esos puertos están en /etc/apache2/ports.conf, no en los archivos de cada sitio.

127.0.0.1:8080 no aparece en ports.conf. El VirtualHost del onion indica qué página servir si llega algo a esa dirección, pero no abre el puerto. Sin un Listen 127.0.0.1:8080, Apache conoce el sitio y no tiene ningún socket en el 8080, que es lo que te devolvía curl.

----

Dentro de cada archivo .conf hay uno o más bloques <VirtualHost>. Cada bloque ata tres cosas:
Dónde escucha: dirección IP y puerto.
Qué carpeta sirve: DocumentRoot.
Qué hace con la petición: devolver la página o redirigir.


El puerto 8080 no se abre en el firewall de Google Cloud. Desde internet no se alcanza; solo lo usará TOR, dentro de la misma máquina.

#### 4. Activar el sitio y recargar Apache
Habilitar creando un enlace en sites-enabled hacia onion-site.conf
Comprobar configuracion
Volver a leer los sitios para cargar el de onion
```bash
sudo a2ensite onion-site
sudo apache2ctl configtest
sudo systemctl reload apache2
```

`configtest` tiene que responder `Syntax OK`.

#### 5. Comprobar los dos sitios desde el servidor

```bash
curl http://127.0.0.1:8080
curl http://127.0.0.1
```

El primero devuelve «Servicio ONION». El segundo responde con una redirección a `https://IP_EXTERNA`: el sitio del laboratorio de cifrado sigue igual.

#### 6. Publicar esa página con TOR
/etc/tor/torrc es el archivo de configuración del demonio TOR del servidor.

Lo abrimos  para añadir, al final, las dos líneas que convierten la página local en un sitio onion.

```bash
sudo nano /etc/tor/torrc
```

Al final del archivo:

```
HiddenServiceDir /var/lib/tor/mi_servicio/
HiddenServicePort 80 127.0.0.1:8080
```

`HiddenServiceDir` es la carpeta donde TOR guarda la clave y el fichero `hostname` con la dirección `.onion`. Tiene que estar dentro de `/var/lib/tor/`. No hace falta crearla: al reiniciar la crea el usuario `debian-tor`.

`HiddenServicePort` anuncia el puerto 80 de la dirección `.onion` y entrega esas peticiones a Apache en `127.0.0.1:8080`. Quien visita el onion ve el puerto 80; el 8080 no sale de la máquina.

#### 7. Reiniciar TOR y leer la dirección

```bash
sudo systemctl restart tor
sudo cat /var/lib/tor/mi_servicio/hostname
```

La salida es una dirección de 56 caracteres acabada en `.onion`. Mientras se conserven los ficheros de esa carpeta, la dirección no cambia.



#### 8. Abrirla en el navegador TOR de la máquina local

Hay que meterse en el navegador TOR y ahi meter la direccion, desde Chrome no va.

Al meterse sale algo así

`http://ESA_DIRECCION.onion/`

Tiene que aparecer «Servicio ONION». La primera vez tarda unos segundos, mientras se construye el circuito. 

En un navegador normal como Chrome, si nos metemos en `https://IP_EXTERNA` sigue mostrando «Conexión SSL», por lo que sabemos que no nos hemos cargado nada.

![Servicio ONION](<servicio Onion.png>)


