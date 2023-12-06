LOCAL="$HOME/R/bin"

# install jq
apt-get source jq

pushd jq-*
    autoreconfig -i
    ./configure --prefix="$LOCAL"
    make -j4
    make install
popd

# install ticker.sh
pushd "$LOCAL"
    curl -o ticker.sh https://raw.githubusercontent.com/pstadler/ticker.sh/master/ticker.sh
    chmod +x ticker.sh
popd

# install script to use ticker.sh
cp watchStock.sh "$LOCAL"
chmod +x "$LOCAL/watchStock.sh"
