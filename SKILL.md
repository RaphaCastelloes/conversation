---
name: whatsapp-audio-sender
description: Envia áudios de texto-para-voz (TTS) para o WhatsApp, garantindo a compatibilidade com o formato OGG (Opus). Use para enviar mensagens de áudio geradas por texto diretamente para o WhatsApp do usuário.
---

# WhatsApp Audio Sender

Este skill automatiza o processo de enviar mensagens de áudio geradas por texto para o WhatsApp do usuário, garantindo que o formato seja compatível (OGG com codec Opus).

## Fluxo de Trabalho do Agente

Quando uma solicitação para enviar áudio TTS para o WhatsApp for recebida, o agente deve seguir os seguintes passos:

1.  **Gerar o áudio TTS (MP3):** Use a ferramenta `tts` com a mensagem fornecida pelo usuário.
    ```python
    tts_response = default_api.tts(text = "<mensagem_do_usuario>")
    mp3_path = tts_response["tts_response"]["output"]
    ```

2.  **Converter MP3 para OGG (Opus):** Use o skill `mp3-to-ogg` para converter o arquivo MP3 gerado para OGG (Opus), garantindo a compatibilidade com o WhatsApp. Para isso, execute o script `convert_mp3_to_ogg.py` do skill `mp3-to-ogg`.
    ```bash
    # Primeiramente, limpe o prefixo MEDIA: do caminho MP3
    clean_mp3_path = default_api.exec(command = "python /home/opc/.openclaw/workspace/skills/path-cleaner/scripts/clean_media_path.py " + mp3_path)
    clean_mp3_path = clean_mp3_path["exec_response"]["output"].strip()

    # Converta para OGG
    ogg_conversion_output = default_api.exec(command = "python /home/opc/.openclaw/workspace/skills/mp3-to-ogg/scripts/convert_mp3_to_ogg.py " + clean_mp3_path)
    ogg_path = ogg_conversion_output["exec_response"]["output"].strip().split('\n')[-1]
    ```

3.  **Enviar o áudio OGG para o WhatsApp:** Utilize a ferramenta `message` com o caminho do arquivo OGG e o número do destinatário (obter do `USER.md`).
    ```python
    user_number = "+553288314794" # Substitua pelo número real do USER.md
    default_api.message(action = "send", channel = "whatsapp", media = ogg_path, message = "<mensagem_original>", to = user_number)
    ```

O resultado final será o envio de um áudio OGG compatível com o WhatsApp contendo a mensagem de texto fornecida.
