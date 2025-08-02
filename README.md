# App-para-baixar-todos-os-videos-de-uma-conta-no-tiktok
Um aplicativo que te permitirá baixar todos os vídeos de uma conta pública qualquer no tiktok.

Como utilizar o app?

1. Baixe o python
2. Baixe as bibliotecas necessárias: Flask, Flask_cors, yt-dlp
3. Baixe a extensão EditThisCookie no seu navegador e certifique-se que ao exportar os cookies, eles estejam no formato Netscape. Vá nas configurações para realizar este ajuste.
4. Abra o tiktok logado em sua conta, exporte os seus cookies em Netscape e os cole em cookies.txt
5. Altere, no backend_app.py o valor da variável YT_DLP_EXECUTABLE para o caminho onde está baixado o yt-dlp.exe (normalmente, o caminho é: C:\\Users\\SeuUsuario\\AppData\\Local\\Programs\\Python\\Python39\\Scripts\\yt-dlp.exe
6. Abra seu executor de código preferido (vscode por exemplo) e abra a pasta "Baixar vídeos de um perfil do Tiktok" nele.
7. Execute o backend_app.py
8. Abra o explorador de arquivos, clique 2 vezes no index.html e o execute em seu navegador preferido (de preferencia, no chrome).
9. Coloque o link para o perfil que vc quer baixar no site e pronto!
