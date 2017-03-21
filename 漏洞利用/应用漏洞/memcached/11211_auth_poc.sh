if [ ! $1 ]
then
	echo "Usage: base $0 ip [port]"
	exit
fi

if [ $2 ]
then
	nc $1 $2 << EOF
stats
EOF
else
	nc $1 "11211" << EOF
stats
EOF
fi

