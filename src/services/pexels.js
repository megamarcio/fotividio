const axios = require('axios');

const PEXELS_BASE_URL = 'https://api.pexels.com';

class PexelsService {
  constructor(apiKey) {
    this.client = axios.create({
      baseURL: PEXELS_BASE_URL,
      headers: { Authorization: apiKey },
    });
  }

  async searchVideos(query, { perPage = 10, page = 1, orientation, size } = {}) {
    const params = { query, per_page: perPage, page };
    if (orientation) params.orientation = orientation;
    if (size) params.size = size;
    const { data } = await this.client.get('/videos/search', { params });
    return data;
  }

  async searchPhotos(query, { perPage = 10, page = 1, orientation, size } = {}) {
    const params = { query, per_page: perPage, page };
    if (orientation) params.orientation = orientation;
    if (size) params.size = size;
    const { data } = await this.client.get('/v1/search', { params });
    return data;
  }

  async getVideo(id) {
    const { data } = await this.client.get(`/videos/videos/${id}`);
    return data;
  }

  async downloadVideo(url, outputPath) {
    const fs = require('fs');
    const response = await axios({ url, responseType: 'stream' });
    const writer = fs.createWriteStream(outputPath);
    response.data.pipe(writer);
    return new Promise((resolve, reject) => {
      writer.on('finish', resolve);
      writer.on('error', reject);
    });
  }

  getBestVideoFile(video, quality = 'hd') {
    const files = video.video_files || [];
    const sorted = files.sort((a, b) => (b.width || 0) - (a.width || 0));
    if (quality === 'hd') return sorted.find(f => f.quality === 'hd') || sorted[0];
    if (quality === 'sd') return sorted.find(f => f.quality === 'sd') || sorted[sorted.length - 1];
    return sorted[0];
  }
}

module.exports = { PexelsService };
