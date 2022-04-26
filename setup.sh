mkdir -p ~/.streamlit/
echo "[general]
email = \"replace_this_with_your_email@email\"
" > ~/.streamlit/credentials.toml
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml