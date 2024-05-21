FROM nginx:alpine

# Nginxメイン設定ファイルをコピー
COPY nginx.conf /etc/nginx/nginx.conf

# 仮想サーバー設定ファイルをコピー
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf

# publicディレクトリをドキュメントルートにコピー
COPY public /usr/share/nginx/html
