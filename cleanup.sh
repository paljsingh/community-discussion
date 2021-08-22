#!/bin/bash

cat <<EOF | mongo c18n &>/dev/null
db.user.drop()
db.community.drop()
db.usergroup.drop()
db.invite.drop()
db.post.drop()
db.image.drop()
db.video.drop()
EOF

rm -rf var/data/mongo/* var/data/images/* var/data/videos/* var/data/kafka/* var/data/spark/*
