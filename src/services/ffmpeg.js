const ffmpeg = require('fluent-ffmpeg');
const path = require('path');

class FFmpegService {
  chromakey(inputPath, outputPath, { color = '00ff00', similarity = 0.3, blend = 0.1 } = {}) {
    return new Promise((resolve, reject) => {
      ffmpeg(inputPath)
        .videoFilters(`chromakey=${color}:${similarity}:${blend}`)
        .output(outputPath)
        .on('end', resolve)
        .on('error', reject)
        .run();
    });
  }

  overlay(basePath, overlayPath, outputPath, { x = 0, y = 0, scale } = {}) {
    return new Promise((resolve, reject) => {
      const cmd = ffmpeg()
        .input(basePath)
        .input(overlayPath);

      const filters = [];
      if (scale) filters.push(`[1:v]scale=${scale}[ovrl]`);
      const overlayLabel = scale ? '[ovrl]' : '[1:v]';
      filters.push(`[0:v]${overlayLabel}overlay=${x}:${y}`);

      cmd
        .complexFilter(filters)
        .output(outputPath)
        .on('end', resolve)
        .on('error', reject)
        .run();
    });
  }

  splitScreen(leftPath, rightPath, outputPath, { width = 1920, height = 1080 } = {}) {
    const halfW = Math.floor(width / 2);
    return new Promise((resolve, reject) => {
      ffmpeg()
        .input(leftPath)
        .input(rightPath)
        .complexFilter([
          `[0:v]scale=${halfW}:${height},setsar=1[left]`,
          `[1:v]scale=${halfW}:${height},setsar=1[right]`,
          `[left][right]hstack=inputs=2`,
        ])
        .output(outputPath)
        .on('end', resolve)
        .on('error', reject)
        .run();
    });
  }

  zoom(inputPath, outputPath, { zoomFactor = 1.5, duration = 3 } = {}) {
    return new Promise((resolve, reject) => {
      ffmpeg(inputPath)
        .videoFilters(
          `zoompan=z='min(zoom+${(zoomFactor - 1) / (duration * 25)},${zoomFactor})':d=${duration * 25}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080`
        )
        .output(outputPath)
        .on('end', resolve)
        .on('error', reject)
        .run();
    });
  }

  concat(inputPaths, outputPath) {
    return new Promise((resolve, reject) => {
      const cmd = ffmpeg();
      inputPaths.forEach(p => cmd.input(p));

      const filters = inputPaths.map((_, i) => `[${i}:v][${i}:a]`).join('');
      cmd
        .complexFilter(`${filters}concat=n=${inputPaths.length}:v=1:a=1`)
        .output(outputPath)
        .on('end', resolve)
        .on('error', reject)
        .run();
    });
  }

  addSubtitles(inputPath, srtPath, outputPath, { fontSize = 24, fontColor = 'white' } = {}) {
    return new Promise((resolve, reject) => {
      ffmpeg(inputPath)
        .videoFilters(`subtitles=${srtPath}:force_style='FontSize=${fontSize},PrimaryColour=&H00${fontColor === 'white' ? 'FFFFFF' : fontColor}&'`)
        .output(outputPath)
        .on('end', resolve)
        .on('error', reject)
        .run();
    });
  }

  extractAudio(inputPath, outputPath) {
    return new Promise((resolve, reject) => {
      ffmpeg(inputPath)
        .noVideo()
        .audioCodec('pcm_s16le')
        .audioFrequency(16000)
        .audioChannels(1)
        .output(outputPath)
        .on('end', resolve)
        .on('error', reject)
        .run();
    });
  }

  getInfo(inputPath) {
    return new Promise((resolve, reject) => {
      ffmpeg.ffprobe(inputPath, (err, metadata) => {
        if (err) return reject(err);
        resolve(metadata);
      });
    });
  }
}

module.exports = { FFmpegService };
