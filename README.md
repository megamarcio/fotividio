# FotiVidio - Video Editing Pipeline

Pipeline de edição de vídeo com chromakey, B-rolls, split screen, zoom effects, e áudio.

## Video Original
- **Título**: Quick Avatar Video_1080p.mp4
- **Duração**: 1:31 (91 segundos)
- **Conteúdo**: Imersão de IA em Orlando para jovens 15-22 anos
- **11 cenas** analisadas com Highsfield AI

## Assets Gerados (Magnific AI)

### Backgrounds (7 imagens)
| Asset | Descrição | Link |
|---|---|---|
| office_1 | Escritório moderno com vista panorâmica | [Ver](https://www.magnific.com/app/creation/MXi8UsmDCm) |
| office_2 | Escritório corporativo variação | [Ver](https://www.magnific.com/app/creation/swEOBpYl8e) |
| office_3 | Escritório com iluminação quente | [Ver](https://www.magnific.com/app/creation/NZjGQfK6D9) |
| abstract_1 | Gradiente azul/dourado abstrato | [Ver](https://www.magnific.com/app/creation/l7uyoQ9gv9) |
| abstract_2 | Gradiente abstrato variação | [Ver](https://www.magnific.com/app/creation/Pi1ZCr842C) |
| dashboard_1 | Dashboard futurista de marketing | [Ver](https://www.magnific.com/app/creation/SOF4I5NUb8) |
| dashboard_2 | Dashboard digital variação | [Ver](https://www.magnific.com/app/creation/e8ZmJzkdqL) |

### B-Rolls Animados (7 vídeos)
| Asset | Descrição | Link |
|---|---|---|
| workspace | Workspace moderno com laptop | [Ver](https://www.magnific.com/app/creation/mCcQR5fhJQ) |
| marketing_graphs | Gráficos de marketing crescendo | [Ver](https://www.magnific.com/app/creation/y6kREnnPW9) |
| city_aerial | Cidade aérea ao pôr do sol | [Ver](https://www.magnific.com/app/creation/br8LV7c5Y2) |
| ai_chatbot | Mãos digitando com ChatGPT | [Ver](https://www.magnific.com/app/creation/9RxAFu1NYZ) |
| orlando_aerial | Orlando vista aérea | [Ver](https://www.magnific.com/app/creation/43r2QFE9Aa) |
| ai_hand | Mão robótica tocando humana | [Ver](https://www.magnific.com/app/creation/Vd6owJGMMU) |
| students | Alunos em sala de aula moderna | [Ver](https://www.magnific.com/app/creation/cD4dglZ0eP) |

### Áudio (2 tracks)
| Asset | Descrição | Link |
|---|---|---|
| bg_music | Música corporativa motivacional (2min) | [Ver](https://www.magnific.com/app/creation/8vnC94sIrU) |
| transition_sfx | Efeito whoosh de transição | [Ver](https://www.magnific.com/app/creation/br8LVZ85Y2) |

## HeyGen Video Agent
- **Sessão**: https://app.heygen.com/video-agent/246c25f48046435a92c6f8ff1df746c2
- **Avatar**: Marcio Cavalcante
- **Script**: Narração original em português
- **Status**: Em processamento

## Ferramentas utilizadas

- **Magnific** (20k créditos Premium) - Backgrounds, B-rolls, música, SFX
- **HeyGen** (149 créditos Creator) - Video Agent com avatar do Marcio
- **Highsfield** (38 créditos Plus) - Análise de cenas
- **FFmpeg** (local) - Chromakey, zoom, split screen, composição

## Como usar o script local

```bash
pip install requests
python3 edit_video.py --input video_original.mp4
```

O script baixa todos os assets automaticamente, faz chromakey, compõe com fundos,
adiciona B-rolls, zoom, split screen, música e efeitos sonoros.
