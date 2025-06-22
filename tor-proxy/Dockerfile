FROM alpine:latest

RUN apk add --no-cache curl tor ca-certificates libcap mailcap socat bash && rm -rf /var/cache/apk/*     

RUN set -eux; \
	mkdir -p \
		/config/caddy \
		/data/caddy \
		/etc/caddy \
		/usr/share/caddy \
	; 

# https://github.com/caddyserver/caddy/releases
ENV CADDY_VERSION=v2.10.0

RUN set -eux; \
	apkArch="$(apk --print-arch)"; \
	case "$apkArch" in \
		x86_64)  binArch='amd64'; checksum='626682d623ca04356ab3c9a93a82386cfde6d8243b11f2d0eea9e97ba630c7ada62373401e96b72c6690c98ae8dd004d61fafe477f5249690d5cb251ebbfd2d9' ;; \
		armhf)   binArch='armv6'; checksum='c4647ed1b5407bd61d55f357af62d3935f2972bb5b03472a2747c4c19610376174bdb573f10b936cbc81acd8a103a0b961118d360cebe2b60693161f83e7f046' ;; \
		armv7)   binArch='armv7'; checksum='e6794aef179ec3319c5d692fedbb424532a47d7caf19a67ad2a4317c5f2776baaf47658f9e1f7fd37d6f3447a18285cd1d7cb91d0088f5cd01d73874a43aa9c2' ;; \
		aarch64) binArch='arm64'; checksum='6d100bfd609e8cfe6a51afe1b86066ac68f53ac56670c74a7d7537d93c643aa7f0e82b9f3083218eee1d369a427bfcdafcb445c7a730f9fc0ddf546401d95484' ;; \
		ppc64el|ppc64le) binArch='ppc64le'; checksum='9559d544b8f919837f66623955fd95b03511d85c56455f43d9cc6d0010c00bb1e81fc3b7b5e5a2f8d1d0f65d9571c80cb8b706ea94e2baaaeffec5ae52f68a34' ;; \
		riscv64) binArch='riscv64'; checksum='9633d6f6c2bf1911d5887a5d0ea885413785e0968550875b995eecc3bb5fbd1267edec0add94a0286349273e4df0dc1f1067d5639c2393019e235536c1b7c477' ;; \
		s390x)   binArch='s390x'; checksum='5b29b377409abb9b8d241b95a11f1dd5d709759760b1514c9fbf616c3975048cf384441527fdc179bb8b08dc6189afe9df33499b46509e5d0e3bd6da8bb293b1' ;; \
		*) echo >&2 "error: unsupported architecture ($apkArch)"; exit 1 ;;\
	esac; \
	wget -O /tmp/caddy.tar.gz "https://github.com/caddyserver/caddy/releases/download/v2.10.0/caddy_2.10.0_linux_${binArch}.tar.gz"; \
	echo "$checksum  /tmp/caddy.tar.gz" | sha512sum -c; \
	tar x -z -f /tmp/caddy.tar.gz -C /usr/bin caddy; \
	rm -f /tmp/caddy.tar.gz; \
	setcap cap_net_bind_service=+ep /usr/bin/caddy; \
	chmod +x /usr/bin/caddy; \
	caddy version

EXPOSE 80
EXPOSE 443 

COPY ./torrc /etc/tor/torrc
COPY ./Caddyfile /etc/caddy/Caddyfile
COPY ./start.sh /home/start.sh

RUN chmod +x /home/start.sh

#HEALTHCHECK --interval=300s --timeout=15s --start-period=60s --start-interval=10s \
#    CMD curl -x socks5h://127.0.0.1:9050 'https://check.torproject.org/api/ip' | grep -qm1 -E '"IsTor"\s*:\s*true'

VOLUME ["/var/lib/tor"]

USER tor

CMD ["/bin/sh", "/home/start.sh"]
