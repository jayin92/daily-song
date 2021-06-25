if [ "$1" == "twitter" ]
then
touch twitter_cred.json
echo '{"consumer_key": "${2}", "consumer_secret": "${3}", "access_token": "${4}", "access_token_secret": "${5}"}' > twitter_cred.json
else
touch .cache
touch spotify_cred.json
echo '{"access_token": "${2}", "token_type": "${3}", "expires_in": ${4}, "scope": "${5}", "expires_at": ${6}, "refresh_token": "${7}"}' > .cache
echo '{"SPOTIPY_CLIENT_ID": "${8}", "SPOTIPY_CLIENT_SECRET": "${9}", "SPOTIFY_REDIRECT_URI": "${10}"}'
fi