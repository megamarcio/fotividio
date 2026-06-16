const { PexelsService } = require('./services/pexels');
const { TranscriptionService } = require('./services/transcription');
const { FFmpegService } = require('./services/ffmpeg');

function createPipeline({ pexelsKey, deepgramKey } = {}) {
  const pexels = pexelsKey ? new PexelsService(pexelsKey) : null;
  const transcription = deepgramKey ? new TranscriptionService(deepgramKey) : null;
  const ffmpeg = new FFmpegService();

  return { pexels, transcription, ffmpeg };
}

module.exports = { createPipeline, PexelsService, TranscriptionService, FFmpegService };
