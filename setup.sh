#!/usr/bin/env bash

echo "[*] Getting submodules"
git submodule update --recursive --init

echo "[?] Should the built software be installed? (as opposed to just built) (y/n)"
read doInstall

which bear
bearExists=$?
BEAR_CMD=""
if [ $bearExists -eq 0 ]; then
	BEAR_CMD="bear -- "
fi

JOBS=1

###############################
# ndn-cxx # https://docs.named-data.net/ndn-cxx/current/INSTALL.html#
echo "[*] Installing ndn-cxx"
sudo apt install build-essential pkg-config python3-minimal libboost-all-dev libssl-dev libsqlite3-dev
cd ndn-cxx
./waf configure --with-examples --with-tests
$BEAR_CMD ./waf -j $JOBS
if [ "$doInstall" == "y" ]; then
	sudo ./waf install
	sudo ldconfig
fi
cd ..

###############################
# NFD # https://docs.named-data.net/NFD/current/INSTALL.html
echo "[*] Installing NFD"
sudo apt install libpcap-dev libsystemd-dev
cd NFD
./waf configure
$BEAR_CMD ./waf -j $JOBS
if [ "$doInstall" == "y" ]; then
	sudo ./waf install
	sudo cp /usr/local/etc/ndn/nfd.conf.sample /usr/local/etc/ndn/nfd.conf
fi
cd ..

###############################
# PSync # https://github.com/named-data/PSync#build
echo "[*] Installing PSync"
cd PSync
./waf configure --with-examples
$BEAR_CMD ./waf -j $JOBS
if [ "$doInstall" == "y" ]; then
	sudo ./waf install
fi
cd ..

###############################
# ndn-svs # https://github.com/named-data/ndn-svs?tab=readme-ov-file#installation
echo "[*] Installing ndn-svs"
cd ndn-svs
./waf configure --with-examples
$BEAR_CMD ./waf -j $JOBS
if [ "$doInstall" == "y" ]; then
	sudo ./waf install
fi
cd ..

###############################
# NLSR # https://docs.named-data.net/NLSR/current/INSTALL.html
echo "[*] Installing NLSR"
cd NLSR
./waf configure --with-psync --with-svs --with-tests
$BEAR_CMD ./waf -j $JOBS
if [ "$doInstall" == "y" ]; then
	sudo ./waf install
fi
cd ..

###############################
# ndn-tools # https://github.com/named-data/ndn-tools
echo "[*] Installing ndn-tools"
cd ndn-tools
./waf configure --with-tests
$BEAR_CMD ./waf -j $JOBS
if [ "$doInstall" == "y" ]; then
	sudo ./waf install
fi
cd ..

###############################
# ndn-traffic-generator # https://github.com/named-data/ndn-traffic-generator
echo "[*] Installing ndn-traffic-generator"
cd ndn-traffic-generator
./waf configure
$BEAR_CMD ./waf -j $JOBS
if [ "$doInstall" == "y" ]; then
	sudo ./waf install
fi
cd ..

###############################
# infoedit # https://github.com/NDN-Routing/infoedit
echo "[*] Installing infoedit"
cd infoedit
make
if [ "$doInstall" == "y" ]; then
	sudo make install
fi
cd ..

###############################

echo "[?] Install Mini-NDN? (y/n)"
read doInstallMinindn
if [ "$doInstallMinindn" == "y" ]; then
	cd mini-ndn
	./install.sh
	cd ..
fi

###############################
echo "[*] Done"
