# Skill: Video Pipeline — /video

Pipeline completa de edição de vídeo com IA para o projeto FotiVidio.

## Quando usar
Quando o usuário pedir para criar, editar, ou processar vídeos. Inclui:
- Buscar B-rolls no Pexels
- Transcrever áudio/vídeo automaticamente
- Aplicar chromakey, split screen, zoom, overlays
- Gerar legendas (SRT) a partir de transcrição
- Renderizar composições com Remotion

## Fluxo padrão

### 1. Transcrição automática
```js
const { TranscriptionService } = require('./src/services/transcription');
const svc = new TranscriptionService(process.env.DEEPGRAM_API_KEY);
const result = await svc.transcribeFile('input.mp4', { language: 'pt-BR' });
const srt = svc.generateSRT(result.words);
```

### 2. Buscar B-rolls no Pexels
```js
const { PexelsService } = require('./src/services/pexels');
const pexels = new PexelsService(process.env.PEXELS_API_KEY);
const results = await pexels.searchVideos('nature', { perPage: 5 });
await pexels.downloadVideo(url, 'assets/videos/broll.mp4');
```

### 3. Efeitos com FFmpeg
```js
const { FFmpegService } = require('./src/services/ffmpeg');
const ff = new FFmpegService();
await ff.chromakey('input.mp4', 'output.mp4');
await ff.splitScreen('left.mp4', 'right.mp4', 'split.mp4');
await ff.zoom('input.mp4', 'zoomed.mp4', { zoomFactor: 1.5 });
await ff.addSubtitles('input.mp4', 'subs.srt', 'subtitled.mp4');
await ff.concat(['clip1.mp4', 'clip2.mp4'], 'final.mp4');
```

### 4. Renderizar com Remotion
```bash
npx remotion render src/remotion/Root.jsx FotiVidio out/video.mp4
```

## Estrutura do projeto
```
src/
  services/
    pexels.js       — Busca e download de vídeos/fotos do Pexels
    transcription.js — Transcrição automática via Deepgram
    ffmpeg.js        — Efeitos de vídeo (chromakey, split, zoom, overlay)
  remotion/
    Root.jsx         — Entry point do Remotion
    VideoComposition.jsx — Composição principal com clips e legendas
```

## Variáveis de ambiente necessárias
- `PEXELS_API_KEY` — Chave da API do Pexels
- `DEEPGRAM_API_KEY` — Chave da API do Deepgram (transcrição)
