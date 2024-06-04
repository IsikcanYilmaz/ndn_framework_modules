#!/usr/bin/env bash

NDN_LOG_DIR="$HOME/ndn_log"
NDN_CONF_DIR="/usr/local/etc/ndn/"
NFD_CONF="$NDN_CONF_DIR/nfd.conf"
NLSR_CONF="$NDN_CONF_DIR/nlsr.conf"
CLIENT_CONF="$NDN_CONF_DIR/client.conf"

DEBUG_LEVEL="ERROR"
CS_MAX_PACKETS="65536"
CS_POLICY="lru"
CS_UNSOLICITED="drop-all"

AD_HOC=0

function fresh_confs()
{
	# Init. Create log directory. Copy over fresh config files.
	mkdir -p $NDN_LOG_DIR
	cp nfd.conf.sample $NDN_CONF_DIR/nfd.conf
	cp nlsr.conf.sample $NDN_CONF_DIR/nlsr.conf
	cp client.conf.sample $NDN_CONF_DIR/client.conf
}

function nfd_conf()
{
	# NFD conf
	infoedit -f $NFD_CONF -s log.default_level -v $DEBUG_LEVEL
	infoedit -f $NFD_CONF -s face_system.unix.path -v /run/nfd/nfd.sock
	infoedit -f $NFD_CONF -s tables.cs_max_packets -v $CS_MAX_PACKETS 
	infoedit -f $NFD_CONF -s tables.cs_policy -v $CS_POLICY
	infoedit -f $NFD_CONF -s tables.cs_unsolicited_policy -v $CS_UNSOLICITED

	# Client conf
	sudo sed -i "s|;transport|transport|g" $CLIENT_CONF
	#sudo sed -i "s|nfd.sock|nfd.sock|g" $CLIENT_CONF
}

function nlsr_conf()
{
	# NLSR conf
	infoedit -f $NLSR_CONF -s general.network -v /ndn/
	infoedit -f $NLSR_CONF -s general.site -v /$HOSTNAME-site
	infoedit -f $NLSR_CONF -s general.router -v /%C1.Router/cs/$HOSTNAME
	infoedit -f $NLSR_CONF -s general.state-dir -v $NDN_LOG_DIR
	infoedit -f $NLSR_CONF -s general.sync-protocol -v psync

	infoedit -f $NLSR_CONF -s hyperbolic.state -v off
	infoedit -f $NLSR_CONF -s hyperbolic.radius -v 0.5
	infoedit -f $NLSR_CONF -s hyperbolic.angle -v 2.65

	infoedit -f $NLSR_CONF -s fib.max-faces-per-prefix -v 3 
	infoedit -f $NLSR_CONF -d advertising.prefix
	infoedit -f $NLSR_CONF -s advertising.prefix -v /ndn/$HOSTNAME-site/$HOSTNAME 
	infoedit -f $NLSR_CONF -d security.cert-to-publish 
	infoedit -f $NLSR_CONF -s security.validator.trust-anchor.type -v any
	infoedit -f $NLSR_CONF -d security.validator.trust-anchor.file-name
	infoedit -f $NLSR_CONF -s security.prefix-update-validator.trust-anchor.type -v any
	infoedit -f $NLSR_CONF -d security.prefix-update-validator.trust-anchor.file-name
}

function setup_confs()
{
	fresh_confs
	nfd_conf
	nlsr_conf
}

function nfd_create_faces()
{
	infoedit -f $NLSR_CONF -d neighbors.neighbor
	IFS=$'\n'
	for i in $(cat /etc/hosts | grep raspberry | grep -v 127.0); do
		facename=$(echo $i | awk '{print $2}')
		faceip=$(echo $i | awk '{print $1}')
		if [ $AD_HOC == 1 ]; then
			faceip=$(echo $faceip | sed 's/192.168.6/192.168.1/g')
		fi
		echo "Creating face to $facename udp://$faceip"
		nfdc face create udp://$faceip permanent
		infoedit -f $NLSR_CONF -a neighbors.neighbor <<<"name /ndn/$facename-site/%C1.Router/cs/$facename face-uri udp://$faceip"
	done
	unset IFS
}

function nfd_shortcut()
{
	fresh_confs
	nfd_conf
	nfd-start
	nlsr_conf
	nfd_create_faces
	nlsr -f $NLSR_CONF &
}

function poketest()
{
	nlsrc advertise $1; echo $2 | ndnpoke $1 &
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    nfd_shortcut
fi
