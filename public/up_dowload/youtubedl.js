const ytdl = require('@distube/ytdl-core');

exports.name = '/youtube/download';
exports.index = async (req, res, next) => {
  let url = req.query.url;
  if (!url)
    return res.json({ error: 'Thiếu dữ liệu để khởi chạy chương trình' });

  try {
    const videoData = await getVideoData(url);
    return res.json(videoData);
  } catch (error) {
    console.log(error);
    return res.json({ error: error.message });
  }
};

async function getVideoData(url) {
  try {
    const info = await ytdl.getInfo(url);

    // Extract video details
    const videoDetails = info.videoDetails;
    const formats = ytdl.filterFormats(info.formats, 'audioonly');

    // Extract relevant information
    const linksFormat = formats.map(format => {
      return {
        type: format.container,
        qualitys: [{
          size: format.contentLength,
          dlink: format.url,
          f: format.container,
          q: format.audioBitrate + ' kbps', // Use audio bitrate as quality
          ftype: format.mimeType.split(';')[0]
        }]
      };
    });

    // Return structured data
    return {
      title: videoDetails.title,
      description: videoDetails.description,
      thumbnail: videoDetails.thumbnails[videoDetails.thumbnails.length - 1].url,
      lengthSeconds: videoDetails.lengthSeconds,
      author: {
        name: videoDetails.author.name,
        channel_url: videoDetails.author.channel_url,
        subscriber_count: videoDetails.author.subscriber_count
      },
      viewCount: videoDetails.viewCount,
      publishDate: videoDetails.publishDate,
      likes: videoDetails.likes,
      dislikes: videoDetails.dislikes,
      category: videoDetails.category,
      keywords: videoDetails.keywords,
      age_restricted: videoDetails.age_restricted,
      audioLinks: linksFormat
    };
  } catch (error) {
    throw new Error('Failed to retrieve video information');
  }
}
