const { createClient } = require('@deepgram/sdk');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class TranscriptionService {
  constructor(apiKey) {
    this.deepgram = createClient(apiKey);
  }

  async transcribeFile(filePath, { language = 'pt-BR', model = 'nova-3' } = {}) {
    const audioPath = await this._extractAudio(filePath);
    const audioBuffer = fs.readFileSync(audioPath);

    const { result } = await this.deepgram.listen.prerecorded.transcribeFile(
      audioBuffer,
      {
        model,
        language,
        smart_format: true,
        paragraphs: true,
        utterances: true,
        diarize: true,
      }
    );

    if (audioPath !== filePath) fs.unlinkSync(audioPath);

    return this._formatResult(result);
  }

  async transcribeUrl(url, { language = 'pt-BR', model = 'nova-3' } = {}) {
    const { result } = await this.deepgram.listen.prerecorded.transcribeUrl(
      { url },
      {
        model,
        language,
        smart_format: true,
        paragraphs: true,
        utterances: true,
        diarize: true,
      }
    );

    return this._formatResult(result);
  }

  async _extractAudio(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    if (['.wav', '.mp3', '.flac', '.ogg', '.m4a'].includes(ext)) return filePath;

    const outputPath = filePath.replace(ext, '.wav');
    execSync(`ffmpeg -i "${filePath}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "${outputPath}" -y`, {
      stdio: 'pipe',
    });
    return outputPath;
  }

  _formatResult(result) {
    const channel = result.results?.channels?.[0];
    const transcript = channel?.alternatives?.[0]?.transcript || '';
    const words = channel?.alternatives?.[0]?.words || [];
    const paragraphs = channel?.alternatives?.[0]?.paragraphs?.paragraphs || [];
    const utterances = result.results?.utterances || [];

    return {
      transcript,
      words: words.map(w => ({
        word: w.word,
        start: w.start,
        end: w.end,
        confidence: w.confidence,
        speaker: w.speaker,
      })),
      paragraphs: paragraphs.map(p => ({
        text: p.sentences?.map(s => s.text).join(' ') || '',
        start: p.start,
        end: p.end,
        speaker: p.speaker,
      })),
      utterances: utterances.map(u => ({
        text: u.transcript,
        start: u.start,
        end: u.end,
        speaker: u.speaker,
        confidence: u.confidence,
      })),
    };
  }

  generateSRT(words) {
    const lines = [];
    let idx = 1;
    for (let i = 0; i < words.length; i += 8) {
      const chunk = words.slice(i, i + 8);
      const start = this._formatTimestamp(chunk[0].start);
      const end = this._formatTimestamp(chunk[chunk.length - 1].end);
      const text = chunk.map(w => w.word).join(' ');
      lines.push(`${idx}\n${start} --> ${end}\n${text}\n`);
      idx++;
    }
    return lines.join('\n');
  }

  _formatTimestamp(seconds) {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    const ms = Math.round((seconds % 1) * 1000);
    return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')},${String(ms).padStart(3, '0')}`;
  }
}

module.exports = { TranscriptionService };
