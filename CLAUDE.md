# FotiVidio

Pipeline de edição de vídeo com IA: chromakey, B-rolls (Pexels), split screen, zoom, legendas automáticas, e renderização programática.

## Stack

- **Remotion** — Composição e renderização de vídeo programático (React)
- **FFmpeg** — Processamento de vídeo (chromakey, split screen, zoom, overlay, concat, legendas)
- **Pexels API** — Busca e download de B-rolls e imagens de stock
- **Deepgram** — Transcrição automática de áudio/vídeo (pt-BR, modelo nova-3)

## Comandos

```bash
npm install                # instalar dependências
npx remotion preview src/remotion/Root.jsx   # preview do Remotion
npx remotion render src/remotion/Root.jsx FotiVidio out/video.mp4  # renderizar
```

## Estrutura

```
src/
  index.js               — Entry point e factory
  services/
    pexels.js            — Serviço Pexels (busca + download)
    transcription.js     — Transcrição automática (Deepgram)
    ffmpeg.js            — Efeitos FFmpeg
  remotion/
    Root.jsx             — Composições Remotion
    VideoComposition.jsx — Componente principal de vídeo
.claude/skills/
    video-pipeline.md    — Skill personalizada /video
```

## Variáveis de ambiente

Copie `.env.example` para `.env` e preencha as chaves:
- `PEXELS_API_KEY`
- `DEEPGRAM_API_KEY`
