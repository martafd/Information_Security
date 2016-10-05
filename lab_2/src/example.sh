#!/bin/bash
echo "------------ Welcome to installer! ------------"
echo "-----------------------------------------------"
echo ""
echo "Print path to folder, where you want to install program"
read path
#echo "current paths =  $HOME/$path"
SOURCE = $(readlink -f $0)  # source file location
echo " SOURCE = $PWD"  # source file location

#create folder to install program
if [ ! -d "$HOME/$path" ]; then
    mkdir -p $HOME/$path
    echo "Folder created"
    make
    cp -r $PWD/dist/main/. $HOME/$path
    echo "Writing info.txt ....."
    echo "----- Some information about computer -----"  >> $HOME/$path/info.txt
    echo "User name: `whoami`" >> $HOME/$path/info.txt
    echo "OS: `uname`" >> $HOME/$path/info.txt
    echo "Computer name: `hostname`" >> $HOME/$path/info.txt
#    echo "Product name: `sudo dmidecode -s system-product-name`"  >> $HOME/$path/info.txt
#    echo "Manufacturer: `sudo dmidecode -s system-manufacturer`"  >> $HOME/$path/info.txt
    echo "Path to sys bin files: `find / -name "sbin"`"  >> $HOME/$path/info.txt
    echo "Keyboard `setxkbmap -query | grep layout`"  >> $HOME/$path/info.txt
    echo "Screen height: `xrandr --current | grep '*' | uniq | awk '{print $1}' | cut -d 'x' -f2`"  >> $HOME/$path/info.txt
    echo "`grep MemTotal /proc/meminfo`"  >> $HOME/$path/info.txt
    echo "Disk storage: `df | grep '^/dev/[hs]d' | awk '{s+=$2} END {print s/1048576}'` GB"  >> $HOME/$path/info.txt
    echo "`md5sum info.txt | awk '{ print $1 }'`"  >> $HOME/$path/hash_info.txt

else
echo "Program already installed!"
    #./dist/main/main
fi

exit 0

